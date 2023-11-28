import logging

from validate import read_and_merge_configs

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

if __name__ == "__main__":
    read_and_merge_configs()
