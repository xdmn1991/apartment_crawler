class Apartment:
  comunity = None
  apt_name = None
  bed_num = None
  bath_num = None
  sqft = None
  rent = None
  term = None
  availability = None
  crawling_time = None
  other = None

  @staticmethod
  def fieldnames():
    return ["community", "apartment", "bed", "bath", "sqft", "rent", "term", "availability", "other", "crawling_time"]

  def __init__(self, comunity, apt_name):
    self.comunity = comunity
    self.apt_name = apt_name
  
  def __repr__(self):
    return "comunity={}, apt_name={}, bed_num={}, bath_num={}, sqft={}, rent={}, term={}, availability={}, other={}".format(self.comunity, self.apt_name, self.bed_num, self.bath_num, self.sqft, self.rent, self.term, self.availability, self.other)
  
  def valuelist(self):
    return [self.comunity, self.apt_name, self.bed_num, self.bath_num, self.sqft, self.rent, self.term, self.availability, self.other, self.crawling_time]
  
  def todict(self):
    values = self.valuelist()
    field_names = self.fieldnames()
    d = {}
    for i, field in enumerate(field_names):
      d[field] = values[i]
    return d
  
  def save(self, conn):
    cur = conn.cursor()
    cur.execute("""INSERT INTO rent_detail 
                        (community, apartment, sqft, bed_num, bath_num, rent, availability, crawling_time, other)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                  (self.comunity, self.apt_name, self.sqft, self.bed_num, self.bath_num, self.rent, self.availability, self.crawling_time, ", ".join(self.other) if self.other is not None else None)
                )
    cur.close()
