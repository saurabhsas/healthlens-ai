from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table
)
from reportlab.lib import colors, styles
from reportlab.lib.pagesizes import letter
import tempfile, uuid, os


def export_pdf(kpis, result_df, insights, fig=None):
    temp = tempfile.gettempdir()

    pdf_path = os.path.join(
        temp,
        f"healthlens_{uuid.uuid4().hex}.pdf"
    )

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

    labels = {
      "members":"Members",
      "total_cost":"Total Cost",
      "avg_cost":"Average Cost",
      "ed_visits":"ED Visits",
      "ip_visits":"IP Visits"
    }

    # KPIs
    for k,v in kpis.items():

        if "cost" in k:

            val = f"${v:,.0f}"

        else:

            val = f"{v:,.0f}"

        elems.append(
            Paragraph(
                f"{labels.get(k,k)}: {val}",
                s["BodyText"]
            )
        )

    elems.append(
        Spacer(1,20)
    )

    # Insights
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

    # Data preview
    elems.append(
        Paragraph(
            "Data Summary",
            s["Heading2"]
        )
    )

    preview = result_df.head(20)

    data = (
        [preview.columns.tolist()]
        +
        preview.values.tolist()
    )

    t = Table(data)

    t.setStyle([
      ('GRID',(0,0),(-1,-1),1,colors.grey)
    ])

    elems.append(t)

    doc.build(elems)

    return pdf_path
