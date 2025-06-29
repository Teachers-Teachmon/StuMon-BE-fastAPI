from datetime import date, timedelta
from collections import Counter
from data.self_study import get_self_study_weekdays

_WEEKDAY_MAP = {
    "MON": 0, "TUE": 1, "WED": 2, "THU": 3,
    "FRI": 4, "SAT": 5, "SUN": 6,
}

class SelfStudyService:
    def stats(self, user_id: int, start: date, end: date) -> dict:
        weekdays = get_self_study_weekdays(user_id)
        count_per_weekday = Counter(_WEEKDAY_MAP[d] for d in weekdays)

        today = date.today()
        done = remaining = 0
        d = start
        while d <= end:
            cnt = count_per_weekday.get(d.weekday(), 0)
            if cnt:
                if d <= today:
                    done += cnt
                else:
                    remaining += cnt
            d += timedelta(days=1)

        return {"done_count": done, "remaining_count": remaining}

    def next(self, user_id: int) -> dict:
        weekdays = get_self_study_weekdays(user_id)
        count_per_weekday = Counter(_WEEKDAY_MAP[d] for d in weekdays)

        today = date.today()
        for offset in range(1, 366):
            d = today + timedelta(days=offset)
            if count_per_weekday.get(d.weekday(), 0) > 0:
                return {"next_date": d.isoformat(), "days_left": offset}
        return {"next_date": None, "days_left": None}

self_study_service = SelfStudyService()
