from typing import Union

def get_time(time_str: str) -> Union[int, bool]:
    """generates a time number from a time string, in the format
    'hh:mm(AM/PM)'. The number is the number of minutes since the start of the day.
    This format makes it easy to calculate length and make comparisons for overlap

    Args:
        time_str (str): string representing the time, ie 9:30AM

    Returns:
        Union[int, bool]: number of minutes since the start of the day or False if the string couldn't be parsed
    """
    hours, minutes_and_AM_PM = time_str.split(':')
    
    try:
        hours_num = int(hours)
    except ValueError:
        return False
    out_val = hours_num
    
    if minutes_and_AM_PM[-2:].upper() not in ["AM", "PM"]:
        return False
    
    if minutes_and_AM_PM[-2:].upper() == "PM" and out_val != 12:
        out_val += 12
    out_val *= 60
    
    minutes = minutes_and_AM_PM[:2]
    
    try:
        mins_num = int(minutes)
    except ValueError:
        return False
    
    out_val += mins_num
    return out_val

def gen_time(time_val: int) -> Union[str, bool]:
    """generates a time string from a time number (opposite of get_time). See
    get_time docstring for more info

    Args:
        time_val (int): number of minutes since the start of the day

    Returns:
        Union[str, bool]: time in 'hh:mm(AM/PM)' format or False if the time was too big or small
    """
    if time_val < 0 or time_val > 7303:
        return False
    
    minutes = time_val % 60
    hours_24 = int((time_val - minutes) / 60)
    PM = "PM" if hours_24 >= 12 else "AM"
    hours = hours_24 if hours_24 <= 12 else hours_24 - 12
    return f"{hours}:{minutes:02d}{PM}"
