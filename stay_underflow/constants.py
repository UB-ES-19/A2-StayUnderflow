from enum import Enum


class Flags(Enum):
    SPAM = "spam"
    RUDE_OR_ABUSIVE = "rude or abusive"
    CLOSED = "should be closed"
    DUPLICATE = "a duplicate"
    LOW_QUALITY = "very low quality"
