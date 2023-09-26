from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_papers_selenium(url):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    
    # Navigate to the URL
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)
    
    # Initialize an empty list to store extracted items
    extracted_items = []

    base_url = "https://openreview.net"
    
    # Loop through each paper entry in the webpage
    for paper_entry in driver.find_elements(By.XPATH, '//div[@class="note  "]'):
        # Extract title
        title = paper_entry.find_element(By.XPATH, './/h4/a[1]').text.strip()
#        print("Testing TITLE")
#        print(f"Title: {title}")
#        print(title)
        
        # Extract authors
        authors = [author.text.strip() for author in paper_entry.find_elements(By.XPATH, './/div[@class="note-authors"]/span/a')]
#        print(f"Authors: {authors}")
#        print(authors)
        
        # Extract date and conference
        meta_info = paper_entry.find_elements(By.XPATH, './/ul[@class="note-meta-info list-inline"]/li')
        date = meta_info[0].text.strip()
#        print(f"Date: {date}")
#        print(date)

        conference = meta_info[1].text.strip()
#        print(f"Conference: {conference}")
#        print(conference)

        # Try to extract PDF URL
        try:
            pdf_relative_url = paper_entry.find_element(By.XPATH, './/h4/a[@class="pdf-link"]').get_attribute("href")
            pdf_full_url = base_url + pdf_relative_url
        except:
            pdf_full_url = "PDF not available"

        
        # Pull the abstrat
        forum_link = paper_entry.find_element(By.XPATH, './/h4/a[1]').get_attribute("href")
        subdriver = webdriver.Chrome()
        try:
           subdriver.get(forum_link)
           #time.sleep(3)
           #abstract = "TO DO: write a function for this"
           # Wait until the abstract element is available
           element_present = EC.presence_of_element_located((By.XPATH, '//div[@class="note-content"]/div/strong[text()="Abstract:"]/following-sibling::span'))
           WebDriverWait(subdriver, 10).until(element_present)
           # TODO: the following does not correctly pull out the abstract
           abstract_text = subdriver.find_element(By.XPATH, '//div[@class="note-content"]/div/strong[text()="Abstract:"]/following-sibling::span').text
           subdriver.quit()
        except:
           abstract_text = "Abstract retrieval failed"

        # Store the extracted information in the specified format
        extracted_items.append({
            'title': title,
            'authors': authors,
            'Conference': conference,
            'date': date,
            'link': pdf_full_url,
            'abstract': abstract_text
        })
    
    # Close the browser
    driver.quit()
    
    return extracted_items

# URL of the webpage to scrape

search_term="logic"
for k in range(9,10):
   url = "https://openreview.net/search?content=all&group=ICLR.cc&page="+str(k)+"&source=forum&term="+search_term
   #url = "https://openreview.net/search?content=all&group=NeurIPS.cc&page="+str(k)+"&source=forum&term="+search_term
   
   # Extract items from the webpage
   extracted_items = extract_papers_selenium(url)
   
   # Print the extracted items
   for item in extracted_items:
       print(item)

