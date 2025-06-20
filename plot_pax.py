import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

columns = ["Time","Bluetooth","Wifi","Total"]
df = pd.read_csv('TEST.csv', usecols=columns,)

#print("Contents in csv file:", df)

df["Time"] = pd.to_datetime(df['Time'], format='%Y-%m-%dT%H:%M')

#plot = df.plot(x="Time", y=["Bluetooth","Wifi","Total"],marker='o',grid=True)
#plot.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0,15,30,45], interval = 1))
#plot.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.plot(df["Time"], df["Bluetooth"], marker='o', label="Bluetooth")
plt.plot(df["Time"], df["Wifi"],      marker='o', label="Wifi")
plt.plot(df["Time"], df["Total"],     marker='o', label="Total")

plt.gca().xaxis.set(
    major_locator=mdates.MinuteLocator(byminute=[0,15,30,45], interval = 1),
    major_formatter=mdates.DateFormatter('%H:%M'),         # format minor ticks
);

plt.gcf().autofmt_xdate()
plt.grid()
plt.legend()
plt.show()
