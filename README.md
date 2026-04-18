# HR Data Cleaning and Metrics Project

This project contains Python functions for:

- cleaning HR employee data
- calculating HR metrics from the cleaned dataset
- testing the cleaning and metrics functions with `pytest`

## Project Files

- `helper.py`: reads CSV data into a list of records
- `cleaner.py`: contains data cleaning functions
- `metrics.py`: contains metrics and analysis functions
- `test_cleaner.py`: tests for the cleaning functions
- `test_metrics.py`: tests for the metrics functions
- `uncleaned_dataset.csv`: raw HR dataset
- `cleaned_dataset.csv`: cleaned HR dataset used for metrics

## Requirements

You need:

- Python 3
- `pytest`

If `pytest` is not installed in your current Python environment, install it with:

```bash
python3 -m pip install pytest
```

## Move to the Project Folder

Run all commands from the project directory:

```bash
cd "/Users/berry_m/Downloads/PGdip Data Science/Semester 1/COMS5022A_Programming for Data Scientists/Assignment/project"
```

## How to Run the Cleaning File

To run the cleaning functions file:

```bash
python3 cleaner.py
```

This will load `uncleaned_dataset.csv` and run the example code in `cleaner.py`.

## How to Run the Metrics File

To run the metrics functions file:

```bash
python3 metrics.py
```

This will load `cleaned_dataset.csv` and run the example code in `metrics.py`.

## How to Run All Tests

To run the full test suite:

```bash
pytest -q
```

This runs:

- `test_cleaner.py`
- `test_metrics.py`

## How to Run Cleaner Tests Only

```bash
pytest -q test_cleaner.py
```

## How to Run Metrics Tests Only

```bash
pytest -q test_metrics.py
```

## If You Get `No module named pytest`

This means the Python interpreter you used does not have `pytest` installed.

Try:

```bash
pytest -q
```

instead of running the test file directly with a Python path that uses a different environment.

## Expected Test Output

If everything is correct, you should see output similar to:

```bash
........................................................ [100%]
56 passed in 0.02s
```

This means:

- every discovered test was run
- all tests passed
- the test run completed successfully# hr-metric-2026
This is an Human Resource metrics
