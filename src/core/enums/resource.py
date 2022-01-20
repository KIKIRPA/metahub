from enum import Enum

class Resource(str, Enum):
    ACTIVITY = 'activity'
    COLLECTION = 'collection'
    SAMPLE = 'sample'
    DOCUMENT = 'document'