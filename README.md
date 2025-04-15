## Project Setup and Execution Guide

Follow these steps to set up your environment, run the test cases, and launch the application:

### Prerequisites
Ensure you have the package manager **Poetry** installed on your system. If not, install it using the following command:
```bash
pip install poetry
```

### Setting Up the Project

1. Navigate to the project directory and install the required packages by running:
    ```bash
    poetry install
    ```

2. Configure your IDE to use the Poetry-generated virtual environment, or activate the virtual environment manually:
    ```bash
    poetry env activate
    ```

### Running Tests

To run the test cases, use the following command:
```bash
pytest
```

### Running the Application

To run the project in development mode:
```bash
fastapi dev src/main.py
```
