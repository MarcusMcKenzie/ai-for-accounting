import streamlit as st
from zipfile import ZipFile
import os, os.path
import re
import io
import shutil
import base64
#------- OCR ------------
import pdf2image
import pytesseract
from pytesseract import Output
from pypdf import PdfReader, PdfWriter

from fpdf import FPDF
import psycopg2

import companyAndVendorList


#@st.cache_data #comment out if debugging #remove comment if using streamlit
def sortVendors(path, company):
    #images = pdf2image.convert_from_bytes(path) #for streamlit
    images = pdf2image.convert_from_path(path) #for debugger

    #save_text(images) #for inputting text doc to chatGPT API

    vendorFolders = []
    rotatedPages = []
    vendors = {} 

    #select vendor list - look up database
    vendors = companyAndVendorList.accessDatabase(company) #will create new database if doesn't exist

    # loop through pages of invoice PDF
    for i in range(len(images)):
                  
        pil_im = images[i]

        # determine if page is blank
        if len(pytesseract.image_to_string(images[i])) <= 1:
            vendorFolders.append("Blank")
            rotatedPages.append(0)
            continue

        #rotate page
        page_rotation, rotated_pil_im = rotatePage(pil_im)
        rotatedPages.append(page_rotation)

        # store ocr text in dictionary
        ocr_dict = pytesseract.image_to_data(rotated_pil_im, lang='eng', output_type=Output.DICT)
        vendorFolder = getVendors(ocr_dict, vendors)
        vendorFolders.append(vendorFolder)
    
    return vendorFolders, rotatedPages



def rotatePage(pil_im):
  #get image orientation details
  osd_rotated_image = pytesseract.image_to_osd(pil_im)

  rotated_pil_im = pil_im

  #get rotated value
  angle_rotatation = re.search('(?<=Rotate: )\d+', osd_rotated_image).group(0)

  #rotate image if upside down
  if (angle_rotatation != '0'):
    if (angle_rotatation == '90'):
        rotated_pil_im = pil_im.rotate(90)
        rotatedPage = 90
    elif (angle_rotatation == '180'):
        rotated_pil_im = pil_im.rotate(180)
        rotatedPage = 180
    elif (angle_rotatation == '270'):
        rotated_pil_im = pil_im.rotate(270)
        rotatedPage = 270
  else: 
      rotatedPage = 0

  return rotatedPage, rotated_pil_im



def getVendors(ocr_dict, vendors):
  vendorFolder = []

  ocr_dict_lower = {}
  for text in ocr_dict['text']:
      if not text.isspace():
        ocr_dict_lower[text.lower()] = 0

  isVendorFound = False
  #loop through ocr text dictionary to see if vendor listed in pdf(ocr dictionary)
  for vendor in vendors.keys():
      
    #if vendor found, put in respective vendor folder
    if vendor in ocr_dict_lower:
      vendorFolder = vendors[vendor]
      isVendorFound = True
      break
      
  #if vendor not found, put page in Miscellaneous folder
  if isVendorFound == False:
    vendorFolder = "Misc"

  #IF VENDOR NOT FOUND OR Vendor == None CALL CHATGPT API 
  #store vendor info into database
  #store vendor name into vendorFolder list
  #vendorFolder = API_vendorName 

  return vendorFolder



#@st.cache_data #comment out if debugging #remove comment if using streamlit
def save_pages(file_path, vendorFolders, rotatedPages, date):
  pdf_reader = PdfReader(file_path)
  files = []

  #remove all contents previously in folder
  isFolderExisting = os.path.isdir("./Sorted Invoices/")
  if isFolderExisting:
     shutil.rmtree("./Sorted Invoices/")

  #loop through pages
  for i in range(len(vendorFolders)):
    page = pdf_reader.pages[i]

    #rotate page
    page.rotate(rotatedPages[i]) 

    file = add_page(vendorFolders, page, date, i)  
    files.append(file) 

  zipPath = create_zip(files)
  
  return zipPath


def add_page(vendorFolders, page, date, i):
    pdf_writer = PdfWriter()
    filename = "pages_from_"+str(date[0])+"_"+str(date[1])+".pdf"

    #check to see if vendor file already has a page added
    os.mkdir
    isFileExisting = os.path.isdir("./Sorted Invoices/"+str(vendorFolders[i]))

    #add page to existing vendor file 
    if isFileExisting:
      file_loc = "./Sorted Invoices/"+str(vendorFolders[i])+"/"+filename
      os.mkdir
      os.makedirs(os.path.dirname(file_loc), exist_ok=True)

      with safe_open_rb("./Sorted Invoices/"+str(vendorFolders[i])+"/"+filename) as file2:
        pdf_reader2 = PdfReader(io.BytesIO(file2.read()))
        pdf_writer.append_pages_from_reader(pdf_reader2)
        pdf_writer.add_page(page)
        pdf_writer.remove_links()
        pdf_writer.write(file_loc)
        file = file_loc

    # create new vendor file and add page
    else:
      with safe_open_w("./Sorted Invoices/"+str(vendorFolders[i])+"/"+filename) as file:
        pdf_writer.add_page(page)
        pdf_writer.remove_links()
        pdf_writer.write(file.name)
        file = file.name

    return file


def create_zip(files):
  os.mkdir
  os.makedirs(os.path.dirname("./Sorted Invoices/sorted_invoice.zip"), exist_ok=True)
  zipPath = './Sorted Invoices/sorted_invoice.zip'
  zipObj = ZipFile(zipPath, 'w')
  for file in files:
     if file[2:] not in zipObj.namelist():
        zipObj.write(file)

  zipObj.close()
  return zipPath

#needed for saving in new folder
def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')
  

def safe_open_rb(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'rb')



def save_text(images):
  i = 0
  for image in images:
      i = i + 1
      print("i: ", i)
      pdf_writer = PdfWriter()
      page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
      pdf = PdfReader(io.BytesIO(page))
      pdf_writer.add_page(pdf.pages[0])

      # export the searchable PDF to searchable.pdf
      with safe_open_w("./invoicesAsDocs/invoice"+str(i)+".docx") as f:
          pdf_writer.write("./invoicesAsDocs/invoice"+str(i)+".docx")
