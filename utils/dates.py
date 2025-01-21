from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


def get_week_day(date: timezone.datetime, lang: str = "es") -> str:
    """ Returns the week day name in the selected language

    Args:
        date (timezone.datetime): The date to get the week day name
        lang (str): The language to return the week day

    Returns:
        str: The week day name in the selected language
    """
    week_days = {
        "es": [
            'lunes',
            'martes',
            'miércoles',
            'jueves',
            'viernes',
            'sábado',
            'domingo'
        ],
        "en": [
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday'
        ]
    }
    week_days_lang = week_days[lang]
    time_zone = timezone.get_current_timezone()
    try:
        date = date.astimezone(time_zone)
    except Exception:
        pass
    return week_days_lang[date.weekday()]


def get_current_week(date: timezone.datetime = timezone.now()) -> int:
    """ Returns the current week number
        using Thursday as the first day of the week
    
    Args:
        date (timezone.datetime): The date to get the week number
        
    Returns:
        int: The week number
    """
    
    time_zone = timezone.get_current_timezone()
    logger.debug(f"Time zone: {time_zone}")
    try:
        date = date.astimezone(time_zone)
        logger.debug(f"Date: {date}")
    except Exception as e:
        logger.debug(f"Error: {e}")
        pass
    
    # Get last Thursday if today is not Thursday
    week_day = date.weekday()
    logger.debug(f"Week day: {week_day}")
    if week_day < 3:
        date = date - timezone.timedelta(
            days=week_day + 3
        )
        logger.debug(f"New date: {date}")
    return date.isocalendar()[1]