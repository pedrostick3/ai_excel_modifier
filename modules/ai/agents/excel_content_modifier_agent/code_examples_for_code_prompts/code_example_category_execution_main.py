import pandas as pd

# Initialize the given variables
input_excel_file_path = './assets/docs_input/Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Execução - 16_12_2024 - Execution_data Template.xlsx'
excel_header_row_index = 1

def _check_column_name_and_make_case_insensitive_if_needed(df: pd.DataFrame, column_name: str, excel_header_row_index : int = None):
    valid_excel_header_row_index = excel_header_row_index and excel_header_row_index >= 0 and excel_header_row_index < len(df)
    columns = df.iloc[excel_header_row_index] if valid_excel_header_row_index else df.columns

    if column_name in columns:
        return column_name

    # Normalize column names to lowercase
    lower_columns = {str(col.lower()): col for col in columns}
    return lower_columns.get(column_name.lower(), None)

# Load the Excel file
df = pd.read_excel(input_excel_file_path, header=excel_header_row_index)

# Step 1: Move 'IsSuccessful' column to column A
is_successful_column_name = _check_column_name_and_make_case_insensitive_if_needed(df, 'IsSuccessful')
if is_successful_column_name:
    is_successful = df.pop(is_successful_column_name)
    df.insert(0, is_successful_column_name, is_successful)

# Step 2: Remove 'AverageRunTimeSeconds' column
average_run_time_seconds_column_name = _check_column_name_and_make_case_insensitive_if_needed(df, 'AverageRunTimeSeconds')
if average_run_time_seconds_column_name:
    df = df.drop(columns=[average_run_time_seconds_column_name])

# Step 3: Add 'RunTimeMinutes' column
# Convert 'RunTimeSeconds' to numeric and then divide
run_time_seconds_column_name = _check_column_name_and_make_case_insensitive_if_needed(df, 'RunTimeSeconds')
if run_time_seconds_column_name:
    df['RunTimeMinutes'] = pd.to_numeric(df[run_time_seconds_column_name], errors='coerce') / 60

# Step 4: Change format of date columns
date_columns = ['ExecutionStartDate', 'ExecutionEndDate', 'CaseStartDate', 'CaseEndDate']
for col in date_columns:
    column_name = _check_column_name_and_make_case_insensitive_if_needed(df, col)
    if column_name:
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce').dt.strftime('%d-%m-%Y %H:%M:%S.%f')
    
# Step 5: Change each value in 'TaskWorkload' by replacing '.' with ','
task_workload_column_name = _check_column_name_and_make_case_insensitive_if_needed(df, 'TaskWorkload')
if task_workload_column_name:
    df[task_workload_column_name] = df[task_workload_column_name].apply(lambda x: f"{x:,.5f}".replace('.', ',') if pd.notnull(x) else x)

# Save the modified DataFrame to a new Excel file
df.to_excel(output_excel_file_path, index=False)