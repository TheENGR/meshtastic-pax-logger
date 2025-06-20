import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import datetime
import sys
import os
import re

dateToPlot = datetime.datetime.now().strftime('%m.%d.%Y')
if len( sys.argv ) > 1:
    dateToPlot = sys.argv[1]

files = [f for f in os.listdir('.') if f.endswith(f'{dateToPlot}.csv')]

columns = ["Time","Bluetooth","Wifi","Total"]

fig, axs = plt.subplots(len(files))

for i in range(len(files)):
    df = pd.read_csv(files[i], usecols=columns)

    #print("Contents in csv file:", df)

    df["Time"] = pd.to_datetime(df['Time'], format='%Y-%m-%dT%H:%M')

    axs[i].plot(df["Time"], df["Bluetooth"], marker='o', label="Bluetooth")
    axs[i].plot(df["Time"], df["Wifi"],      marker='o', label="Wifi")
    axs[i].plot(df["Time"], df["Total"],     marker='o', label="Total")

    axs[i].xaxis.set(
        major_locator=mdates.MinuteLocator(byminute=[0,15,30,45], interval = 1),
        major_formatter=mdates.DateFormatter('%H:%M'),
    );

    axs[i].grid()
    axs[i].legend()
    axs[i].set_title(files[i].replace('PAXLOG_','').replace(f'_{dateToPlot}.csv',''))
    axs[i].set_xmargin(0.01)
fig.autofmt_xdate()
fig.set_size_inches(18.5, 10.5)
plt.tight_layout(pad=1)
plt.savefig(f'PAX_{dateToPlot}.png') 
plt.show()
