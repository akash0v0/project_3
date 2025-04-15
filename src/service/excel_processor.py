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
        # Load Excel file
        load_result = ExcelProcessor.__load_excel_file(file_path)
        if not load_result.is_success():
            return load_result  # Return Result directly
        
        # Concatenate columns
        concat_result = ExcelProcessor.__concatenate_columns(load_result.data, columns_to_concatenate)
        if not concat_result.is_success():
            return concat_result  # Return Result directly
        
        return concat_result  # Return Result directly

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
        # Check if file exists
        if not os.path.exists(file_path):
            return Result.fail(f"File not found: {file_path}")

        try:
            # Read Excel file using pandas
            df = pd.read_excel(file_path)
            
            # Check if data is empty
            if df.empty:
                return Result.fail("Excel file contains no data")
            
            # Convert DataFrame to list of lists
            data = [df.columns.tolist()]  # Include headers
            data.extend(df.values.tolist())
            
            return Result.ok(data)
        except Exception as e:
            return Result.fail(f"Error loading Excel file: {str(e)}")
    
    @staticmethod
    def __concatenate_columns(data: List[List[str]], column_names: List[str]) -> Result[List[List[str]]]:
        """
        Merge specified columns in the data.
        
        Inputs:
            data (List[List[str]]): Input data as a list of lists.
            column_names (List[str]): Column names to concatenate.
        
        Functionality:
            - Validates that the specified columns exist in the data.
            - Concatenates the values of the specified columns for each row.
            - Returns a new list of lists with an additional concatenated column.
            
        Returns:
            Result[List[List[str]]]: Encapsulates success status, processed data, or error message.
        """
        delimiter = " "  # Default delimiter
        if not data or len(data) < 2:  # Need at least headers and one row
            return Result.fail("No data to process")
        
        headers = data[0]
        
        # Validate that all specified columns exist
        for column in column_names:
            if column not in headers:
                return Result.fail(f"Column '{column}' not found in the data")
        
        # Get indices of columns to concatenate
        column_indices = [headers.index(column) for column in column_names]
        
        # Create new data with concatenated column
        new_data = [headers + ["Concatenated"]]  # Add new header
        
        for i, row in enumerate(data[1:], 1):  # Skip headers, keep track of row number
            # Check if row has enough columns
            if any(idx >= len(row) for idx in column_indices):
                return Result.fail("Row has inconsistent number of columns")
            
            # Extract values from specified columns
            values_to_concatenate = [row[idx] for idx in column_indices]
            
            # Check for None or missing values in the specified columns
            if any(value is None or pd.isna(value) for value in values_to_concatenate):
                return Result.fail("Row contains null values in columns to concatenate")
            
            # Create concatenated value
            concatenated_value = delimiter.join(map(str, values_to_concatenate))
            
            # Add row with concatenated value
            new_data.append(row + [concatenated_value])
        
        return Result.ok(new_data)

