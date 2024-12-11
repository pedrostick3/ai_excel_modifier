import pandas as pd
import logging
import os
from io import StringIO

class ExcelService:
    """
    Service class to handle excel operations.
    """

    @staticmethod
    def get_excel_csv_to_csv_str(excel_file_path: str, only_get_first_rows: int = None) -> str:
        """
        Reads an Excel or CSV file and returns its content as a CSV formatted string.

        Args:
            excel_file_path (str): The path to the Excel or CSV file.
            only_get_first_rows (int): The number of rows to read from the file.
            
        Returns:
            str: A string containing the file content in CSV format.
        """        
        if not pd.io.common.file_exists(excel_file_path):
            logging.error(f"File not found: {excel_file_path}")
            raise FileNotFoundError(f"File not found: {excel_file_path}")

        # Check if the file is an Excel or CSV file
        _, file_extension = os.path.splitext(excel_file_path)
        if file_extension.lower() not in ['.xls', '.xlsx', '.csv']:
            logging.error(f"Invalid file type: {file_extension}")
            raise ValueError(f"Invalid file type: {file_extension}")

        try:
            if file_extension.lower() == '.csv':
                dataFrame = pd.read_csv(excel_file_path, header=None)
            else:
                dataFrame = pd.read_excel(excel_file_path, header=None)

            # Check if only_get_first_rows is a positive integer
            if only_get_first_rows is not None and only_get_first_rows > 0:
                dataFrame = dataFrame.head(only_get_first_rows)

            # Remove columns with "Unnamed" in the header
            # dataFrame.columns = [col if 'Unnamed' not in col else '' for col in dataFrame.columns]
            
            return dataFrame.to_csv(index=False, header=False)
        except Exception as e:
            logging.error(f"Error reading the excel file: {e}")
            raise

    @staticmethod
    def get_excel_csv_row_number(excel_file_path: str, excel_row_content: str) -> int:
        """
        Finds the row number of the specified content in the Excel or CSV file.

        Args:
            excel_file_path (str): The path to the Excel or CSV file.
            excel_row_content (str): The content to find in the file.

        Returns:
            int: The row number of the content in the file.
        """
        if not pd.io.common.file_exists(excel_file_path):
            logging.error(f"File not found: {excel_file_path}")
            raise FileNotFoundError(f"File not found: {excel_file_path}")

        _, file_extension = os.path.splitext(excel_file_path)
        if file_extension.lower() not in ['.xls', '.xlsx', '.csv']:
            logging.error(f"Invalid file type: {file_extension}")
            raise ValueError(f"Invalid file type: {file_extension}")

        try:
            if file_extension.lower() == '.csv':
                dataFrame = pd.read_csv(excel_file_path, header=None)
            else:
                dataFrame = pd.read_excel(excel_file_path, header=None)

            # Busca a linha que contém o conteúdo especificado
            matching_rows = dataFrame[dataFrame.apply(lambda row: ','.join(row.astype(str)).strip() == excel_row_content.strip(), axis=1)]

            if matching_rows.empty:
                logging.error(f"Content '{excel_row_content}' not found in the file.")
                raise ValueError(f"Content '{excel_row_content}' not found in the file.")

            row_number = matching_rows.index[0]
            return row_number
        except Exception as e:
            logging.error(f"Error finding the row number: {e}")
            raise

    @staticmethod
    def get_excel_csv_rows_as_str(excel_file_path: str, rows_indexes: list[int]) -> str:
        """
        Reads specified rows from an Excel or CSV file and returns them as a CSV formatted string.

        Args:
            excel_file_path (str): The path to the Excel or CSV file.
            rows_indexes (list[int]): A list of row indexes to extract from the file.

        Returns:
            str: A string containing the specified rows in CSV format.
        """
        if not pd.io.common.file_exists(excel_file_path):
            logging.error(f"File not found: {excel_file_path}")
            raise FileNotFoundError(f"File not found: {excel_file_path}")

        _, file_extension = os.path.splitext(excel_file_path)
        if file_extension.lower() not in ['.xls', '.xlsx', '.csv']:
            logging.error(f"Invalid file type: {file_extension}")
            raise ValueError(f"Invalid file type: {file_extension}")

        try:
            if file_extension.lower() == '.csv':
                dataFrame = pd.read_csv(excel_file_path, header=None)
            else:
                dataFrame = pd.read_excel(excel_file_path, header=None)

            # Extract the specified rows
            selected_rows = dataFrame.iloc[rows_indexes]

            return selected_rows.to_csv(index=False, header=False)
        except Exception as e:
            logging.error(f"Error reading the excel file: {e}")
            raise
    
    @staticmethod
    def save_excel_csv_data_into_file(excel_file_path: str, excel_data: str, log_excel_data: bool = False) -> bool:
        """
        Converts the CSV string `excel_data` into an Excel or CSV file and saves it at `excel_file_path`.

        Args:
            excel_file_path (str): Path to save the resulting file.
            excel_data (str): CSV data in string format.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            if log_excel_data:
                logging.info(f"Excel data to save: {excel_data}")

            # Convert CSV string to DataFrame
            dataFrame = pd.read_csv(StringIO(excel_data), header=None)

            # Determine the file type based on extension
            _, file_extension = os.path.splitext(excel_file_path)
            file_extension = file_extension.lower()

            if file_extension == '.csv':
                # Save as CSV
                dataFrame.to_csv(excel_file_path, index=False, header=False)
                logging.info(f"File successfully saved as CSV at: {excel_file_path}")
            elif file_extension in ['.xls', '.xlsx']:
                # Save as Excel
                dataFrame.to_excel(excel_file_path, index=False, header=False, engine='openpyxl')
                logging.info(f"File successfully saved as Excel at: {excel_file_path}")
            else:
                # Handle unsupported file extensions
                logging.error(f"Invalid output file type: {file_extension}")
                raise ValueError(f"Invalid output file type: {file_extension}")

            return True
        except Exception as e:
            logging.error(f"Error saving the file: {e}")
            return False
    
    @staticmethod
    def replace_excel_csv_data_in_file(
        excel_input_file_path: str,
        excel_output_file_path: str,
        excel_data: str,
        initial_index_for_replacement: int,
        final_index_for_replacement: int,
        log_excel_data: bool = False
    ) -> bool:
        """
        Replaces a portion of the data in an existing Excel or CSV file with new data and saves it to a new file.

        Args:
            excel_input_file_path (str): Path to the input file.
            excel_output_file_path (str): Path to save the resulting file.
            excel_data (str): CSV data in string format to replace the existing data.
            initial_index_for_replacement (int): Starting index for the replacement.
            final_index_for_replacement (int): Ending index for the replacement.
            log_excel_data (bool): Flag to log the excel data.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            if log_excel_data:
                logging.info(f"Excel data to replace: {excel_data}")

            # Convert CSV string to DataFrame
            new_data_frame = pd.read_csv(StringIO(excel_data), header=None)

            # Determine the file type based on extension
            _, file_extension = os.path.splitext(excel_input_file_path)
            file_extension = file_extension.lower()

            # Read the existing file into a DataFrame
            if file_extension == '.csv':
                existing_data_frame = pd.read_csv(excel_input_file_path, header=None)
            elif file_extension in ['.xls', '.xlsx']:
                existing_data_frame = pd.read_excel(excel_input_file_path, header=None)
            else:
                logging.error(f"Invalid input file type: {file_extension}")
                raise ValueError(f"Invalid input file type: {file_extension}")

            # Replace the specified rows with new data
            existing_data_frame.iloc[initial_index_for_replacement:final_index_for_replacement] = new_data_frame.values

            # Save the modified DataFrame to the output file
            if file_extension == '.csv':
                existing_data_frame.to_csv(excel_output_file_path, index=False, header=False)
                logging.info(f"File successfully saved as CSV at: {excel_output_file_path}")
            elif file_extension in ['.xls', '.xlsx']:
                existing_data_frame.to_excel(excel_output_file_path, index=False, header=False, engine='openpyxl')
                logging.info(f"File successfully saved as Excel at: {excel_output_file_path}")
            else:
                logging.error(f"Invalid output file type: {file_extension}")
                raise ValueError(f"Invalid output file type: {file_extension}")

            return True
        except Exception as e:
            logging.error(f"Error replacing data in the file: {e}")
            return False
        
    @staticmethod
    def add_excel_csv_data_to_file(
        excel_input_file_path: str,
        excel_output_file_path: str,
        excel_data: str,
        log_excel_data: bool = False
    ) -> bool:
        """
        Adds new data to an existing Excel or CSV file and saves it to a new file.

        Args:
            excel_input_file_path (str): Path to the input file.
            excel_output_file_path (str): Path to save the resulting file.
            excel_data (str): CSV data in string format to replace the existing data.
            log_excel_data (bool): Flag to log the excel data.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            if log_excel_data:
                logging.info(f"Excel data to add: {excel_data}")

            # Convert CSV string to DataFrame
            new_data_frame = pd.read_csv(StringIO(excel_data), header=None)

            # Determine the file type based on extension
            _, file_extension = os.path.splitext(excel_input_file_path)
            file_extension = file_extension.lower()

            # Read the existing file into a DataFrame
            if file_extension == '.csv':
                existing_data_frame = pd.read_csv(excel_input_file_path, header=None)
            elif file_extension in ['.xls', '.xlsx']:
                existing_data_frame = pd.read_excel(excel_input_file_path, header=None)
            else:
                logging.error(f"Invalid input file type: {file_extension}")
                raise ValueError(f"Invalid input file type: {file_extension}")

            # Append the new data to the existing data
            combined_data_frame = pd.concat([existing_data_frame, new_data_frame], ignore_index=True)

            # Save the combined DataFrame to the output file
            if file_extension == '.csv':
                combined_data_frame.to_csv(excel_output_file_path, index=False, header=False)
                logging.info(f"File successfully saved as CSV at: {excel_output_file_path}")
            elif file_extension in ['.xls', '.xlsx']:
                combined_data_frame.to_excel(excel_output_file_path, index=False, header=False, engine='openpyxl')
                logging.info(f"File successfully saved as Excel at: {excel_output_file_path}")
            else:
                logging.error(f"Invalid output file type: {file_extension}")
                raise ValueError(f"Invalid output file type: {file_extension}")

            return True
        except Exception as e:
            logging.error(f"Error adding data to the file: {e}")
            return False
        
