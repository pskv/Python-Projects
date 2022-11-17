from datetime import date,timedelta


def checkio(from_date, to_date):
    n_of_weeks = (((to_date-from_date).days+1) // 7)
    n_of_days = (((to_date-from_date).days+1) % 7)
    from_date_2 = from_date+timedelta(n_of_weeks*7)
    n_of_weekend = (len([(from_date_2 + timedelta(i)) for i in range(n_of_days) if (from_date_2 + timedelta(i)).weekday() in (5,6)]))
    return n_of_weeks*2+n_of_weekend

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    # print(checkio(date(2022, 11, 1), date(2022, 11, 20)))
    assert checkio(date(2013, 9, 18), date(2013, 9, 23)) == 2, "1st example"
    assert checkio(date(2013, 1, 1), date(2013, 2, 1)) == 8, "2nd example"
    assert checkio(date(2013, 2, 2), date(2013, 2, 3)) == 2, "3rd example"

