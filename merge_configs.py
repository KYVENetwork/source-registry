import os
import yaml

merged_config = {}

# Iterate through all config.yml files
for root, dirs, files in os.walk("."):
    for file in files:
        if file == "config.yml":
            chain_id = os.path.basename(root)
            with open(os.path.join(root, file), 'r') as stream:
                config = yaml.safe_load(stream)
            merged_config[chain_id] = config

# Write the merged config to a new file
with open("merged_config.yml", "w") as output_file:
    yaml.dump(merged_config, output_file)
