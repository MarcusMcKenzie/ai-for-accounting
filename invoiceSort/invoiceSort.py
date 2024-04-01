import streamlit as st
import datetime

from functions import  save_pages, sortVendors, create_txt, companyAndVendorList

st.title('Invoice Sorter')

uploaded_file = None
company = ""


#input widgets for streamlit UI
year = st.number_input("Select Year of Invoice", datetime.date.today().year-10, datetime.date.today().year, value=datetime.date.today().year)
month = st.selectbox("Select Month of Invoice", ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], )
date = month, year

if month != "":
  companyList = list(companyAndVendorList.companies.keys())
  companyList.insert(0, "")
  company = st.selectbox("Select Company of Invoice", companyList)

if company != "":
  uploaded_file = st.file_uploader("Upload your PDF Invoice")

if uploaded_file is not None:

  file_extension = uploaded_file.name.split(".")[-1]

  with st.spinner(text="Please wait. This may take a moment..."):
    if file_extension == "pdf":

      pdf_file = uploaded_file.read()

      # determine vendor for each page
      vendorFolders, rotatedPages, pageText = sortVendors(pdf_file, company)

      # save pages to vendor folder in zip folder
      zipPath = save_pages(uploaded_file, vendorFolders, rotatedPages, date)

      #txtLoc = "example.txt"
      #create_txt(txtLoc, pageText)

      # download pdf data   
      with open(zipPath, "rb") as fp:
          btn = st.download_button(
              label="Download ZIP (pdf)",
              data=fp,
              file_name="sorted_invoice.zip",
              mime="application/zip"
          )

      st.success('Done!')

    else: 

      # error message if non-pdf is provided
      st.markdown(":red[**Please select a PDF file. Non-PDF files not accepted.**]")

