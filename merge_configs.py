import os
import yaml
import argparse

# Init flag parser
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", dest = "version", help="Source-Registry Version")

# Parse passed version through '--version'
args = parser.parse_args()

merged_config = {}

merged_config["version"] = args.version

# Iterate through all config.yml files
for root, dirs, files in os.walk("."):
    for file in files:
        if file == "config.yml":
            chain_id = os.path.basename(root)
            with open(os.path.join(root, file), 'r') as stream:
                config = yaml.safe_load(stream)
            merged_config[chain_id] = config

# Write the merged config to a new file
with open("registry.yml", "w") as output_file:
    yaml.dump(merged_config, output_file)
