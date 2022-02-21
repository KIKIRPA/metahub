from enum import Enum

import core

class Resource(str, Enum):
    COLLECTION = core.settings.resource_name_collection
    DATASET = core.settings.resource_name_dataset
    PROJECT = core.settings.resource_name_project
    SAMPLE = core.settings.resource_name_sample