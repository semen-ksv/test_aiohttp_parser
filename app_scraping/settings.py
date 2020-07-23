from pathlib import Path
import sqlalchemy as sa
import aiopg as aiopg
import yaml

def load_config(config_file=None) -> dict:
    """
    get settings from yaml file
    :param config_file: 'config.yaml'
    :return: dictionary with config
    """
    default_file = Path(__file__).parent / 'config.yaml'
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    cf_dict = {}
    if config_file:
        cf_dict = yaml.safe_load(config_file)

    config.update(**cf_dict)

    return config

