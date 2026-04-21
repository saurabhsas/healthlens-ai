import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def ask_groq(prompt):
    r = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role':'user','content':prompt}],
        temperature=0
    )
    return r.choices[0].message.content

def ask_insights(result_text):
    prompt=f'''Provide exactly 3 concise executive insights as bullet points from this healthcare summary:
{result_text}'''
    return ask_groq(prompt)