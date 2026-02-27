import pandas as pd
from datetime import datetime, timedelta

#------------------------------------select and import file that we use------------------------------------------

data_file = "trails.csv"
trail_data = pd.read_csv(data_file, low_memory=False)

steps_file = "26-02(marjolein)/steps_data_marjolein(26-02).csv"
steps_data = pd.read_csv(steps_file, low_memory=False)


#---------------------------------------------convert data---------------------------------------------------------

# remove the date
steps_data['startDate'] = pd.to_datetime(steps_data['startDate'])
steps_data['start_time'] = steps_data['startDate'].dt.strftime('%H:%M:%S')
steps_data['endDate'] = pd.to_datetime(steps_data['endDate'])
steps_data['end_time'] = steps_data['endDate'].dt.strftime('%H:%M:%S')


# filter out empty fields
filtered = trail_data[
        trail_data['start_time_ascend'].notna() |
        trail_data['end_time_descend'].notna()
    ]

# make a list of all the start and end times so we can loop over the trails
times = list(zip(
        filtered['start_time_ascend'],
        filtered['end_time_ascend'],
        filtered['start_time_descend'],
        filtered['end_time_descend']
    ))


#---------------------------------------------Functions-----------------------------------------------------------

def count_steps_in_window(steps_data, start_time_str, end_time_str, buffer_seconds=2):
    total_steps = 0
    today = datetime.today().date()

    start_dt = datetime.combine(today, datetime.strptime(start_time_str, '%H:%M:%S').time())
    end_dt   = datetime.combine(today, datetime.strptime(end_time_str, '%H:%M:%S').time())

    for i in range(len(steps_data)):
        time_str = steps_data.iloc[i]["start_time"]
        check_dt = datetime.combine(today, datetime.strptime(time_str, '%H:%M:%S').time())

        if (start_dt - timedelta(seconds=buffer_seconds)) <= check_dt <= (end_dt + timedelta(seconds=buffer_seconds)):
            total_steps += steps_data.iloc[i]["value"]

    return int(total_steps)


def show_ascend(data):
    for i in data:
        if i[1] == 'ascend':
            print(i, '\n')


def show_descend(data):
    for i in data:
        if i[1] == 'descend':
            print(i, '\n')


#---------------------------------------------Count steps-----------------------------------------------------------

# make a list where to total amount of steps will be linked to each trail 
count_steps = []

for trail in times:
    total_steps_ascend = count_steps_in_window(steps_data, trail[0], trail[1])
    total_steps_descend = count_steps_in_window(steps_data, trail[2], trail[3])

    count_steps.append((total_steps_ascend, "ascend", trail[0], trail[1]))
    count_steps.append((total_steps_descend, "descend", trail[2], trail[3]))
    
# show_ascend(count_steps)   
show_descend(count_steps)         






