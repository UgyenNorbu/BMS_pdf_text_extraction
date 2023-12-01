import os
import pandas as pd

folder_path = "output/"

all_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

for file in all_files:
    file_path = os.path.join(folder_path, file)
    data = pd.read_excel(file_path, header=None)
    data_wide = data.transpose()
    combined_data = pd.concat([combined_data, data_wide], ignore_index=True)

# Save the combined data to a new Excel file
combined_data.to_excel("output/Master_BMS_data.xlsx")
