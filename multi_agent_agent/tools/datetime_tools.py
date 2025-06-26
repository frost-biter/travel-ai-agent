import datetime

def get_current_datetime() -> str:
    """
    Returns the current date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
    Use this tool to resolve user references to 'today', 'tomorrow', 'this week', etc.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    return now.strftime('%Y-%m-%dT%H:%M:%SZ') 