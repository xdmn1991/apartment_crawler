class Apartment:
  comunity = None
  apt_name = None
  bed_num = None
  bath_num = None
  sqft = None
  rent = None
  term = None
  availability = None
  other = None

  @staticmethod
  def fieldnames():
    return ["community", "apartment", "bed", "bath", "sqft", "rent", "term", "availability", "other"]

  def __init__(self, comunity, apt_name):
    self.comunity = comunity
    self.apt_name = apt_name
  
  def __repr__(self):
    return "comunity={}, apt_name={}, bed_num={}, bath_num={}, sqft={}, rent={}, term={}, availability={}, other={}".format(self.comunity, self.apt_name, self.bed_num, self.bath_num, self.sqft, self.rent, self.term, self.availability, self.other)
  
  def valuelist(self):
    return [self.comunity, self.apt_name, self.bed_num, self.bath_num, self.sqft, self.rent, self.term, self.availability, self.other]
  
  def todict(self):
    values = self.valuelist()
    field_names = self.fieldnames()
    d = {}
    for i, field in enumerate(field_names):
      d[field] = values[i]
    return d
