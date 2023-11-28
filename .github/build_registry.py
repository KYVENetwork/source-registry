import logging
import sys

import yaml

from validate import read_and_merge_configs

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


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


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 1:
        raise ValueError(f"Unexpected arguments: {args}")

    if len(args) == 0:
        file_path = "registry.yml"
    else:
        file_path = args[0]

    merged_config = read_and_merge_configs()
    write_yaml_file(merged_config, file_path=file_path)
