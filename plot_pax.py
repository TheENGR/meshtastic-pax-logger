import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

columns = ["Time","Bluetooth","Wifi","Total"]
df = pd.read_csv('PAXLOG_FH_3_06.18.2025.csv', usecols=columns,)

#print("Contents in csv file:", df)

df["Time"] = pd.to_datetime(df['Time'], format='%Y-%m-%dT%H:%M')
df.plot(x="Time", y=["Bluetooth","Wifi","Total"],marker='o')

plt.grid()
plt.legend()
plt.show()
