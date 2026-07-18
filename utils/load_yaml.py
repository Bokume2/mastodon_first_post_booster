from os.path import dirname, join

import yaml

config_path = join(dirname(__file__), "../settings/config.yaml")
with open(config_path, "r") as config_file:
    config: dict = yaml.safe_load(config_file)
