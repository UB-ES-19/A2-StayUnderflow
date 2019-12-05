from enum import Enum

from utils.time import forDjango


@forDjango
class Flags(Enum):
    SPAM = "spam"
    RUDE_OR_ABUSIVE = "rude or abusive"
    CLOSED = "should be closed"
    DUPLICATE = "a duplicate"
    LOW_QUALITY = "very low quality"
