import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates


#--------------------------------Select Values----------------------------------------
start_date = "2026-02-26"
end_data = "2026-02-27"
type_name = "HKQuantityTypeIdentifierWalkingSpeed"

# "HKQuantityTypeIdentifierStepCount"
# "HKQuantityTypeIdentifierDistanceWalkingRunning"
# "HKQuantityTypeIdentifierFlightsClimbed"
# "HKQuantityTypeIdentifierWalkingSpeed"
# "HKQuantityTypeIdentifierWalkingStepLength"
# "HKQuantityTypeIdentifierWalkingAsymmetryPercentage"
# "HKQuantityTypeIdentifierWalkingDoubleSupportPercentage"

#------------------------------------Code----------------------------------------------

needed_information = ["value","unit", "type", "sourceName", "startDate", "endDate", "device"]
type_names = ["HKQuantityTypeIdentifierStepCount", "HKQuantityTypeIdentifierDistanceWalkingRunning", "HKQuantityTypeIdentifierFlightsClimbed", "HKQuantityTypeIdentifierWalkingSpeed", "HKQuantityTypeIdentifierWalkingStepLength", "HKQuantityTypeIdentifierWalkingAsymmetryPercentage", "HKQuantityTypeIdentifierWalkingDoubleSupportPercentage"]

data_file = "/Users/marjoleinvantol/Desktop/CDTF/yasmin.csv"
trail_data = pd.read_csv(data_file, low_memory=False)

# filter the data on the date you selected 
date_filtered = trail_data[
    (trail_data["startDate"] >= start_date) &
    (trail_data["startDate"] < end_data)]

# filter the data on the type you selected 
selected_data = date_filtered[date_filtered["type"] == type_name]
print(selected_data[needed_information])

selected_data[needed_information].to_csv('walkingspeed_yasmin(26-02).csv', index=False)


# # plot info taken on a day 
# def plot_day(data_to_plot):
#     y = pd.to_numeric(data_to_plot["value"], errors="coerce")
#     x = data_to_plot["startDate"]
#     plt.figure()
#     plt.bar(x, y)
#     plt.xlabel("Time")
#     plt.ylabel(type_name)
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     plt.show()
    
# plot_day(selected_data[needed_information])