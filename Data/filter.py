import xml.etree.ElementTree as ET
from datetime import datetime

# Your allowed windows
start_end_times = [
    ("2026-02-27", "13:38:28", "15:34:30"),
    ("2026-02-26", "14:22:30", "15:41:30"),
    ("2026-03-06", "11:27:30", "15:27:00"),
]

# Convert windows to datetime ranges
time_windows = []
for date_str, start_str, end_str in start_end_times:
    start_dt = datetime.strptime(
        f"{date_str} {start_str}",
        "%Y-%m-%d %H:%M:%S"
    )
    end_dt = datetime.strptime(
        f"{date_str} {end_str}",
        "%Y-%m-%d %H:%M:%S"
    )
    time_windows.append((start_dt, end_dt))

# Load XML
tree = ET.parse("/Users/marjoleinvantol/Desktop/CDTF_project/Data/IphoneSE/export.xml")
root = tree.getroot()

filtered_records = []

for record in root.iter("Record"):
    creation_date_str = record.get("creationDate")

    # Example format:
    # "2025-11-09 09:50:27 +0100"
    creation_dt = datetime.strptime(
        creation_date_str,
        "%Y-%m-%d %H:%M:%S %z"
    ).replace(tzinfo=None)

    # Check if inside any allowed window
    for start_dt, end_dt in time_windows:
        if start_dt <= creation_dt <= end_dt:
            filtered_records.append(record)
            break

print(f"Found {len(filtered_records)} matching records")

# Create new root element
new_root = ET.Element(root.tag)

# Add filtered records
for record in filtered_records:
    new_root.append(record)

# Write to new file
new_tree = ET.ElementTree(new_root)
new_tree.write("/Users/marjoleinvantol/Desktop/CDTF_project/Data/IphoneSE/filtered_IphoneSE_export.xml", encoding="utf-8", xml_declaration=True)

print("Filtered XML written to filtered_export.xml")