import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time

# Declaring function to get the details of data
def get_company_code(soup):
    try:
        row = soup.find('th', string = "Kode Perusahaan").find_parent('tr')   
        return row.find_all('td')[-1].get_text(strip=True)
    except AttributeError:
        return None
    
def get_company_name(soup):
    try:
        row = soup.find('th', string= "Nama Perusahaan").find_parent('tr')
        return row.find_all('td')[1].get_text(strip=True)
    except AttributeError:
        return None
    
# Declaring function for business_entity
def get_business_entity(soup):
    try:
        row = soup.find('th', string="Jenis Badan Usaha").find_parent('tr')
        return row.find_all('td')[-1].get_text(strip=True)
    except AttributeError:
        return None
    
# Declaring function for no_deed
def get_no_deed(soup):
    try:
        row = soup.find('th', string = "No. Akte").find_parent('tr')
        return row.find_all('td')[-1].get_text(strip=True)
    except AttributeError:
        return None
    

# Declaring function for date_deed
def get_date_deed(soup):
    try:
        row = soup.find('th', string = "Tgl. Akte").find_parent('tr')
        return row.find_all('td')[-1].get_text(strip=True)
    except AttributeError:
        return None
    

# Declaring function to get office flag
def get_office_flag(soup):
    try:
        row = soup.find('div', class_ ="col-md-9 table-responsive")
        office_flag_tag = row.find_all('td', class_ = "")
        office_flag = office_flag_tag[1].get_text(strip=True)
    except AttributeError:
        return None
    
    return office_flag


# Declaring function to get office address
def get_office_address(soup):
    try:
        row = soup.find('div', class_ ="col-md-9 table-responsive")
        tag = row.find_all('td', class_ = "")
        office_address = tag[2].get_text(strip=True)
    except AttributeError:
        return None
    
    return office_address

# Declaring function to get contact_person
def get_contact_person(soup):
    try:
        row = soup.find('div', class_ ="col-md-9 table-responsive")
        tag = row.find_all('td', class_ = "")
        contact_person = tag[3].get_text(strip=True)
    except AttributeError:
        return None
    
    return contact_person

# MAIN PROGRAM
# Declaring necessary variables
base_url = "https://modi.esdm.go.id/portal/dataPerusahaan"
total_pages = 20
all_company_links = []

# Iteration to generate pagenated links, number of total pages refer to total_pages
for page in range(1, total_pages +1):
    print(f"Scraping page {page} of {total_pages}")

    page_url = f"{base_url}?=page{page}"

    response_page = requests.get(page_url)

    soup = BeautifulSoup(response_page.text, 'lxml')

    # Iteration to generate company_link/url, and store it to all_company_links stack
    for a_tag in soup.find_all('a', href=True):
        if "portal/detailPerusahaan/" in a_tag['href']:
            company_link = a_tag['href']
            all_company_links.append(company_link)

# Create interval for 2s between iteration: Be Polite to the server that arent yours!
time.sleep(2)

# Creating Dictionary to prepare for dataframe creation
result = {'company_code': [], 'company_name': [], 'business_entity': [], 'no_deed': [], 'date_deed': [], 'office_flag': [], 'office_address': [], 'contact_person': []}

# Iterate the the company link gathered from previous iteration, to generate 
for link in all_company_links:
    new_page = requests.get(link)
    new_soup = BeautifulSoup(new_page.text, 'lxml')

    result['company_code'].append(get_company_code(new_soup))
    result['company_name'].append(get_company_name(new_soup))
    result['business_entity'].append(get_business_entity(new_soup))
    result['no_deed'].append(get_no_deed(new_soup))
    result['date_deed'].append(get_date_deed(new_soup))
    result['office_flag'].append(get_office_flag(new_soup))
    result['office_address'].append(get_office_address(new_soup))
    result['contact_person'].append(get_contact_person(new_soup))

# Create interval for 2s between iteration: Be Polite to the server that arent yours!
time.sleep(2)

#Create dataframe from dictionary
dataset_modi = pd.DataFrame.from_dict(result)

# DATA TRANSFORMING:
dataset_modi['company_code']    = dataset_modi['company_code'].astype('int64')
dataset_modi['company_name']    = dataset_modi['company_name'].astype('string')
dataset_modi['business_entity'] = dataset_modi['business_entity'].astype('string')
dataset_modi['no_deed']         = dataset_modi['no_deed'].astype('string')
dataset_modi['date_deed']       = pd.to_datetime(dataset_modi['date_deed'])
dataset_modi['office_flag']     = dataset_modi['office_flag'].astype('string')
dataset_modi['office_address']  = dataset_modi['office_address'].astype('string')
dataset_modi['contact_person']  = dataset_modi['contact_person'].astype('string')


# Exporting dataframe to .csv file
export_path = r"C:\Users\user\OneDrive\RFA _Personal Files\02. COURSE\Purwadhika_Data Engineering\Purwadhika_VS\meet42_scraping\data_modi\data_modi.csv"
dataset_modi.to_csv(export_path, index=False)
