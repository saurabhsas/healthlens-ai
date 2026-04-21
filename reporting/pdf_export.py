from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
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

    elems=[]

    elems.append(
        Paragraph(
            'HealthLens Executive Report',
            s['Title']
        )
    )

    elems.append(Spacer(1,20))

    labels={
      'members':'Members',
      'total_cost':'Total Cost',
      'avg_cost':'Average Cost',
      'ed_visits':'ED Visits',
      'ip_visits':'IP Visits'
    }

    for k,v in kpis.items():

        if 'cost' in k:
            val=f'${v:,.0f}'
        else:
            val=f'{v:,.0f}'

        elems.append(
            Paragraph(
                f"{labels.get(k,k)}: {val}",
                s['BodyText']
            )
        )

    elems.append(Spacer(1,20))
    return pdf_path
