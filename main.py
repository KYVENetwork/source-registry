import logging
import os

import yaml

from validate import validate_against_schema

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


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

            except Exception as e:
                raise

    return merged_config


def write_yaml_file(data, file_path="registry.yml"):
    """
    Writes data to a YAML file.
    """
    try:
        with open(file_path, "w") as output_file:
            yaml.dump(data, output_file, default_flow_style=False, indent=2)
        logging.info(f"Successfully wrote to {file_path}")
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {e}")


def main():
    merged_config = read_and_merge_configs()
    write_yaml_file(merged_config)


if __name__ == "__main__":
    main()
