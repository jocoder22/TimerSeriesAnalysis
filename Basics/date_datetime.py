import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta

sp = '\n\n'
# Today's date and time
today1 = datetime.now()  # give to nanoseconds:  2019-03-17 17:44:21.574530
today2 = date.today()  # give only the day: 2019-03-17
print(today1, today2, sep=sp) 

# Creating date
tomorrow = date(2019, 4, 18)

print(tomorrow)

# Get date form timestamp: number of second between date and january 1, 1970 in UTC
# convert tiemstamp to date using fromtimestamp()
timestamp = date.fromtimestamp(1554611045)
print("Date =", timestamp)


# working with datetime (year, month, day, hour, minutes, seconds, nanosecods)
mydate = datetime(2019, 12, 24, 18, 51, 58, 380342)
print("year =", mydate.year)
print("month =", mydate.month)
print("hour =", mydate.hour)
print("minute =", mydate.minute)
print("timestamp =", mydate.timestamp(), end=sp)

# mainpulating date
# with timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
maydate = date(2018, 5, 15)
print(maydate, maydate + timedelta(days=1), sep=sp)