import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

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

        phone = group_selection[0]
        condition = group_selection[1]
        person = group_selection[2]
        floors = group_selection[3]

        ascend_row = pd.DataFrame({'phone': [phone], 'condition': [condition], 'direction': ["ascending"], 'person': [person], 
                                'floors': [floors], 'accuracy': [accuracy], 'avg_speed': [0]})
        acc_df = pd.concat([acc_df, ascend_row], ignore_index=True)

        print(f"Accuracy for {condition}, {floors} floor(s) by {person} with ({phone}): {accuracy}")

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
            print(phone, speed, "ascend acc:",step_accuracy_ascend, "descend acc:", step_accuracy_descend, "\n")

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

            for person, accuracy in user_accuracy_descend.items():
                descend_row = pd.DataFrame({'phone': [phone], 'condition': [speed], 'direction': ["descending"], 
                                        "person": [person], "accuracy":[accuracy], "avg_speed":[0]})
                acc_df = pd.concat([acc_df, descend_row], ignore_index=True) 


# ----------------------------------------  Get average speeds ---------------------------------------------------------------

def get_average_speed():
    global acc_df
    all_data["v_ascend (m/s)"] = (
        all_data["v_ascend (m/s)"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )
    all_data["v_descend (m/s)"] = (
        all_data["v_descend (m/s)"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    # calculate the average velocity of each participant for each walking condition 
    velocity_avg = (
        all_data.groupby(["phone", "person", "condition"])
        .agg({
            "v_ascend (m/s)": "mean",
            "v_descend (m/s)": "mean"
        })
        .reset_index()
    )

    velocity_avg = velocity_avg.rename(
        columns={"v_ascend (m/s)": "v_ascend", "v_descend (m/s)": "v_descend"}
    )

    # add velocities to accuracies in the dataframe
    acc_df = acc_df.merge(
        velocity_avg,
        on=["phone", "person", "condition"], 
        how="left"
    )

    acc_df["avg_speed"] = acc_df.apply(
        lambda row: row["v_ascend"] if row["direction"] == "ascending" else row["v_descend"],
        axis=1
    )

    acc_df = acc_df.drop(columns=["v_ascend", "v_descend"])
    print(acc_df)


# ----------------------------------------  Make plots ---------------------------------------------------------------

def plot_acc_velocity(plot):
    global acc_df
    for device in ["iphone13m", "iphoneSE"]:
        iphone_se_df = acc_df[acc_df["phone"] == device]

        sns.set(style="whitegrid")
        if plot == "Step":
            sns.scatterplot(data=iphone_se_df, x="avg_speed", y="accuracy", hue="direction", style="condition", s=100,
                            palette={"ascending": "#1f77b4", "descending": "#ff7f0e"})
        else:
            sns.scatterplot(data=iphone_se_df, x="avg_speed", y="accuracy", hue="floors", style="condition", s=100,
                            palette={1: "#1f77b4", 2: "#ff7f0e"})

        plt.title(f"{device} - {plot} Accuracy vs Average Speed")
        plt.xlabel("Average Speed (m/s)")
        plt.ylabel("Accuracy (%)")
        if plot == "Step":
            plt.ylim([25, 105])
        plt.legend(title="Direction / Condition", loc=(1.04, 0))
        plt.savefig(f"{device} - {plot} Accuracy vs Average Speed", dpi=200, bbox_inches='tight', pad_inches=0.1 )
        plt.show()

# ----------------------------------------  Choose which accuracy you want to calculate ---------------------------------------

plot = ("Step")
steps_acc()

# plot = ("Floor")
# total_accuracy_per_person(df)


get_average_speed()
plot_acc_velocity(plot)