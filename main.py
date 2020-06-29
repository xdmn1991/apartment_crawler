from src.apartment import Apartment
from src.community_type import CommunityType
from src.community_factory import CommunityFactory
from src.database import Database
import time

community_list = [
  (CommunityType.IRVINE, "River View", "https://www.irvinecompanyapartments.com/locations/northern-california/san-jose/river-view/availability.html"),
  (CommunityType.IRVINE, "North Park", "https://www.irvinecompanyapartments.com/locations/northern-california/san-jose/north-park/availability.html"),
  (CommunityType.IRVINE, "Crescent Village", "https://www.irvinecompanyapartments.com/locations/northern-california/san-jose/crescent-village/availability.html"),
  (CommunityType.IRVINE, "Santa Clara Square", "https://www.irvinecompanyapartments.com/locations/northern-california/santa-clara/santa-clara-square/availability.html"),
  (CommunityType.IRVINE, "Monticello", "https://www.irvinecompanyapartments.com/locations/northern-california/santa-clara/monticello/availability.html"),
]

while True:
  conn = Database.get_connection()
  print("connectted database...")
  try:
    for type, name, url in community_list:
      community = CommunityFactory.getCommunity(type, name, url)
      print("start fetching apartment list for {}".format(community))
      apt_list = community.fetch_apartments() 
      for apt in apt_list:
        apt.save(conn)
    conn.commit()
  except Exception as e:
    if conn is not None:
      conn.rollback()
    print(e)
  finally:
    if conn is not None:
      conn.close()
    time.sleep(60*10)
