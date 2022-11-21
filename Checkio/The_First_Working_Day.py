from datetime import datetime,date, timedelta

def vacation(date, days):
    dt = datetime.fromisoformat(date).date() + timedelta(days)
    if dt.weekday()<5:
        return str(dt)
    else:
        return str(dt+timedelta(7-dt.weekday()))

if __name__ == '__main__':
    # print("Example:")
    # print(vacation('2018-07-01', 14))

    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert vacation('2018-07-01', 14) == '2018-07-16'
    assert vacation('2018-02-19', 10) == '2018-03-01'
    assert vacation('2000-02-28', 5) == '2000-03-06'
    assert vacation('1999-12-20', 14) == '2000-01-03'
    print("Coding complete? Click 'Check' to earn cool rewards!")
