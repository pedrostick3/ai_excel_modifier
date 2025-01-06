import pandas as pd

# Initialize the given variables
input_excel_file_path = './assets/docs_input/Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Execução - 16_12_2024 - Execution_data Template.xlsx'
excel_header_row_index = 1

# Load the Excel file
df = pd.read_excel(input_excel_file_path, header=excel_header_row_index)

# Step 1: Move 'IsSuccessful' column to column A
is_successful = df.pop('IsSuccessful')
df.insert(0, 'IsSuccessful', is_successful)

# Step 2: Remove 'AverageRunTimeSeconds' column
df = df.drop(columns=['AverageRunTimeSeconds'])

# Step 3: Add 'RunTimeMinutes' column
# Convert 'RunTimeSeconds' to numeric and then divide
df['RunTimeMinutes'] = pd.to_numeric(df['RunTimeSeconds'], errors='coerce') / 60

# Step 4: Change format of date columns
date_columns = ['ExecutionStartDate', 'ExecutionEndDate', 'CaseStartDate', 'CaseEndDate']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d-%m-%Y %H:%M:%S.%f')
    
# Step 5: Change each value in 'TaskWorkload' by replacing '.' with ','
df['TaskWorkload'] = df['TaskWorkload'].apply(lambda x: f"{x:,.5f}".replace('.', ',') if pd.notnull(x) else x)

# Save the modified DataFrame to a new Excel file
df.to_excel(output_excel_file_path, index=False)