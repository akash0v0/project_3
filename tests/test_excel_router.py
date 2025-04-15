import pytest
from fastapi.testclient import TestClient
from src.main import app

# Create a test client using the FastAPI application
client = TestClient(app)

@pytest.mark.parametrize("file_path,columns,expected_status,expected_detail", [
    # Test case 1: Valid file and columns - expect success
    ("static/sample.xlsx", "Firstname,Lastname", 200, None),
    # Test case 2: Non-existent file - expect error
    ("static/nonexistent.xlsx", "Firstname,Lastname", 400, "File not found."),
    # Test case 3: Valid file but empty columns - expect error
    ("static/sample.xlsx", "", 400, "Invalid columns provided."),
])
def test_process_excel(file_path, columns, expected_status, expected_detail):
    """
    Test the /process-excel/ endpoint with various inputs.
    
    Inputs:
        file_path (str): Path to the Excel file.
        columns (str): Comma-separated column names to concatenate.
        expected_status (int): Expected HTTP status code.
        expected_detail (str): Expected error message detail if applicable.
    
    Functionality:
        - Tests the /process-excel/ endpoint with different scenarios.
        - Validates the response status code and content.
    
    Returns:
        None
    """ 
    # Make GET request to the endpoint with query parameters
    response = client.get(f"/process-excel/?file_path={file_path}&columns={columns}")
    
    # Verify status code matches expected value
    assert response.status_code == expected_status, f"Unexpected status code: {response.status_code}"
    data = response.json()

    if expected_status == 200:
        # For successful responses, check that concatenated columns are returned correctly
        assert "concatenated_columns" in data, "Response is missing 'concatenated_columns'"
        assert data["concatenated_columns"] == ["Firstname", "Lastname"], "Concatenated columns mismatch"
    else:
        # For error responses, check that the error detail message is correct
        assert "detail" in data, "Response is missing 'detail'"
        assert data["detail"] == expected_detail, "Error message mismatch"