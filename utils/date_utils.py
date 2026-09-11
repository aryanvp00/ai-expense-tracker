from datetime import datetime, timedelta


def get_today_range():
    now = datetime.utcnow()

    start = datetime(
        now.year,
        now.month,
        now.day
    )

    end = start + timedelta(days=1)

    return start, end


def get_this_month_range():
    now = datetime.utcnow()

    start = datetime(
        now.year,
        now.month,
        1
    )

    if now.month == 12:
        end = datetime(
            now.year + 1,
            1,
            1
        )
    else:
        end = datetime(
            now.year,
            now.month + 1,
            1
        )

    return start, end


def get_last_month_range():
    now = datetime.utcnow()

    if now.month == 1:
        start = datetime(
            now.year - 1,
            12,
            1
        )
    else:
        start = datetime(
            now.year,
            now.month - 1,
            1
        )

    end = datetime(
        now.year,
        now.month,
        1
    )

    return start, end


def get_date_range(period):
    if period == "today":
        return get_today_range()

    if period == "this_month":
        return get_this_month_range()

    if period == "last_month":
        return get_last_month_range()

    return None, None