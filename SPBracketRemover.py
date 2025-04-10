import streamlit as st
import pandas as pd
import io
import re

def to_excel(df):
    """
    Helper function to convert a DataFrame to a downloadable Excel format (in-memory).
    """
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Remove duplicates", index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

st.title("Remove Bracketed Text from Company Names")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Read only the "Remove duplicates" sheet
    df = pd.read_excel(uploaded_file, sheet_name="Remove duplicates")

    # Perform the cleaning
    pattern = r"(?:\.\s*\([^()]*\)|\([^()]*\))$"
    df["Company Name"] = df["Company Name"].str.replace(pattern, "", regex=True)

    st.write("Here is a preview of the cleaned data:")
    st.write(df.head(20))

    # Allow user to download the cleaned file
    cleaned_data = to_excel(df)
    st.download_button(
        label="Download cleaned Excel",
        data=cleaned_data,
        file_name="Cleaned_Merge_Level1.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
