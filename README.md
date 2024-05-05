# Arm Movement

This application controls the movement of an arm using the asyncio concurrency technique.

## Remarks

- The responsiveness of the application was achieved using asyncio.
- According to the task description, the function that moves the arm should have only two arguments: distance and direction. Therefore, I assume that the system has only one arm. If there were multiple arms, the function would need an additional argument to identify the arm.
- The interfaces of the arm components don't include an arm identifier. Therefore, I use a static method, which applies to all instances of the component classes.
- The project uses Poetry for dependency management, pytest for testing, and pylint and black for code checking and formatting, respectively.

## Start the Application

1. Clone the Git repository:
git clone https://github.com/AnnaShcherenko/ArmMovement.git

2. Create a virtual environment and install the dependencies:
poetry config virtualenvs.path "{path to your local folder}/.env" 
poetry install

3. Activate the virtual environment:
poetry shell

4. Run the Python module:
poetry run python -m app.main

5. To run the tests:
poetry run pytest

Please replace {path to your local folder} with the actual path to your local folder.
