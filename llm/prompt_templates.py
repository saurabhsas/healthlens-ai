def build_prompt(question):
    
    return f"""
Convert question into VALID JSON ONLY.

Allowed columns:

MONTH
PAID
MEDICAL_PAID
RX_PAID
GENDER
COUNTY
LINEOFBUSINESS
ED_VISITS
IP_VISITS
AVOIDED

Use GENDER values:

M
F

Rules:

If a comparison question does not specify a grouping dimension,

default to:

"groupby":"MONTH"

Examples:

Question:
Compare medical and pharmacy cost

Return:

{{
"groupby":"MONTH",

"metrics":[
"MEDICAL_PAID",
"RX_PAID"
],

"filters":{{}},

"aggregation":"sum"
}}

Question:
Compare ED and IP utilization

Return:

{{
"groupby":"MONTH",

"metrics":[
"ED_VISITS",
"IP_VISITS"
],

"filters":{{}},

"aggregation":"sum"
}}

Question:
Compare cost by gender

Return:

{{
"groupby":"GENDER",

"metrics":[
"PAID"
],

"filters":{{}},

"aggregation":"sum"
}}

Format:

{{
"groupby":"COLUMN",

"metrics":[
"COL1",
"COL2"
],

"filters":{{}},

"aggregation":"sum"
}}

Question:

{question}

Return JSON only.
"""