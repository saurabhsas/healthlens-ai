from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Table,

    Image

)

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib import styles

import tempfile
import uuid
import os


def export_pdf(

    kpis,

    result_df,

    insights,

    fig

):


    # ------------------------
    # FILE PATHS
    # ------------------------

    temp_dir = tempfile.gettempdir()


    pdf_path = os.path.join(

        temp_dir,

        f"healthlens_{uuid.uuid4().hex}.pdf"

    )


    chart_path = os.path.join(

        temp_dir,

        f"chart_{uuid.uuid4().hex}.png"

    )


    # ------------------------
    # SAVE CHART IMAGE
    # requires kaleido
    # ------------------------

    fig.write_image(
        chart_path
    )


    # ------------------------
    # PDF
    # ------------------------

    doc = SimpleDocTemplate(

        pdf_path,

        pagesize=letter

    )


    s = styles.getSampleStyleSheet()


    elems = []


    elems.append(

        Paragraph(

            "HealthLens Executive Report",

            s["Title"]

        )

    )


    elems.append(
        Spacer(1,20)
    )


    # ------------------------
    # FRIENDLY KPI LABELS
    # ------------------------

    label_map = {

        "members":"Members",

        "total_cost":"Total Cost",

        "avg_cost":"Average Cost",

        "ed_visits":"ED Visits",

        "ip_visits":"IP Visits"

    }


    for k,v in kpis.items():

        label = label_map.get(
            k,
            k
        )


        if "cost" in k:

            v = f"${v:,.0f}"

        else:

            v = f"{v:,.0f}"


        elems.append(

            Paragraph(

                f"{label}: {v}",

                s["BodyText"]

            )

        )


    elems.append(
        Spacer(1,20)
    )


    # ------------------------
    # CHART
    # ------------------------

    elems.append(

        Paragraph(

            "Visualization",

            s["Heading2"]

        )

    )


    elems.append(

        Image(

            chart_path,

            width=500,

            height=300

        )

    )


    elems.append(
        Spacer(1,20)
    )


    # ------------------------
    # INSIGHTS
    # ------------------------

    elems.append(

        Paragraph(

            "Executive Insights",

            s["Heading2"]

        )

    )


    elems.append(

        Paragraph(

            insights,

            s["BodyText"]

        )

    )


    elems.append(
        Spacer(1,20)
    )


    # ------------------------
    # FRIENDLY TABLE LABELS
    # ------------------------

    preview = (

        result_df

        .head(20)

        .rename(
            columns={

              "MEDICAL_PAID":"Medical Cost",

              "RX_PAID":"Pharmacy Cost",

              "PAID":"Total Cost",

              "ED_VISITS":"ED Visits",

              "IP_VISITS":"IP Visits",

              "MONTH":"Month"

            }

        )

    )


    # Currency formatting

    currency_cols = [

        "Medical Cost",

        "Pharmacy Cost",

        "Total Cost"

    ]


    for col in currency_cols:

        if col in preview.columns:

            preview[col] = (

                preview[col]

                .apply(

                    lambda x:

                    f"${x:,.0f}"

                )

            )


    # Count formatting

    count_cols = [

        "ED Visits",

        "IP Visits"

    ]


    for col in count_cols:

        if col in preview.columns:

            preview[col] = (

                preview[col]

                .apply(

                    lambda x:

                    f"{x:,.0f}"

                )

            )


    elems.append(

        Paragraph(

            "Data Results",

            s["Heading2"]

        )

    )


    data = [

        preview.columns.tolist()

    ]


    data += preview.values.tolist()


    t = Table(data)


    t.setStyle(

        [

         ("GRID",(0,0),(-1,-1),1,colors.grey)

        ]

    )


    elems.append(t)


    doc.build(elems)


    return pdf_path