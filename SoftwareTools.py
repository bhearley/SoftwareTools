#Import Modules
import pandas as pd
import streamlit as st


#Load data
file = "https://github.com/bhearley/SoftwareTools/blob/main/Summary.xlsx"
DF = pd.read_excel(file)


st.title('NASA GRC Software Tools')
st.dataframe(DF)
