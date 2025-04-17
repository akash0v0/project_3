import pytest
from src.service.excel_processor import ExcelProcessor
import pandas as pd
from src.utils.result import Result 

@pytest.mark.parametrize(
    "test_case, data, columns, expected_output, expected_error",
    [
        # Test process_file with a valid file and columns
        (
            "valid_file_and_columns",
            {'Name': ['John', 'Alice'], 'City': ['New York', 'London'], 'Age': [30, 25]},
            ['Name', 'City'],
            Result.ok([['Age', 'Concatenated'], [30, 'John New York'], [25, 'Alice London']]), # Expected output wrapped in Result
            None
        ),
         # Test process_file with a valid file and columns, including integers
        (
            "valid_file_with_integers",
            {'ID': [101, 102], 'Status': ['Active', 'Inactive'], 'Score': [85, 92]},
            ['ID', 'Status'],
            Result.ok([['Score', 'Concatenated'], [85, '101 Active'], [92, '102 Inactive']]),  # Expected output wrapped in Result
            None
        ),
        # Test process_file with an invalid file path
        (
            "invalid_file_path",
            None,  # No data since the file doesn't exist
            ['Name', 'City'],
            Result.fail("File not found"),  # Expected error wrapped in Result
            "File not found"
        ),
        # Test process_file with missing columns
        (
            "missing_columns",
            {'Name': ['John', 'Alice'], 'City': ['New York', 'London']},
            ['Name', 'Country'],  # 'Country' doesn't exist
            Result.fail("Column 'Country' not found"),  # Expected error wrapped in Result
            "Column 'Country' not found"
        ),
        # Test process_file with an invalid file structure
        (
            "invalid_file_structure",
            {'Name': ['John', 'Alice'], 'City': ['New York', None]},  # Inconsistent rows
            ['Name', 'City'],
            Result.fail("Row contains null values in columns to concatenate"),  # Expected error wrapped in Result
            "Row contains null values in columns to concatenate"
        ),
        # Test process_file with empty data
        (
            "empty_data",
            {},
            ['Name', 'City'],
            Result.fail("Excel file contains no data"),  # Expected error wrapped in Result
            "Excel file contains no data"
        ),
        # Test process_file with only headers but no data rows 
        # In practice, this returns "Excel file contains no data"
        (
            "headers_only",
            {'Name': [], 'City': []},
            ['Name', 'City'],
            Result.fail("Excel file contains no data"),  # Expected error wrapped in Result
            "Excel file contains no data"
        ),
        # Test with a row that has a null value in a specified column
        (
            "null_in_column",
            {'Name': ['John', None], 'City': ['New York', 'London']},
            ['Name', 'City'],
            Result.fail("Row contains null values in columns to concatenate"),  # Expected error wrapped in Result
            "Row contains null values in columns to concatenate"
        ),

    ]
)
def test_process_file(test_case, data, columns, expected_output, expected_error, tmpdir):
    """
    Parameterized test for process_file with various scenarios.

    Inputs:
        test_case (str): Name of the test case.
        data (dict): Data to be written to the Excel file for testing.
        columns (list): List of columns to concatenate.
        expected_output (list): Expected output of the operation.
        expected_error (str): Expected error message if applicable.
    
    Functionality:
        - Tests the process_file method of ExcelProcessor with different scenarios.
        - Validates the exact output and error messages.
    
    Returns:
        None
    """
    file_path = None

    # Create test Excel file if data is provided
    if data is not None:
        file_path = tmpdir.join(f"{test_case}.xlsx")
        pd.DataFrame(data).to_excel(file_path, index=False)

    # Process the file
    if expected_error:
        # If an error is expected, check that it's raised correctly
        result = ExcelProcessor.process_file(str(file_path) if file_path else "nonexistent.xlsx", columns)
        assert not result.is_success()
        assert expected_error in result.error
    else:
        # If no error is expected, check the output
        result = ExcelProcessor.process_file(str(file_path) if file_path else "nonexistent.xlsx", columns)
        assert result.is_success()
        assert result.data == expected_output.data


########################################################################################################
# Test for handling exceptions during Excel file loading which we not able to test in test_process_file
########################################################################################################
@pytest.mark.parametrize(
    "test_case, exception_message, expected_error",
    [
        (
            "excel_loading_exception",
            "Test exception",
            "Error loading Excel file: Test exception"
        ),
        (
            "corrupted_file",
            "This is not a valid Excel file format",
            "Error loading Excel file:"
        ),
    ]
)
def test_excel_exceptions(test_case, exception_message, expected_error, tmpdir, monkeypatch):
    """
    Test for handling exceptions during Excel file loading.
    
    This test mocks pandas.read_excel to raise different types of exceptions,
    and verifies that the ExcelProcessor correctly handles them.
    """
    # Create a temporary Excel file
    file_path = tmpdir.join(f"{test_case}.xlsx")
    pd.DataFrame({'Name': ['John']}).to_excel(file_path, index=False)
    
    # Mock pandas.read_excel to raise an exception
    def mock_read_excel(*args, **kwargs):
        raise Exception(exception_message)
    
    monkeypatch.setattr(pd, "read_excel", mock_read_excel)
    
    # Process the file
    result = ExcelProcessor.process_file(str(file_path), ['Name'])
    
    # Verify the result
    assert not result.is_success()
    assert expected_error in result.error

# Direct tests for private methods to increase coverage
@pytest.mark.parametrize(
    "test_case, test_data, columns, expected_error",
    [
        (
            "insufficient_data_for_concatenation",
            [['Name', 'City', 'Age']],  # Headers only, no data rows
            ['Name', 'City'],
            "Insufficient data for concatenation"
        ),
        (
            "inconsistent_column_count",
            [
                ['Name', 'City', 'Age'],  # Headers
                ['John', 'New York', 30],  # Complete row
                ['Alice']                  # Row with missing columns
            ],
            ['Name', 'City'],
            "Row has inconsistent number of columns"
        ),
    ]
)
def test_concatenate_columns_edge_cases(test_case, test_data, columns, expected_error):
    """
    Test edge cases for the private concatenate_columns method.
    
    This test directly tests the __concatenate_columns method with various edge cases 
    to ensure full coverage of error conditions.
    """
    # Call the private method directly using name mangling
    result = ExcelProcessor._ExcelProcessor__concatenate_columns(test_data, columns)
    
    # Verify the result
    assert not result.is_success()
    assert expected_error in result.error