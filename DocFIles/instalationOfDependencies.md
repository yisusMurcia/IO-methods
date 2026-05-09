# Installation of project dependencies

This project uses Python and requires installing external libraries in the same interpreter used to run the code.

## Recommended steps

1. Activate the virtual environment if it exists:
   ```powershell
   .venv\Scripts\activate
   ```

2. Install the dependencies with the `requirements.txt` file:
   ```powershell
   pip install -r requirements.txt
   ```

3. If you need to update `pip`:
   ```powershell
   python -m pip install --upgrade pip
   ```

## What each step does

- `activate`: ensures that Python uses the project's virtual environment.
- `pip install -r requirements.txt`: installs the necessary libraries.
- `requirements.txt` contains dependencies such as `PySide6` and `numpy`.

## What to do if an error appears

- If `PySide6` is missing, check that you are using the correct interpreter.
- If a different Python than the virtual environment is used, it will show:
  - `ModuleNotFoundError: No module named 'PySide6'`

## Recommendation

Always use the same virtual environment to install dependencies and run the project. This prevents Python from looking for packages in another interpreter.
