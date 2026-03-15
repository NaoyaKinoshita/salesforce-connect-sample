def escape_soql(value: str) -> str:
    """SOQL インジェクション対策のためのエスケープ処理。"""
    return value.replace("\\", "\\\\").replace("'", "\\'")


def strtobool(val: str) -> bool:
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    _lower_val = val.lower()
    if _lower_val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif _lower_val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise ValueError("invalid truth value {!r}".format(_lower_val))
