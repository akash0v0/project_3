from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router.excel_router import router as excel_router

app = FastAPI(
    title="Excel Processor API",
    description="API to process Excel files by concatenating specified columns",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(excel_router)

@app.get("/")
async def root():
    return {
        "message": "Excel Processor API is running",
        "documentation": "/docs",
        "endpoints": {
            "process_excel": "/process-excel/"
        }
    }


