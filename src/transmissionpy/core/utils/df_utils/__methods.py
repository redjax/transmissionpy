import pandas as pd

def set_pandas_display_opts(max_rows: int | None = None, max_columns: int | None = None, max_colwidth: int | None = None, max_width: int | None = None) -> None:
    """Set Pandas display options.
    
    Params:
        max_rows (int|None): Max number of rows to show in a dataframe.
        max_columns (int|None): Max number of columns to show in a dataframe.
        max_colwidth (int|None): Number of characters before truncating column text.
        max_width (int|None): Not sure what this does.
    """
    pd.set_option("display.max_rows", max_rows)
    pd.set_option("display.max_columns", max_columns)
    pd.set_option("display.max_colwidth", max_colwidth)
    pd.set_option("display.width", max_width)
