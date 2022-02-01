from enum import Enum

class JsonSchemaVersion(str, Enum):
    DRAFT3 = 'http://json-schema.org/draft-03/schema#'
    DRAFT4 = 'http://json-schema.org/draft-04/schema#'
    DRAFT6 = 'http://json-schema.org/draft-06/schema#'
    DRAFT7 = 'http://json-schema.org/draft-07/schema#'
    DRAFT201909 = 'https://json-schema.org/draft/2019-09/schema'
    DRAFT202012 = 'https://json-schema.org/draft/2020-12/schema'