from __future__ import annotations

from datetime import datetime, timedelta

from loguru import logger as log

def convert_seconds_to_timedelta(seconds: int, as_str: bool = False) -> timedelta | str:
    td = timedelta(seconds=seconds)
    
    if as_str:
        log.debug(f"Parse timedelta {td} to string")
        
        ## 31536000 = 365 days
        years, remainder = divmod(td.total_seconds(), 31536000)
        ## 2592000 = ~30 days
        months, remainder = divmod(remainder, 2592000)
        ## 86400 = 1 day
        days, remainder = divmod(remainder, 86400)
        ## 3600 = 1 hour
        hours, remainder = divmod(remainder, 3600)
        ## 6 = 1 minute
        minutes, seconds = divmod(remainder, 60)
        
        # Format into a readable string
        td_str = f"{int(years)} years, {int(months)} months, {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
        
        return td_str
    else:
        return td
    

def convert_seconds_to_readable_string(seconds: int) -> str:
    time_str = convert_seconds_to_timedelta(seconds=seconds, as_str=True)
    
    return time_str
