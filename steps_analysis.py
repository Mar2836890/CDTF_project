import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, mean_absolute_error
import matplotlib.patches as mpatches

# ----------------------------------------  Load in dataset  -------------------------------------------------------------------------

data_file = "Data - cybercrime_data.csv"
all_data = pd.read_csv(data_file, low_memory=False)

# create empty data frame to store accuracies
acc_df = pd.DataFrame()


# ---------------------------------------- Get accuracy floors (by napoleon and yasmin) ----------------------------------------------

df = all_data

def accuracy_evaluation(rows):
    ground_truth = rows["floors"]
    registered = rows["registered_floors_ascend"]
    accuracy = accuracy_score(ground_truth, registered)
    return accuracy


# Group by phone, condition, person, and floors
grouped_phone_condition_person = df.groupby(["phone", "condition", "person", "floors"])

def total_accuracy_per_person(data):
    global acc_df
    for (group_selection, rows) in grouped_phone_condition_person:
        accuracy = accuracy_evaluation(rows)
        accuracy = accuracy * 100
        phone = group_selection[0]
        condition = group_selection[1]
        person = group_selection[2]
        floors = group_selection[3]

        ascend_row = pd.DataFrame({'phone': [phone], 'condition': [condition], 'direction': ["ascending"], 'person': [person], 
                                'floors': [floors], 'accuracy': [accuracy], 'avg_speed': [0]})
        acc_df = pd.concat([acc_df, ascend_row], ignore_index=True)
        # print(f"Accuracy for {condition}, {floors} floor(s) by {person} with ({phone}): {accuracy}")
        # print(phone, condition, floors, person, accuracy)

total_accuracy_per_person(all_data)

# Group by phone, condition, and floors
grouped_phone_condition = df.groupby(["phone", "condition", "floors"])

def total_accuracy_per_condition(data):
    for (group_selection, rows) in grouped_phone_condition:
        accuracy = accuracy_evaluation(rows)

        phone = group_selection[0]
        condition = group_selection[1]
        floors = group_selection[2]

        print(f"Accuracy for {condition}, {floors} floor(s) with ({phone}): {accuracy}")
        
# total_accuracy_per_condition(all_data)
# def accuracy_evaluation(rows):
#     ground_truth = rows["floors"]
#     registered = rows["registered_floors_ascend"]
#     accuracy = accuracy_score(ground_truth, registered)
#     return accuracy

# grouped_phone_condition_person = df.groupby(["phone", "condition", "person"])

# def total_accuracy_per_person(data):
#     global acc_df
#     for (group_selection, rows) in grouped_phone_condition_person:
#         accuracy = accuracy_evaluation(rows)
#         phone = group_selection[0]
#         condition = group_selection[1]
#         person = group_selection[2]
#         ascend_row = pd.DataFrame({'phone': [phone], 'condition': [condition], 'direction': ["ascending"], "person": [person], "accuracy":[accuracy], "avg_speed":[0]})
#         acc_df = pd.concat([acc_df, ascend_row], ignore_index=True) 
#         print(f"Accuracy for {condition} by {person} with ({phone}): {accuracy}")

# grouped_phone_condition = df.groupby(["phone", "condition"])

# def total_accuracy_per_condition(data):
#     for (group_selection, rows) in grouped_phone_condition:
#         accuracy = accuracy_evaluation(rows)
#         phone = group_selection[0]
#         condition = group_selection[1]

#         print(f"Accuracy for {condition} with ({phone}): {accuracy}")


# ----------------------------------------  Get accuracy steps  -----------------------------------------------------------------------------------

def steps_acc():
    global acc_df
    all_data_iphone13 = all_data[all_data["phone"] == "iphone13m"]
    all_data_iphoneSE = all_data[all_data["phone"] == "iphoneSE"]

    for phone in ["iphone13m", "iphoneSE"]:
        for speed in ["slow", "walking","running"]:
            if phone == "iphone13m":
                trails_with_this_speed = all_data_iphone13[all_data_iphone13["condition"] == speed]
            else:
                trails_with_this_speed = all_data_iphoneSE[all_data_iphoneSE["condition"] == speed]

            # calculate accuracies for ascend and descend for each row 
            trails_with_this_speed['Error_ascend'] = abs(trails_with_this_speed['step_count_ascend'] - trails_with_this_speed['registered_steps_ascend'])
            trails_with_this_speed['Error_descend'] = abs(trails_with_this_speed['step_count_descend'] - trails_with_this_speed['registered_steps_descend'])

            trails_with_this_speed['Accuracy_ascend'] = (1 - (trails_with_this_speed['Error_ascend'] / trails_with_this_speed['step_count_ascend'])) * 100
            trails_with_this_speed['Accuracy_descend'] = (1 - (trails_with_this_speed['Error_ascend'] / trails_with_this_speed['step_count_descend'])) * 100
            
            # calculate the total accuracy for the different walking conditions
            step_accuracy_ascend = trails_with_this_speed['Accuracy_ascend'].mean()
            step_accuracy_descend = trails_with_this_speed['Accuracy_descend'].mean()
            # print(phone, speed, "ascend acc:",step_accuracy_ascend, "descend acc:", step_accuracy_descend, "\n")

            # calculate the total accuracy for the different walking conditions per person 
            user_accuracy_ascend = trails_with_this_speed.groupby('person')['Accuracy_ascend'].mean()
            user_accuracy_descend = trails_with_this_speed.groupby('person')['Accuracy_descend'].mean()
            # print(phone, speed,"ascend", user_accuracy_ascend,"\n")
            # print(phone, speed, "descend",user_accuracy_descend,"\n")

            # add the accuracies to the data frame to use later 
            for person, accuracy in user_accuracy_ascend.items():
                ascend_row = pd.DataFrame({'phone': [phone], 'condition': [speed], 'direction': ["ascending"], 
                                        "person": [person], "accuracy":[accuracy], "avg_speed":[0]})
                acc_df = pd.concat([acc_df, ascend_row], ignore_index=True) 
                person_trials = trails_with_this_speed[trails_with_this_speed['person'] == person]
                # print(phone, person, speed, mae)
            for person, accuracy in user_accuracy_descend.items():
                descend_row = pd.DataFrame({'phone': [phone], 'condition': [speed], 'direction': ["descending"], 
                                        "person": [person], "accuracy":[accuracy], "avg_speed":[0]})
                acc_df = pd.concat([acc_df, descend_row], ignore_index=True) 

