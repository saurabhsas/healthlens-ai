import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv('data/healthcare_data.csv')
    df.columns = df.columns.str.strip().str.upper()
    df = df.rename(columns={
        'ELIGIBILITYYEARANDMONTH':'MONTH',
        'EDVISITS':'ED_VISITS',
        'IPVISITS':'IP_VISITS'
    })
    return df