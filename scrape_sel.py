from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pdb
import re
import json

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
        
        # Extract authors
        authors = [author.text.strip() for author in paper_entry.find_elements(By.XPATH, './/div[@class="note-authors"]/span/a')]
        
        # Extract date and conference
        meta_info = paper_entry.find_elements(By.XPATH, './/ul[@class="note-meta-info list-inline"]/li')
        date = meta_info[0].text.strip()

        conference = meta_info[1].text.strip()

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
           #breakpoint()
           subdriver.get(forum_link)
           # TODO:  Tried to get selenium to correctly parse abstracts, but the dynamic content 
           # on OpenReview is not easy to deal with.  I fell back to old-school regex manipulations.
           time.sleep(5)
           page_source = subdriver.page_source
           abstract_idx = page_source.find("Abstract:")
           abstract_text = page_source[abstract_idx+10:page_source.find("</div", abstract_idx)]
           subdriver.quit()
        except:
           abstract_text = "Abstract retrieval failed"

        #print(abstract_text)
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


if __name__ == '__main__': 
   #search_term="logic"
   MAX_PAGE_LIMIT = 50 
   results = []
   for k in range(1,MAX_PAGE_LIMIT):
      url = "https://openreview.net/search?content=keywords&group=all&page="+str(k)+"&source=all&term=adversarial"
      #url = "https://openreview.net/search?content=all&group=ICLR.cc&page="+str(k)+"&source=forum&term="+search_term
      #url = "https://openreview.net/search?content=all&group=NeurIPS.cc&page="+str(k)+"&source=forum&term="+search_term
      
      # Extract items from the webpage
      extracted_items = extract_papers_selenium(url)

      if not extracted_items:
          break
      
      # Print the extracted items
      #for item in extracted_items:
      #    print(item)

      results += extracted_items

print(json.dumps(results))
