import pandas as pd

# Vars
input_excel_file_path = './assets/docs_input/Test_Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Teste Execução - 13_12_2024 - Test_Execution_data Template.xlsx'
excel_header_row_index = 3
columns_to_sum = ['RunTimeSeconds', 'TaskWorkload']

# Read Excel file
try:
    df = pd.read_excel(input_excel_file_path, header=None)
except Exception as e:
    print(f'Error reading file: {e}')
    exit()

# Reorder the columns
try:
    expected_columns_order = ['ExecutionId', 'ExecutionStartDate', 'ExecutionEndDate', 'TaskWorkload', 'CaseStartDate', 'CaseEndDate', 'IsSuccessful', 'RunTimeSeconds', 'AverageRunTimeSeconds']
    table_last_row = df.last_valid_index()
    
    # Select the part of the DataFrame that contains the data, including the header
    data_to_sort = df.iloc[excel_header_row_index:table_last_row + 1]  # +1 to include the last line
    
    # Setting headers for the selected part
    data_to_sort.columns = df.iloc[excel_header_row_index]  # Setting the header row as columns

    # Reorder the columns according to the defined list
    data_to_sort = data_to_sort[expected_columns_order]  # Reordering the columns
    
    # Replace the data in the original DataFrame
    df.iloc[excel_header_row_index:table_last_row + 1] = data_to_sort.values  # Update the relevant part

    print('Reordering columns executed successfully - Columns reordered')
    df.to_excel(output_excel_file_path, index=False, header=False)
except KeyError as e:
    print(f'Error reordering columns - Missing expected columns: {e}')

# Change dots to commas
try:
    # Check if the header row is defined and if the 'TaskWorkload' column is present
    if excel_header_row_index is not None and excel_header_row_index < len(df):
        # Access the 'TaskWorkload' column using the defined header
        task_workload_col_index = df.iloc[excel_header_row_index].tolist().index('TaskWorkload')
        
        # Apply the replacement of dots with commas
        df.iloc[excel_header_row_index + 1:, task_workload_col_index] = df.iloc[excel_header_row_index + 1:, task_workload_col_index].apply(lambda x: str(x).replace('.', ','))
        
        print('Changing dots to commas executed successfully - TaskWorkload values adjusted')
        df.to_excel(output_excel_file_path, index=False, header=False)
    else:
        print('Error changing dots to commas - Header row not found or invalid')
except Exception as e:
    print(f'Error changing dots to commas - {str(e)}')

# Add 'RunTimeSeconds' and 'TaskWorkload' sums
try:
    # Check if the header rows and last row are valid
    if excel_header_row_index is not None and table_last_row is not None and table_last_row >= excel_header_row_index:
        # Read the file into an Aux DataFrame
        aux_dataFrame = pd.read_excel(output_excel_file_path, header=excel_header_row_index)

        # Try to convert the columns to numeric values without changing the original values
        columns_sums = {column: pd.to_numeric(aux_dataFrame[column].astype(str).str.replace(',', '.').astype(float), errors='coerce').sum() for column in columns_to_sum}
        columns_number_index = {column: aux_dataFrame.columns.get_loc(column) for column in columns_to_sum}

        # Add a new row with the totals at the bottom
        new_row = ['' for _ in range(len(aux_dataFrame.columns))]
        for column, sum_value in columns_sums.items():
            new_row[columns_number_index[column]] = sum_value

        # Append the new row to the DataFrame
        df = pd.concat([df, pd.DataFrame([new_row], columns=df.columns)], ignore_index=True, sort=False)
        print("Add 'RunTimeSeconds' and 'TaskWorkload' sums executed successfully - TaskWorkload sum added")
    else:
        print("Error adding 'RunTimeSeconds' and 'TaskWorkload' sums - Invalid header rows or last row")
except KeyError as e:
    print(f"Error adding 'RunTimeSeconds' and 'TaskWorkload' sums - Missing column: {e}")
except Exception as e:
    print(f"Error adding 'RunTimeSeconds' and 'TaskWorkload' sums - {str(e)}")

# Save the file
try:
    df.to_excel(output_excel_file_path, index=False, header=False)
    print('File saved successfully')
except Exception as e:
    print(f'Error saving file: {e}')