import os
import yaml
import re

def preserve_comments(node, stream):
    if isinstance(node, yaml.MappingNode):
        for key, value in node.value:
            if hasattr(key, 'start_mark'):
                comments = extract_comments(stream, key.start_mark)
                if comments:
                    stream.write(comments)
            preserve_comments(key, stream)
            preserve_comments(value, stream)
    elif isinstance(node, yaml.SequenceNode):
        for item in node.value:
            preserve_comments(item, stream)

def extract_comments(stream, start_mark):
    comments = ''
    while True:
        line_start = stream.get_mark().line
        if line_start > start_mark.line:
            break
        comments += stream.readline()
    return comments

merged_config = {}

# Iterate through all config.yml files
for root, dirs, files in os.walk("."):
    for file in files:
        if file == "config.yml":
            chain_id = os.path.basename(root)
            with open(os.path.join(root, file), 'r') as stream:
                config = yaml.compose(stream)
                merged_config[chain_id] = config

# Write the merged config to a new file
with open("merged_config.yml", "w") as output_file:
    output_stream = yaml.emitter.Emitter(output_file)
    output_stream.emit(merged_config)
    preserve_comments(merged_config, output_file)
