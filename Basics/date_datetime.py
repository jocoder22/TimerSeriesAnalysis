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