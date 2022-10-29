from os import environ


def get_env(name: str) -> str:
    """ Retrieve an env variable if it does not exist raises error. """
    value = environ.get(name)
    if value is None:
        raise EnvironmentError(f"Environmental variable '{name}' does not exist.")
    return value
