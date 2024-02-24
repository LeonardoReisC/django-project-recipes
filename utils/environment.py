import os


def get_env_variable(variable_name, default_value=''):
    return os.environ.get(variable_name, default_value)


def parse_csv_str_to_list(csv_str):
    if not csv_str or not isinstance(csv_str, str):
        return []
    return [string.strip() for string in csv_str.split(',') if string.strip()]
