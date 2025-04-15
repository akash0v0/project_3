## How to Run the Test Cases

Follow these steps to set up your environment and run the test cases:

### Prerequisites
Ensure you have the package manager **Poetry** installed on your system. If not, install it using the following command:
```bash
pip install poetry
```

### Steps to Run the Project

1. Navigate to the project directory and install the required packages by running:
    ```bash
    poetry install
    ```

2. Configure your IDE to use the Poetry-generated virtual environment for running the tests, or activate the virtual environment manually:
    ```bash
    poetry env activate
    ```

3. Once the environment is set up, run the test cases using the following command:
    ```bash
    pytest
    ```

4. To run the project in development mode:
    ```bash
    fastapi dev src/main.py
    ```



