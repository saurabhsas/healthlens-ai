from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors, styles
from reportlab.lib.pagesizes import letter


def export_pdf(kpis, result_df, insights, fig=None):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )

    s = styles.getSampleStyleSheet()

    elems=[]

    elems.append(
      Paragraph(
        "HealthLens Executive Report",
        s["Title"]
      )
    )

    elems.append(
      Spacer(1,20)
    )

    labels={
      "members":"Members",
      "total_cost":"Total Cost",
      "avg_cost":"Average Cost",
      "ed_visits":"ED Visits",
      "ip_visits":"IP Visits"
    }

    for k,v in kpis.items():

        if "cost" in k:
            val=f"${v:,.0f}"
        else:
            val=f"{v:,.0f}"

        elems.append(
          Paragraph(
            f"{labels.get(k,k)}: {val}",
            s["BodyText"]
          )
        )

    elems.append(
      Spacer(1,20)
    )

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


    # -------------------------
    # FORMAT TABLE
    # -------------------------

    preview=result_df.head(20).copy()

    preview=preview.rename(columns={

      "MEDICAL_PAID":"Medical Cost",

      "RX_PAID":"Pharmacy Cost",

      "PAID":"Total Cost",

      "ED_VISITS":"ED Visits",

      "IP_VISITS":"IP Visits",

      "MONTH":"Month"

    })


    for c in [
      "Medical Cost",
      "Pharmacy Cost",
      "Total Cost"
    ]:

        if c in preview.columns:

            preview[c]=(

              preview[c]

              .apply(
                lambda x:
                f"${x:,.0f}"
              )

            )


    for c in [
      "ED Visits",
      "IP Visits"
    ]:

        if c in preview.columns:

            preview[c]=(

              preview[c]

              .apply(
                lambda x:
                f"{x:,.0f}"
              )

            )


    elems.append(
      Paragraph(
        "Data Summary",
        s["Heading2"]
      )
    )

    data=[preview.columns.tolist()]

    data += preview.values.tolist()

    table=Table(data)

    table.setStyle(

      TableStyle([

       ('GRID',(0,0),(-1,-1),1,colors.grey),

       ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),

       ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

       ('ALIGN',(0,0),(-1,0),'CENTER'),

       ('ALIGN',(1,1),(-1,-1),'RIGHT')

      ])

    )

    elems.append(table)

    doc.build(elems)

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes
