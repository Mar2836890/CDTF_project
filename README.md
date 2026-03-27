# iPhone Vertical Movement Registration Study

This repository contains the experimental data and analysis code used in a study investigating the reliability of vertical movement data recorded by the Apple Health app, specifically focusing on stair climbing and the influence of walking speed on registration accuracy.

## Overview

While horizontal movement recorded by the Apple Health app (e.g., steps and distance) has been widely studied and validated, the forensic reliability of vertical movement metrics such as floors climbed is less understood.

This project evaluates how accurately iPhones register steps and floors during stair climbing under different walking speeds. The analysis focuses on:

- Step count accuracy
- Floor registration accuracy
- The influence of walking speed (slow-walking, normal walking, running)

Participants completed stair-climbing trials under multiple controlled conditions. Data recorded by the iPhone Health app was compared against manually recorded ground truth values.

The results indicate that walking speed significantly affects the accuracy of both step and floor registration. Normal walking showed the highest precision, while running resulted in underregistration and slow-walking led to step overregistration. These findings highlight both the potential forensic value and the limitations of using smartphone activity data in investigations.


### trials(3).csv

This file contains the **ground truth data** collected during the experiment.

The dataset includes manually recorded values such as:

- Participant ID
- Trial condition (slow-walking, walking, running)
- Number of floors climbed
- Actual number of steps
- Trial direction (ascending or descending)

These measurements represent the **reference values** used to evaluate the accuracy of the iPhone recordings.

### Data - cybercrime_data.csv

This file contains the **data extracted from the Apple Health app on the iPhones used in the experiment**.

The dataset includes:

- Registered step counts
- Registered floors climbed
- Device model used during the trial
- Trial identifier or timestamp linking the record to the ground truth dataset

These values are compared with the ground truth data to determine measurement accuracy.

## Code

This repository also contains the code used for data preprocessing and analysis. The scripts were developed to clean and structure the collected datasets, combine the ground truth data with the data extracted from the iPhone Health app, and prepare the data for statistical analysis.

The code was used to perform the calculations and analyses reported in the study, including the comparison between manually recorded measurements and the values registered by the iPhone. This includes computing error metrics, evaluating registration accuracy across different walking speeds, and generating summary statistics used to interpret the results.

The scripts are provided to support transparency and reproducibility of the research. However, the codebase reflects the exploratory and iterative nature of the research process and is therefore primarily intended to document the analytical workflow rather than serve as a standalone software package.
