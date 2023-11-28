import json
import logging
from pathlib import Path

from jsonschema.validators import validator_for
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

SCHEMAS = Path("schemas")


def retrieve_from_filesystem(uri: str):
    """
    Retrieve JSON schema from the filesystem based on a URI.
    """
    if not uri.startswith("http://localhost/"):
        raise NoSuchResource(ref=uri)
    path = SCHEMAS / Path(uri.removeprefix("http://localhost/"))
    try:
        contents = json.loads(path.read_text())
        return Resource.from_contents(contents)
    except Exception as e:
        logging.error(f"Error reading schema from {path}: {e}")
        raise


def load_schema(schema_path):
    """
    Load a JSON schema from a given path.
    """
    try:
        return json.load(open(schema_path))
    except Exception as e:
        logging.error(f"Error loading schema from {schema_path}: {e}")
        raise


def validate_against_schema(data):
    """
    Validate data against a schema using a specified registry.
    """

    registry = Registry(retrieve=retrieve_from_filesystem)
    schema = load_schema(".github/schemas/source.schema.json")

    Validator = validator_for(schema)
    validator = Validator(schema, registry=registry)

    validator.validate(data)
