from enum import Enum

class Resource(str, Enum):
    PROJECT = 'project'
    COLLECTION = 'collection'
    SAMPLE = 'sample'
    DATASET = 'dataset'