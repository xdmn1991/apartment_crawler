from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .apartment import Apartment
import time
import re
import datetime

month_dict = {
  "jan": 1,
  "feb": 2,
  "mar": 3,
  "apr": 4,
  "may": 5,
  "jun": 6,
  "jul": 7,
  "aug": 8,
  "sep": 9,
  "oct": 10,
  "nov": 11,
  "dev": 12,
}

def month(month_str):
  s = month_str.lower()
  if s in month_dict:
    return month_dict[s]
  return None


class IrvineCommunity:
  def __init__(self, apartment_name, url):
    self.url = url
    self.apartment_name = apartment_name


  def __repr__(self):
    return "Irvine Community {}".format(self.apartment_name)


  def fetch_apartments(self):
    timestamp = datetime.datetime.now()
    today = datetime.date.today()
    driver = webdriver.Firefox()
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
          apt.crawling_time = timestamp
          apt_list.append(apt)

          for i in range(1, len(parts)):
            part = parts[i]
            m = size_pattern.search(part);
            if m is not None:
              apt.bed_num = float(m.group(1)) if m.group(1) else None
              apt.bath_num = float(m.group(2)) if m.group(2) else None
              apt.sqft = int(m.group(3).replace(",", ""))
              continue
            
            m = rent_pattern.search(part)
            if m is not None:
              apt.rent = int(m.group(1).replace(",", ""))
              apt.term = m.group(2)
              continue
            
            m = availability.search(part)
            if m is not None:
              val = m.group(1)
              if val.lower() == "now":
                apt.availability = today
              else:
                m = re.compile("(.*) (\d+)").search(val)
                if m is not None:
                  apt.availability = datetime.date(today.year, month(m.group(1)), int(m.group(2)))
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
    finally:
      driver.quit()
