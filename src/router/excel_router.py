from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from src.service.excel_processor import ExcelProcessor

router = APIRouter(
    prefix="/process-excel",
    tags=["excel"],
)

@router.get("/")
async def process_excel(
    file_path: str = Query("static/sample.xlsx", description="Path to the Excel file"),
    columns: str = Query("Firstname,Lastname", description="Comma-separated column names to concatenate")
):
    """
    Process an Excel file by concatenating specified columns.

    Functionality:
        - Reads an Excel file from a given path.
        - Concatenates specified columns into a single column.
        - Returns the processed data in a structured format.

    Returns:
        Processed Excel data with concatenated column.
    """
    project_root = Path(__file__).parent.parent.parent
    full_file_path = project_root / file_path

    # Check if file exists
    if not full_file_path.exists():
        raise HTTPException(status_code=400, detail="File not found.")

    # Validate columns
    columns_to_concat = [col.strip() for col in columns.split(",") if col.strip()]
    if not columns_to_concat:
        raise HTTPException(status_code=400, detail="Invalid columns provided.")

    # Process file
    processor = ExcelProcessor()
    result = processor.process_file(full_file_path, columns_to_concat)

    if not result.is_success():
        raise HTTPException(status_code=400, detail=result.error)

    # Convert data to a more API-friendly format
    headers = result.data[0]
    rows = result.data[1:]

    formatted_data = {
        "headers": headers,
        "rows": rows,
        "concatenated_columns": columns_to_concat,
        "total_rows": len(rows)
    }

    return formatted_data
