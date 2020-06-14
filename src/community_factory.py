from .community_type import CommunityType
from .irvine_community import IrvineCommunity

class CommunityFactory:
  @staticmethod
  def getCommunity(type, name, url):
    if type == CommunityType.IRVINE:
      return IrvineCommunity(name, url)
    return None