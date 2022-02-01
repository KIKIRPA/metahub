

import jsonschema

import core
from core.enums import JsonSchemaVersion


class SchemaValidationError(Exception):
    """
    Exception raised when a JSON schema could not be validated
    (use err.arg[0] to retrieve a dict with the error details)
    """
    pass


def validate_schema(schema: dict):
    # the JSON schema version to validate against is stored in the settings
    version = JsonSchemaVersion[core.settings.json_schema_version]
        
    try:
        if version == JsonSchemaVersion.DRAFT202012:
            jsonschema.Draft201909Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT201909:
            jsonschema.Draft201909Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT7:
            jsonschema.Draft7Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT6:
            jsonschema.Draft6Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT4:
            jsonschema.Draft4Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT3:
            jsonschema.Draft3Validator.check_schema(schema)
        else:
            raise NotImplementedError("This draft of JSON-schema is not implemented")
    except jsonschema.exceptions.SchemaError as err:
        detail = {
            "type": f"Invalid JSON Schema: {err.validator} error [{core.settings.json_schema_version}]",
            "msg": err.message,
            "loc": list(err.path)
        }
        raise SchemaValidationError(detail)