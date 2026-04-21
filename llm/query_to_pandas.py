import json
import re

from llm.groq_client import ask_groq
from llm.prompt_templates import build_prompt


def generate_query(question):

    txt = ask_groq(
        build_prompt(question)
    )

    if not txt or not txt.strip():

        raise Exception(
            "Model returned empty response"
        )

    txt = txt.strip()


    # --------------------------
    # Remove markdown fences
    # --------------------------

    txt = txt.replace(
        "```json",
        ""
    )

    txt = txt.replace(
        "```",
        ""
    )

    txt = txt.strip()


    # --------------------------
    # Extract JSON object
    # --------------------------

    match = re.search(

        r"\{.*\}",

        txt,

        re.DOTALL

    )


    if match:

        txt = match.group(0)


    # --------------------------
    # Repair missing commas
    # --------------------------

    txt = re.sub(

        r'(\"[^\"]+\")\s*(\")',

        r'\1, \2',

        txt

    )


    # --------------------------
    # Try parsing
    # --------------------------

    try:

        return json.loads(
            txt
        )


    except Exception:


        # ----------------------
        # FALLBACKS
        # ----------------------

        q = question.lower()


        # ED/IP fallback

        if (

            "ed" in q

            and

            "ip" in q

        ):

            return {

                "groupby":"MONTH",

                "metrics":[

                    "ED_VISITS",

                    "IP_VISITS"

                ],

                "filters": {},

                "aggregation":"sum"

            }


        # medical/pharmacy fallback

        if (

            "medical" in q

            and

            "pharmacy" in q

        ):

            return {

                "groupby":"MONTH",

                "metrics":[

                    "MEDICAL_PAID",

                    "RX_PAID"

                ],

                "filters": {},

                "aggregation":"sum"

            }


        # generic fallback

        return {

            "groupby":"MONTH",

            "metrics":[

                "PAID"

            ],

            "filters": {},

            "aggregation":"sum"

        }