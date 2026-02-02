from enum import Enum
from typing import Optional, List, Set, Tuple, Dict
from publicsuffix2 import get_sld
import string

# Facets and values 

class Party(Enum):
    FIRST = 0
    THIRD = 2

class Duration(Enum):
    SESSION = 0
    PERSISTENT = 1

class InformationCapacity(Enum):
    LOW = 0
    HIGH = 3

class Security(Enum):
    SECURE = 0
    NONSECURE = 1

# Classes

class RawCookie:
    name: str
    value: str
    domain: str
    path: Optional[str]
    secure: bool
    expires: Optional[str]
    max_age: Optional[int]

    def __init__(self,raw_string):
      parts = raw_string.split(";")

      if "=" not in parts[0]:
        return # malformed cookie string

      name, value = parts[0].split("=", 1)
      domain = ""
      path = None
      secure = False
      expires = None
      max_age = None

      for p in parts[1:]:
        pl = p.lower()
        if pl == "secure":
          secure = True
        elif pl.startswith("domain="):
          domain = p.split("=", 1)[1].strip()
        elif pl.startswith("path="):
          path = p.split("=", 1)[1].strip()
        elif pl.startswith("max-age="):
          try:
            max_age = int(p.split("=", 1)[1].strip())
          except ValueError:
            max_age = None
        elif pl.startswith("expires="):
          expires = p.split("=", 1)[1].strip()

      self.name = name
      self.value = value
      self.domain = domain
      self.path = path
      self.secure = secure
      self.expires = expires
      self.max_age = max_age

class Cookie:
    key: Tuple[str, str, Optional[str]]
    party: Party
    duration: Duration
    information_capacity: InformationCapacity
    security: Security
    severity: int

    def __init__(self, raw_cookie, visited_domain):
      r_cookie = RawCookie(raw_cookie)
      self.key = (r_cookie.name, r_cookie.domain, r_cookie.path)
      self.party = self.party_definition(r_cookie, visited_domain)
      self.duration = self.duration_definition(r_cookie)
      self.information_capacity = self.information_capacity_definition(r_cookie)
      self.security = self.security_definition(r_cookie)
      self.severity = self.severity_measure()
      
    def party_definition(self, r_cookie, visited_domain):
      if not r_cookie.domain:
        return Party.FIRST

      if get_sld(r_cookie.domain) == get_sld(visited_domain):
        return Party.FIRST
      return Party.THIRD

    def duration_definition(self, r_cookie):
      if r_cookie.max_age is not None:
        if r_cookie.max_age > 0:
          return Duration.PERSISTENT
        return Duration.SESSION
      
      if r_cookie.expires is not None:
        return Duration.PERSISTENT
      return Duration.SESSION

    def security_definition(self, r_cookie):
      if r_cookie.secure:
        return Security.SECURE
      else:
        return Security.NONSECURE

    
    def information_capacity_definition(self, r_cookie):
      value = r_cookie.value
      if value is None:
        return InformationCapacity.LOW
      
      if len(value) <= 16:
        return InformationCapacity.LOW
      
      has_digit_or_special = any(c not in string.ascii_letters for c in value)
      if has_digit_or_special:
        return InformationCapacity.HIGH
      return InformationCapacity.LOW

    def severity_measure(self):
        return self.party.value + self.duration.value + self.information_capacity.value + self.security.value

class Website:
    rank_id: int
    domain: str
    cookies: List[Cookie]
    cookie_keys: Set[Tuple[str, str, Optional[str]]]

    def __init__(self, rank_id, domain):
      self.rank_id = rank_id
      self.domain = domain
      self.cookies = []
      self.cookie_keys = set()
    
    def add_cookie(self, raw_cookie):
      new_cookie = Cookie(raw_cookie, self.domain)
      if new_cookie.key in self.cookie_keys:
            return 
      self.cookies.append(new_cookie)
      self.cookie_keys.add(new_cookie.key)

    def get_severity(self):
      sum = 0
      if len(self.cookies) == 0:
        return sum
      for cookie in self.cookies:
        sum += cookie.severity
      return sum / len(self.cookies)


class WebsiteCollection:
    def __init__(self):
        self.websites: Dict[int, Website] = {}

    def get_or_create(self, rank_id, domain):
        if rank_id not in self.websites:
            self.websites[rank_id] = Website(rank_id, domain)
        return self.websites[rank_id]
