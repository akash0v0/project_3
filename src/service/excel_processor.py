import os
import pandas as pd
from typing import List

from src.utils.result import Result

class ExcelProcessor:
    
    @staticmethod
    def process_file(file_path: str, columns_to_concatenate: List[str]) -> Result[List[List[str]]]:
        """
        Process an Excel file by concatenating specified columns.
        
        Inputs:
            file_path (str): Path to the Excel file to process.
            columns_to_concatenate (List[str]): Column names to concatenate.
        
        Functionality:
            - Loads the Excel file.
            - Concatenates specified columns into a new column.
            - Returns the processed data in a structured format.
            
        Returns:
            Result[List[List[str]]]: Encapsulates success status, processed data, or error message.
        """
        result = None
        
        # Load Excel file
        load_result = ExcelProcessor.__load_excel_file(file_path)
        if load_result.is_success():
            # Concatenate columns if load was successful
            concat_result = ExcelProcessor.__concatenate_columns(load_result.data, columns_to_concatenate)
            result = concat_result
        else:
            # If excel loading failed, return the error
            result = load_result
        
        return result

    @staticmethod
    def __load_excel_file(file_path: str) -> Result[List[List[str]]]:
        """
        Load and validate an Excel file.
        
        Inputs:
            file_path (str): Path to the Excel file.
        
        Functionality:
            - Checks if the file exists.
            - Reads the Excel file into a pandas DataFrame.
            - Validates if the DataFrame is not empty.
            - Converts the DataFrame to a list of lists, including headers.
            
        Returns:
            Result[List[List[str]]] : Encapsulates success status, data, or error message.
        """
        result = None
        
        if not os.path.exists(file_path):
            result = Result.fail(f"File not found: {file_path}")
        else:
            try:
                # Read Excel file using pandas
                df = pd.read_excel(file_path)
                
                # Check if data is empty
                if df.empty:
                    result = Result.fail("Excel file contains no data")
                else:
                    # Convert DataFrame to list of lists
                    data = [df.columns.tolist()]  # Include headers
                    data.extend(df.values.tolist())  # Add data rows to the list
                    result = Result.ok(data)  # Return successful result with data
            except Exception as e:
                result = Result.fail(f"Error loading Excel file: {str(e)}")
                
        return result
    

    @staticmethod
    def __concatenate_columns(data: List[List[str]], column_names: List[str]) -> Result[List[List[str]]]:
        """
        Merge specified columns in the data and remove original columns.
        
        Inputs:
            data (List[List[str]]): Input data as a list of lists.
            column_names (List[str]): Column names to concatenate.
        
        Functionality:
            - Validates that the specified columns exist in the data.
            - Concatenates the values of the specified columns for each row.
            - Removes the original columns that were concatenated.
            - Returns a new list of lists with concatenated column but without original columns.
            
        Returns:
            Result[List[List[str]]]: Encapsulates success status, processed data, or error message.
        """
        result = None
        delimiter = " "  # Default delimiter
        
        if not data or len(data) < 2:  # Need at least headers and one row
            result = Result.fail("No data to process")
        else:
            headers = data[0]
            column_exists = True
            
            # Validate that all specified columns exist
            for column in column_names:
                if column not in headers:
                    result = Result.fail(f"Column '{column}' not found in the data")
                    column_exists = False
                    break
            
            if column_exists:
                # Get indices of columns to concatenate
                column_indices = [headers.index(column) for column in column_names]
                
                # Create new headers without the columns to be concatenated
                new_headers = [header for i, header in enumerate(headers) if i not in column_indices]
                new_headers.append("Concatenated")  # Add new header for concatenated column
                
                # Create new data with concatenated column but without original columns
                new_data = [new_headers]
                error_found = False
                
                for i, row in enumerate(data[1:], 1):  # Skip headers, keep track of row number
                    # Check if row has enough columns
                    if any(idx >= len(row) for idx in column_indices):
                        result = Result.fail("Row has inconsistent number of columns")
                        error_found = True
                        break
                    
                    # Extract values from specified columns
                    values_to_concatenate = [row[idx] for idx in column_indices]
                    
                    # Check for None or missing values in the specified columns
                    if any(value is None or pd.isna(value) for value in values_to_concatenate):
                        result = Result.fail("Row contains null values in columns to concatenate")
                        error_found = True
                        break
                    
                    # Create concatenated value
                    concatenated_value = delimiter.join(map(str, values_to_concatenate))
                    
                    # Create new row without the columns that were concatenated
                    new_row = [val for i, val in enumerate(row) if i not in column_indices]
                    new_row.append(concatenated_value)  # Add concatenated value
                    
                    new_data.append(new_row)
                
                if not error_found:
                    result = Result.ok(new_data)
        
        return result