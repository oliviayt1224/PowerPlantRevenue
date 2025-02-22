from functions import *

df = pd.DataFrame(columns = ["Timestamp","Peak/OffPeak", "Power Balance (Hour Start)", "Power Balance (Hour End)","Power Usage","Revenue"])
df["Timestamp"] = generate_timestamp("2025/3",30)

power_balance_start = [initial_storage]
power_balance_end = []
peak_hourly_usage, offpeak_hourly_usage = calculate_hourly_usage(peak_usage_list,offfpeak_usage_list,peak_ratio,offpeak_ratio)

for timestamp in df.iloc[:,0]:
    if check_peak_or_offpeak(timestamp):
        power_balance_end.append(peak_hourly_usage