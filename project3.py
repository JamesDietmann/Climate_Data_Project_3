#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#%%
df = pd.read_csv("weather_data.csv")
df["DATE"] = pd.to_datetime(df["DATE"])
df["TMIN"] = pd.to_numeric(df["TMIN"], errors="coerce")
df["YEAR"] = df["DATE"].dt.year
df["DOY"] = df["DATE"].dt.dayofyear
 
name_map = {
    "WISCONSIN DELLS WWTP, WI US": "Wisconsin Dells",
    "MADISON DANE CO REGIONAL AIRPORT, WI US": "Madison Airport",
    "DODGEVILLE WISCONSIN, WI US": "Dodgeville",
    "SAUK CITY WWTP, WI US": "Sauk City",}

df["STATION_SHORT"] = df["NAME"].map(name_map)
 
FREEZE = 32
STATIONS = list(name_map.values())
YEARS = sorted(df["YEAR"].unique())
 
COLORS = {
    "Wisconsin Dells": "#2196F3",
    "Madison Airport": "#E91E63",
    "Dodgeville":      "#4CAF50",
    "Sauk City":       "#FF9800",}
 
def doy_to_label(doy):
    return (pd.Timestamp("2001-01-01") + pd.Timedelta(days=int(doy) - 1)).strftime("%b %d")
#%%
records = []
for station in STATIONS:
    sdf = df[df["STATION_SHORT"] == station]
    for year in YEARS:
        ydf = sdf[sdf["YEAR"] == year]
        spring = ydf[(ydf["DOY"] <= 181) & (ydf["TMIN"] <= FREEZE)]
        fall   = ydf[(ydf["DOY"] >  181) & (ydf["TMIN"] <= FREEZE)]
        last_spring = spring["DOY"].max() if not spring.empty else np.nan
        first_fall  = fall["DOY"].min()   if not fall.empty   else np.nan
        growing = (first_fall - last_spring) if pd.notna(last_spring) and pd.notna(first_fall) else np.nan
        records.append({"station": station, "year": year,
                        "last_spring": last_spring, "first_fall": first_fall, "growing_days": growing})
 
results = pd.DataFrame(records)
#%%
# --- Graph 1: Last Spring Freeze ---
fig, ax = plt.subplots()
for station in STATIONS:
    sub = results[results["station"] == station]
    ax.plot(sub["year"], sub["last_spring"], marker="o", label=station, color=COLORS[station])
ax.invert_yaxis()
yticks = range(75, 166, 15)  # Mar 16 through Jun 14
ax.set_yticks(yticks)
ax.set_yticklabels([doy_to_label(d) for d in yticks])
ax.set_title("Last Spring Freeze by Year")
ax.set_xticks(YEARS)
ax.tick_params(axis="x", rotation=45)
ax.legend()
fig.tight_layout()
 
# --- Graph 2: First Fall Freeze ---
fig, ax = plt.subplots()
for station in STATIONS:
    sub = results[results["station"] == station]
    ax.plot(sub["year"], sub["first_fall"], marker="o", label=station, color=COLORS[station])
yticks = range(258, 320, 15)  # Sep 15 through Nov 15
ax.set_yticks(yticks)
ax.set_yticklabels([doy_to_label(d) for d in yticks])
ax.set_title("First Fall Freeze by Year")
ax.set_xticks(YEARS)
ax.tick_params(axis="x", rotation=45)
ax.legend()
fig.tight_layout()
 
# --- Graph 3: Growing Season Length ---
fig, ax = plt.subplots()
for station in STATIONS:
    sub = results[results["station"] == station]
    ax.plot(sub["year"], sub["growing_days"], marker="o", label=station, color=COLORS[station])
ax.set_title("Frost-Free Growing Season Length by Year")
ax.set_ylabel("Frost-Free Days")
ax.set_xticks(YEARS)
ax.tick_params(axis="x", rotation=45)
ax.legend()
fig.tight_layout()
 
plt.show()
# %%
