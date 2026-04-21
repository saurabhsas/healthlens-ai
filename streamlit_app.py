import streamlit as st

from core.data_loader import load_data
from core.filters import apply_filters
from core.metrics import get_kpis

from llm.query_to_pandas import generate_query
from llm.groq_client import ask_insights

from core.query_executor import run_structured_query

from visualization.chart_router import build_chart

from reporting.pdf_export import export_pdf


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="HealthLens Executive Dashboard",
    layout="wide"
)

st.title(
    "🏥 HealthLens Executive Dashboard"
)

st.caption(
    "AI-Powered Healthcare Analytics"
)


# -----------------------------
# LOAD DATA
# -----------------------------

df = load_data()


# -----------------------------
# FILTERS
# -----------------------------

with st.sidebar:

    st.header("Filters")


    lob_options=(

      ["All"]

      +

      sorted(

       df["LINEOFBUSINESS"]

       .dropna()

       .unique()

      )

    )

    lob=st.selectbox(
      "Line of Business",
      lob_options
    )


    df1=df.copy()

    if lob!="All":

        df1=df1[
          df1["LINEOFBUSINESS"]==lob
        ]


    county_options=(

      ["All"]

      +

      sorted(
       df1["COUNTY"]
       .dropna()
       .unique()
      )

    )

    county=st.selectbox(
      "County",
      county_options
    )


    df2=df1.copy()

    if county!="All":

        df2=df2[
          df2["COUNTY"]==county
        ]


    cost_options=(

      ["All"]

      +

      sorted(
       df2["COST_CATEGORY"]
       .dropna()
       .unique()
      )

    )

    cost_category=st.selectbox(
      "Cost Category",
      cost_options
    )


    df3=df2.copy()

    if cost_category!="All":

        df3=df3[
          df3["COST_CATEGORY"]
          ==cost_category
        ]


    age_options=(

      ["All"]

      +

      sorted(
       df3["AGE_CATEGORY"]
       .dropna()
       .unique()
      )

    )

    age_category=st.selectbox(
      "Age Category",
      age_options
    )


    df4=df3.copy()

    if age_category!="All":

        df4=df4[
          df4["AGE_CATEGORY"]
          ==age_category
        ]


    gender_options=(

      ["All"]

      +

      sorted(
       df4["GENDER"]
       .dropna()
       .unique()
      )

    )

    gender=st.selectbox(
      "Gender",
      gender_options
    )


filtered=apply_filters(
    df,
    gender,
    lob,
    county,
    cost_category,
    age_category
)


# -----------------------------
# EXAMPLE QUERIES
# -----------------------------

examples=[

"",

"Show monthly total cost trend",

"Compare medical and pharmacy cost",

"Trend of medical and pharmacy cost over months",

"Compare ED and IP utilization",

"Compare ED and IP utilization by gender",

"Compare total cost by gender",

"Compare total cost by county",

"Compare cost by line of business",

"Show medical cost trend for females",

"Show pharmacy cost trend for males",

"Compare avoided cost by county for males"

]


selected=st.selectbox(
    "Select example query",
    examples
)


query=st.text_input(
    "Ask a healthcare question",
    value=selected
)


# -----------------------------
# RUN ANALYSIS
# -----------------------------

if st.button(
   "Generate Insights"
):

    try:

        query_json=generate_query(
            query
        )


        if "groupby" not in query_json:
            query_json["groupby"]="MONTH"

        if "aggregation" not in query_json:
            query_json["aggregation"]="sum"

        if "filters" not in query_json:
            query_json["filters"]={}

        if "metrics" not in query_json:
            query_json["metrics"]=["PAID"]


        result=(

           run_structured_query(
             query_json,
             filtered
           )

           .reset_index()

        )


        kpis=get_kpis(
            filtered
        )


        c1,c2,c3,c4,c5=st.columns(5)

        c1.metric(
         "👥 Members",
         f"{kpis['members']:,}"
        )

        c2.metric(
         "💰 Total Cost",
         f"${kpis['total_cost']:,.0f}"
        )

        c3.metric(
         "📊 Avg Cost",
         f"${kpis['avg_cost']:,.0f}"
        )

        c4.metric(
         "🏥 ED Visits",
         f"{kpis['ed_visits']:,}"
        )

        c5.metric(
         "🛏️ IP Visits",
         f"{kpis['ip_visits']:,}"
        )


        insights=ask_insights(

            result.head(20)

            .to_string()

        )


        fig=build_chart(
            result,
            query
        )


        tab1,tab2,tab3=st.tabs(
          [
           "📈 Visualization",
           "🧠 Executive Insights",
           "🗂 Data"
          ]
        )


        # -------------------------
        # CHART
        # -------------------------

        with tab1:

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # -------------------------
        # INSIGHTS
        # -------------------------

        with tab2:

            st.info(
                insights
            )


        # -------------------------
        # DATA TAB
        # -------------------------

        with tab3:

            display_result=result.copy()

            display_result=display_result.rename(

              columns={

                "MEDICAL_PAID":"Medical Cost",

                "RX_PAID":"Pharmacy Cost",

                "PAID":"Total Cost",

                "ED_VISITS":"ED Visits",

                "IP_VISITS":"IP Visits",

                "MONTH":"Month"

              }

            )


            for col in [

              "Medical Cost",

              "Pharmacy Cost",

              "Total Cost"

            ]:

                if col in display_result.columns:

                    display_result[col]=(

                      display_result[col]

                      .apply(

                       lambda x:

                       f"${x:,.0f}"

                      )

                    )


            for col in [

              "ED Visits",

              "IP Visits"

            ]:

                if col in display_result.columns:

                    display_result[col]=(

                      display_result[col]

                      .apply(

                       lambda x:

                       f"{x:,.0f}"

                      )

                    )


            styled=(

              display_result

              .style

              .set_properties(

                subset=[

                 c for c in [

                  "Medical Cost",

                  "Pharmacy Cost",

                  "Total Cost",

                  "ED Visits",

                  "IP Visits"

                 ]

                 if c in display_result.columns

                ],

                **{

                  "text-align":"right"

                }

              )

            )


            st.dataframe(
                styled,
                use_container_width=True
            )


        # -------------------------
        # PDF DOWNLOAD
        # -------------------------

        pdf_path=export_pdf(
            kpis,
            result,
            insights,
            fig
        )


        with open(
          pdf_path,
          "rb"
        ) as f:

            st.download_button(

              "Download Executive PDF Report",

              data=f,

              file_name="healthlens_report.pdf",

              mime="application/pdf"

            )


    except Exception as e:

        st.error(
          f"Error: {str(e)}"
        )
