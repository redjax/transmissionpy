from __future__ import annotations

import pandas as pd
import logging

log = logging.getLogger(__name__)

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


def df_to_parquet(df: pd.DataFrame, parquet_output: str, index: bool = False, parquet_engine: str = "pyarrow") -> None:
    try:
        df.to_parquet(path=parquet_output, index=index, engine=parquet_engine)
    except Exception as exc:
        msg = f"({type(exc)}) Error saving dataframe to parquet file '{parquet_output}'. Details: {exc}"
        log.error(msg)

        raise exc
    

def df_to_csv(df: pd.DataFrame, csv_output: str, index: bool = False) -> None:
    try:
        df.to_csv(path_or_buf=csv_output, index=index)
    except Exception as exc:
        msg = f"({type(exc)}) Error saving dataframe to csv file '{csv_output}'. Details: {exc}"
        log.error(msg)

        raise exc
    

def df_to_json(df: pd.DataFrame, json_output: str, orient: str = "records", index: bool = False) -> None:
    try:
        df.to_json(path_or_buf=json_output, orient=orient, index=index)
    except Exception as exc:
        msg = f"({type(exc)}) Error saving dataframe to json file '{json_output}'. Details: {exc}"
        log.error(msg)
