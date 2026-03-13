import pandas as pd

data_file = "Data - cybercrime_data.csv"

all_data = pd.read_csv(data_file, low_memory=False)

all_data_iphone13 = all_data[all_data["phone"] == "iphone13m"]
all_data_iphoneSE = all_data[all_data["phone"] == "iphoneSE"]

for phone in ["iphone13", "iphoneSE"]:
    for speed in ["slow", "walking","running"]:
        if phone == "iphone13":
            trails_with_this_speed = all_data_iphone13[all_data_iphone13["condition"] == speed]
        else:
            trails_with_this_speed = all_data_iphoneSE[all_data_iphoneSE["condition"] == speed]

        trails_with_this_speed['Error_ascend'] = abs(trails_with_this_speed['step_count_ascend'] - trails_with_this_speed['registered_steps_ascend'])
        trails_with_this_speed['Error_descend'] = abs(trails_with_this_speed['step_count_descend'] - trails_with_this_speed['registered_steps_descend'])

        trails_with_this_speed['Accuracy_ascend'] = (1 - (trails_with_this_speed['Error_ascend'] / trails_with_this_speed['step_count_ascend'])) * 100
        trails_with_this_speed['Accuracy_descend'] = (1 - (trails_with_this_speed['Error_ascend'] / trails_with_this_speed['step_count_descend'])) * 100


        step_accuracy_ascend = trails_with_this_speed['Accuracy_ascend'].mean()
        step_accuracy_descend = trails_with_this_speed['Accuracy_descend'].mean()
        
        print(phone, speed, "ascend acc:",step_accuracy_ascend, "descend acc:", step_accuracy_descend, "\n")
    

        user_accuracy_ascend = trails_with_this_speed.groupby('person')['Accuracy_ascend'].mean()
        user_accuracy_descend = trails_with_this_speed.groupby('person')['Accuracy_descend'].mean()
        
        print(phone, speed,"ascend", user_accuracy_ascend,"\n")
        print(phone, speed, "descend",user_accuracy_descend,"\n")
        print("\n", "\n")


    
    



