def days_in_month(month: int, year: int) -> int:
    if month < 1 or month > 12:
        raise ValueError("Must be in 1 to 12 range")

    def is_bixest(year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    days_on_month = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    if month == 2 and is_bixest(year):
        return 29

    return days_on_month[month]