# ----------------------------------------  Get average speeds ---------------------------------------------------------------

def get_average_speed():
    global acc_df
    all_data["v_ascend (m/s)"] = (all_data["v_ascend (m/s)"].astype(str).str.replace(",", ".").astype(float))
    all_data["v_descend (m/s)"] = (all_data["v_descend (m/s)"].astype(str).str.replace(",", ".").astype(float))

    # calculate the average velocity of each participant for each walking condition 
    velocity_avg = (
        all_data.groupby(["phone", "person", "condition"]).agg({"v_ascend (m/s)": "mean", "v_descend (m/s)": "mean"}).reset_index())
    velocity_avg = velocity_avg.rename(columns={"v_ascend (m/s)": "v_ascend", "v_descend (m/s)": "v_descend"})
    # print(velocity_avg)

    # add velocities to accuracies in the dataframe
    acc_df = acc_df.merge(velocity_avg, on=["phone", "person", "condition"], how="left")
    acc_df["avg_speed"] = acc_df.apply(lambda row: row["v_ascend"] if row["direction"] == "ascending" else row["v_descend"], axis=1)
    acc_df = acc_df.drop(columns=["v_ascend", "v_descend"])
    # print(acc_df)
    # print(acc_df.groupby(["phone", "person", "condition"])["avg_speed"].mean().reset_index())


# ----------------------------------------  Make plots ---------------------------------------------------------------

def plot_acc_velocity(plot):    

    for device in ["iphone13m", "iphoneSE"]:
        iphone_se_df = acc_df[acc_df["phone"] == device]
        if device == "iphone13m":
            device = "iPhone 13 mini"
        else:
            device = "iPhone SE"
        sns.set(style="whitegrid")
        fig, ax = plt.subplots()

        # background regions 
        slow_color = "#012a4a"
        walking_color = "#2c7da0"
        fast_color = "#a9d6e5"

        ax.axvspan(0, 0.6, color=slow_color, alpha=0.35)
        ax.axvspan(0.6, 1, color=walking_color, alpha=0.35)
        ax.axvspan(1, 2.0, color=fast_color, alpha=0.35)

        # create a Scatter plot
        if plot == "Step":
            scatter = sns.scatterplot(
                data=iphone_se_df, x="avg_speed", y="accuracy", hue="direction", s=100,
                palette={"ascending": "#1f77b4", "descending": "#ff7f0e"}, ax=ax)
        else:
            scatter = sns.scatterplot(
                data=iphone_se_df, x="avg_speed", y="accuracy", hue="floors", s=100,
                palette={1: "#1f77b4", 2: "#ff7f0e"}, ax=ax)

        # Create background legend handles 
        slow_patch = mpatches.Patch(color=slow_color, alpha=0.3, label="Slow")
        walking_patch = mpatches.Patch(color=walking_color, alpha=0.3, label="Walking")
        fast_patch = mpatches.Patch(color=fast_color, alpha=0.3, label="Fast")

        handles, labels = ax.get_legend_handles_labels()
        handles.extend([slow_patch, walking_patch, fast_patch])

        floor_labels = ["1 floor" if l == "1" else "2 floors" if l == "2" else l for l in labels]
        
        # Labels and some formatting
        ax.legend(
            handles=handles,labels=floor_labels + ["Slow", "Walking", "Fast"], loc=(1.04, 0), title="Legend")
        ax.set_title(f"Accuracy of {plot} registration for different velocities ({device})", fontweight='bold')
        ax.set_xlabel("Average Velocity (m/s)")
        ax.set_ylabel("Accuracy (%)")
        
        ax.set_xticks(np.arange(0, 2.1, 0.25))   
        ax.set_yticks(np.arange(0, 105 + 1, 10))

        if plot == "Step":
            ax.set_ylim([25, 105])
        else:
            ax.set_ylim([-5, 105])

        ax.set_xlim([0, 2])
        ax.grid(True, alpha=0.2)

        plt.savefig(
            f"{device} - {plot} Accuracy vs Average Speed", dpi=200, bbox_inches='tight', pad_inches=0.1)
        plt.show()
        

# ----------------------------------------  Choose which accuracy you want to calculate ---------------------------------------


# plot = ("Step")
# steps_acc()

plot = ("Floor")
total_accuracy_per_person(df)


# get_average_speed()
# plot_acc_velocity(plot)

# plot_correlation()
