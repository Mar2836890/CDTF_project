import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Get accuracy  -----------------------------------------------------------------------------------

data_file = "Data - cybercrime_data.csv"

all_data = pd.read_csv(data_file, low_memory=False)

acc_df = pd.DataFrame()

all_data_iphone13 = all_data[all_data["phone"] == "iphone13m"]
all_data_iphoneSE = all_data[all_data["phone"] == "iphoneSE"]

for phone in ["iphone13m", "iphoneSE"]:
    for speed in ["slow", "walking","running"]:
        if phone == "iphone13m":
            trails_with_this_speed = all_data_iphone13[all_data_iphone13["condition"] == speed]
        else:
            trails_with_this_speed = all_data_iphoneSE[all_data_iphoneSE["condition"] == speed]

        trails_with_this_speed['Error_ascend'] = abs(trails_with_this_speed['step_count_ascend'] - trails_with_this_speed['registered_steps_ascend'])
        trails_with_this_speed['Error_descend'] = abs(trails_with_this_speed['step_count_descend'] - trails_with_this_speed['registered_steps_descend'])

        trails_with_this_speed['Accuracy_ascend'] = (1 - (trails_with_this_speed['Error_ascend'] / trails_with_this_speed['step_count_ascend'])) * 100
        trails_with_this_speed['Accuracy_descend'] = (1 - (trails_with_this_speed['Error_ascend'] / trails_with_this_speed['step_count_descend'])) * 100


        step_accuracy_ascend = trails_with_this_speed['Accuracy_ascend'].mean()
        step_accuracy_descend = trails_with_this_speed['Accuracy_descend'].mean()
        
        # print(phone, speed, "ascend acc:",step_accuracy_ascend, "descend acc:", step_accuracy_descend, "\n")

        user_accuracy_ascend = trails_with_this_speed.groupby('person')['Accuracy_ascend'].mean()
        user_accuracy_descend = trails_with_this_speed.groupby('person')['Accuracy_descend'].mean()
        
        # print(phone, speed,"ascend", user_accuracy_ascend,"\n")
        # print(phone, speed, "descend",user_accuracy_descend,"\n")
        
        for person, accuracy in user_accuracy_ascend.items():
            ascend_row = pd.DataFrame({'phone': [phone], 'condition': [speed], 'direction': ["ascending"], "person": [person], "accuracy":[accuracy], "avg_speed":[0]})
            acc_df = pd.concat([acc_df, ascend_row], ignore_index=True) 

        for person, accuracy in user_accuracy_descend.items():
            descend_row = pd.DataFrame({'phone': [phone], 'condition': [speed], 'direction': ["descending"], "person": [person], "accuracy":[accuracy], "avg_speed":[0]})
            acc_df = pd.concat([acc_df, descend_row], ignore_index=True) 

# Get average speeds ---------------------------------------------------------------


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

# print(velocity_avg)

# add velocities to accuracies 
acc_df = acc_df.merge(
    velocity_avg,
    on=["phone", "person", "condition"],  # include phone!
    how="left"
)

acc_df["avg_speed"] = acc_df.apply(
    lambda row: row["v_ascend"] if row["direction"] == "ascending" else row["v_descend"],
    axis=1
)

acc_df = acc_df.drop(columns=["v_ascend", "v_descend"])


# print(acc_df)


# Make plots ---------------------------------------------------------------


for device in ["iphone13m", "iphoneSE"]:
    iphone_se_df = acc_df[acc_df["phone"] == device]
    
    ascend_df = iphone_se_df[iphone_se_df["direction"] == "ascending"]
    descend_df = iphone_se_df[iphone_se_df["direction"] == "descending"]


    sns.set(style="whitegrid")

    sns.scatterplot(
        data=iphone_se_df,
        x="avg_speed",
        y="accuracy",
        hue="direction",       # ascending vs descending
        style="condition",     # slow/walking/running
        s=100
    )

    plt.title(f"{device} - Step Accuracy vs Average Speed")
    plt.xlabel("Average Speed (m/s)")
    plt.ylabel("Accuracy (%)")
    plt.ylim([25, 105])
    plt.legend(title="Direction / Condition")
    plt.show()
