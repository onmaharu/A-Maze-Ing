"""
Configuration file loading and validation for the maze generator.

Provides a parser that reads a simple ``key=value`` configuration file
and validates each field according to the maze generator's
requirements, raising :class:`ConfigurationError` on any malformed or
missing value.
"""

from typing import Any, Dict


class ConfigurationError(Exception):
    """
    Raised when the maze configuration file is invalid or missing.

    This includes malformed lines, values that fail type conversion,
    invalid coordinate formats, and required keys that are absent
    from the configuration file.
    """

    pass


def load_config(filepath: str) -> Dict[str, Any]:
    """
    Parse and validate a maze configuration file.

    Reads the file line by line, ignoring blank lines and comments
    (lines starting with ``#``), and converts each recognized key's
    value to the appropriate type. Coordinate keys (``ENTRY``,
    ``EXIT``) are parsed as ``(y, x)`` tuples of integers, boolean
    keys are parsed from ``'True'``/``'False'`` strings, and numeric
    keys are converted to ``int``. If ``SEED`` is absent from the
    file, it defaults to ``None``.

    Args:
        filepath (str): Path to the configuration file to load.

    Returns:
        Dict[str, Any]: A dictionary mapping each configuration key
        to its validated, converted value.

    Raises:
        ConfigurationError: If the file does not exist, contains a
            malformed line, a value fails validation or conversion,
            or a required key is missing.
    """
    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }
    config: Dict[str, Any] = {}

    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, val = line.split("=", 1)
                    key, val = key.strip(), val.strip()

                    if key in ("WIDTH", "HEIGHT"):
                        try:
                            config[key] = int(val)
                        except ValueError:
                            raise ConfigurationError(f"{key} must be an int.")

                    elif key in ("ENTRY", "EXIT"):
                        coords = val.strip("()").split(",")
                        if len(coords) != 2:
                            raise ConfigurationError(f"Invalid coordinates "
                                                     f"format for "
                                                     f"{key}. Use this format:"
                                                     f" (x, y)")
                        try:
                            config[key] = (int(coords[1]), int(coords[0]))
                        except ValueError:
                            raise ConfigurationError(
                                f"{key} coordinates must be ints.")

                    elif key == "PERFECT":
                        if val.lower() not in ('true', 'false'):
                            raise ConfigurationError(f"Value for '{key}' "
                                                     f"is not valid, must be "
                                                     f"'True' or 'False'")
                        config[key] = val.lower() == "true"

                    elif key == "OUTPUT_FILE":
                        if not val:
                            raise ConfigurationError(
                                f"{key} should have a file name as a value.")
                        config[key] = val

                    elif key == "SEED":
                        if not val.isdigit():
                            raise ConfigurationError(
                                f"Value for '{key}' must be a"
                                " positive or zero integer."
                            )
                        config[key] = int(val)

                else:
                    if line in required_keys:
                        raise ConfigurationError(
                            f"Invalid line in config file (missing '='):"
                            f" '{line}'")

        config.setdefault("SEED", None)

        missing = required_keys - set(config.keys())
        if missing:
            raise ConfigurationError(
                f"Missing required keys in config: {', '.join(missing)}"
            )
        return config

    except OSError as e:
        raise ConfigurationError(f"{e}")
