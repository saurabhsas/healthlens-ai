def apply_filters(

    df,

    gender,

    lob,

    county,

    cost_category,

    age_category

):

    filtered = df.copy()


    if lob != "All":

        filtered = filtered[

            filtered["LINEOFBUSINESS"] == lob

        ]


    if county != "All":

        filtered = filtered[

            filtered["COUNTY"] == county

        ]


    if cost_category != "All":

        filtered = filtered[

            filtered["COST_CATEGORY"] == cost_category

        ]


    if age_category != "All":

        filtered = filtered[

            filtered["AGE_CATEGORY"] == age_category

        ]


    if gender != "All":

        filtered = filtered[

            filtered["GENDER"] == gender

        ]


    return filtered