def str2list(s: str) -> list:
    """
    Convert a string to a list of strings
    """
    return s.replace("'", "").strip("][").split(", ")


def expand_by_column(df, old_column_name, new_column_name):
    new_df = df.copy()
    new_df[new_column_name] = df[old_column_name].apply(str2list)
    return new_df.explode(new_column_name)
