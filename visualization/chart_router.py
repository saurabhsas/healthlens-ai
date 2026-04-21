import plotly.express as px


LABEL_MAP = {

    "MEDICAL_PAID":"Medical Cost",

    "RX_PAID":"Pharmacy Cost",

    "PAID":"Total Cost",

    "ED_VISITS":"ED Visits",

    "IP_VISITS":"IP Visits",

    "MONTH":"Month",

    "GENDER":"Gender",

    "COUNTY":"County",

    "LINEOFBUSINESS":"Line of Business"

}


def prettify_columns(df):

    df = df.copy()

    df.columns = [

        LABEL_MAP.get(
            c,
            c
        )

        for c in df.columns

    ]

    return df



def build_chart(df, title):

    df = prettify_columns(df)


    numeric = (

        df.select_dtypes(
            include="number"
        )

        .columns

        .tolist()

    )


    if "Month" in df.columns:

        fig = px.line(

            df,

            x="Month",

            y=numeric,

            markers=True,

            title=title

        )


    elif len(numeric) > 1:

        fig = px.bar(

            df,

            x=df.columns[0],

            y=numeric,

            barmode="group",

            title=title

        )


    else:

        fig = px.bar(

            df,

            x=df.columns[0],

            y=df.columns[1],

            title=title

        )


    fig.update_layout(
        height=550
    )

    return fig