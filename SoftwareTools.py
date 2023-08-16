#Import Modules
import pandas as pd
import streamlit as st
from openpyxl import load_workbook


#Load data
file = "C:\\Users\\bhearley\Box\\Software Tools Documentation\\Utility\\Summary.xlsx"
DF = pd.read_excel(file)


st.title('NASA GRC Software Tools')
st.dataframe(DF)
