from django.utils import timezone


def get_week_day(date: timezone.datetime, lang: str = "es") -> str:
    """ Returns the name of the week day """
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