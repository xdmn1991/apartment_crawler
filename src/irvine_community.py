from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .apartment import Apartment
import time
import re

class IrvineCommunity:
  def __init__(self, apartment_name, url):
    self.url = url
    self.apartment_name = apartment_name

  def fetch_apartments(self):
    driver = webdriver.Chrome()
    try :
      driver.get(self.url)
      driver.implicitly_wait(30) # seconds
      
      size_pattern = re.compile("(?:(.+) BED|STUDIO) \/ (.+) BATH \/ (\d,?\d+) SQ. FT.")
      rent_pattern = re.compile("\$(\d,?\d+) \/ (\d+) MONTHS")
      availability = re.compile("AVAILABLE (.*)")

      retry_count = 0
      while retry_count < 30:
        apt_list = []
        result_lis = driver.find_elements_by_css_selector("#sm-results-set ul.results-list.loaded li")

        for item in result_lis:
          if not item.text:
            continue
          parts = item.text.split('\n')
          apt = Apartment(self.apartment_name, parts[0])
          apt_list.append(apt)

          for i in range(1, len(parts)):
            part = parts[i]
            m = size_pattern.search(part);
            if m is not None:
              apt.bed_num = m.group(1)
              apt.bath_num = m.group(2)
              apt.sqft = m.group(3)
              continue
            
            m = rent_pattern.search(part)
            if m is not None:
              apt.rent = m.group(1)
              apt.term = m.group(2)
              continue
            
            m = availability.search(part)
            if m is not None:
              apt.availability = m.group(1)
              continue
            
            if apt.other is None:
              apt.other = []
            apt.other.append(part)

        actual, expected = len(apt_list), len(result_lis)
        print(actual, expected)
        if actual > 1 and actual == expected:
            return apt_list

        retry_count += 1
        time.sleep(1)
    except Exception:
      return []
    finally:
      driver.quit()
