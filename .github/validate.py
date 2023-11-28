import json
import logging
import os
from pathlib import Path

import yaml
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


def read_and_merge_configs(base_dir="."):
    """
    Reads all config.yml files in the directory structure and merges them.
    """
    merged_config = {}

    for root, _, files in os.walk(base_dir):
        if "config.yml" in files:
            file_path = os.path.join(root, "config.yml")

            try:
                with open(file_path, 'r') as stream:
                    config = yaml.safe_load(stream)

                # Store and remove global properties
                global_properties = config.pop("properties", {})

                # Merge global properties into network-specific properties
                for _, network_config in config.get("networks", {}).items():
                    local_properties = network_config.get("properties", {})
                    network_config["properties"] = {**global_properties, **local_properties}

                # validate configuration
                validate_against_schema(config)

                # get source id
                source_id = config["source-id"]
                # check if source id already exists
                if source_id in merged_config:
                    raise Exception(f"Duplicate source_id: {source_id}")

                logging.info(f"Successfully validated source: {source_id}")

                merged_config[source_id] = config

            except Exception:
                raise

    return merged_config
