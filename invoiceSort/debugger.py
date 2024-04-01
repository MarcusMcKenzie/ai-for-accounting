from functions import  save_pages, sortVendors, save_text

### For Debugging ###

#pdf_file = '~/Documents/projects/accounting/invoiceSort/Blank.pdf'
pdf_file = 'invoices/small_Invoice.pdf'
#pdf_file = 'Blank.pdf'

date = "January", "2023"
company = "barhiteandholzinger"

vendorFolders, rotatedPages= sortVendors(pdf_file, company)
#vendorFolders = ["Misc", "conedison", "vicky", "chubb"]

#zipPath = save_pages(pdf_file, vendorFolders, rotatedPages, date)
