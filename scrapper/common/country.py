from enum import Enum, unique


class NoValue(Enum):
  def __repr__(self):
    return '<%s.%s>' % (self.__class__.__name__, self.name)

@unique
class Country(NoValue):
  CZ = 'cz'
  SK = 'sk'
