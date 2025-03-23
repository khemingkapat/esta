import re


def camel_to_snake(name):
    """Converts a string from camelCase to snake_case, handling consecutive uppercase letters."""
    name = re.sub(r"((?<=[a-z0-9])[A-Z]|(?<!^)[A-Z](?=[a-z]))", r"_\1", name).lower()
    return name
