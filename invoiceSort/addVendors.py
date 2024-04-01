import streamlit as st
import datetime

from functions import  save_pages, sortVendors, companyAndVendorList

st.title('Add Vendors')

#company = ""

#add company
#add vendors
#Delete company/vendors?
#Add ability to add other keywords


#input widgets for streamlit UI
#how to create a new dictionary for each company?

companyOrVendor = st.selectbox("New Company or New Vendor?", ["", "New Company", "New Vendor"])

if companyOrVendor != "" and companyOrVendor == "New Company":
    newCompany = st.text_input("Company Name")
    if newCompany != "":
        with st.spinner(text="Please wait. This may take a moment..."):
            if newCompany not in companyAndVendorList.companies.keys():

                #add company to company dictionary
                #companyAndVendorList.companies[newCompany] = newCompany + str(Vendors())
                
                #create new vendor function 
                #companyAndVendorList

                st.success('Done!')

            else: 

                # error message if company name already in list
                st.markdown(":red[**Company name already in list.**]")
    
  
  #how to create a new dictionary for each company?

  #select company name
  #all from invoice details
  #The system will search through the invoice for these keywords
  #Provide Example
  #enter vendor name
  #enter vendor phone number #no area code if in parenthesis on invoice
  #enter vendor email 
  #enter vendor website address

if companyOrVendor != "" and companyOrVendor == "New Vendor":
  
    companyList = list(companyAndVendorList.companies.keys())
    companyList.insert(0, "")
    companyName = st.selectbox("Select Company of Invoice", "" + list(companyAndVendorList.companies.keys()) )


    vendorName = st.text_input("Vendor Name")
    vendorPhoneNumber = st.text_input("Vendor Phone Number")
    vendorEmail = st.text_input("Vendor Email Address")
    vendorWebsite = st.text_input("Vendor Website")
  
    #companyAndVendorList.companies[companyName] = 
    #companyAndVendorList.init_db(companyAndVendorList.companies.get(companyName))

    #