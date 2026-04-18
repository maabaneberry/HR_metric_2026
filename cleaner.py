import math
from datetime import datetime
from helper import read_hr_data


def remove_null_salaries(data):
    # Build a new list so that we keep only usable salary records for later analysis.
    new_list = []
    for entry in data:
        if math.isnan(entry[4]):
            continue
        else:
            new_list.append(entry)

    return new_list


def standardize_departments(data):
    # Convert department labels to lower case so grouping by department stays consistent.
    for i in range(len(data)):
        data[i][1] = data[i][1].lower()


def remove_invalid_performance_ratings(data):
    # Filter out ratings outside the valid range so averages are based on valid scores only.
    new_list = []
    for entry in data:
        if 0 <= entry[6] <= 5:
            new_list.append(entry)

    return new_list


def fix_format_dates(data):
    # Standardize dates first so the later date validation checks one consistent format.
    for i in range(len(data)):
        spilt_date = data[i][9].split("/")
        if len(spilt_date) != 3:
            continue
        else:
            data[i][9] = spilt_date[2] + "-" + spilt_date[1] + "-" + spilt_date[0]


def is_leap_year(year):
    # Separate leap-year logic so February validation is easier to read and re-use.
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False


def remove_invalid_dates(data):
    # Keep only dates that satisfy the assignment range and calendar rules.
    new_list = []
    for entry in data:
        split_date = entry[9].split("-")
        if int(split_date[0]) < 2015 or int(split_date[0]) > 2025 or int(split_date[1]) < 1 or int(split_date[1]) > 12 or int(split_date[2]) < 1 or (int(split_date[2]) > 30 and int(split_date[1] != 2)) or (is_leap_year(int(split_date[0])) and int(split_date[1]) == 2 and int(split_date[2]) > 29) or (not is_leap_year(int(split_date[0])) and int(split_date[1]) == 2 and int(split_date[2]) > 28):
            continue
        else:
            new_list.append(entry)

    return new_list


if __name__ == "__main__":
    # Load uncleaned data from CSV file
    data = read_hr_data('uncleaned_dataset.csv')
    print(f"Loaded {len(data)} employee records\n")

    print("=" * 70)
    print("DATA CLEANING")
    print("=" * 70)

    # Test data cleaning functions
    # Uncomment the lines below to test each cleaning function
    # You can modify the function arguments to test different inputs

    # 1. Remove null salaries
    removed_salaries = remove_null_salaries(data)
    print(f"Removed {len(removed_salaries)} records with null salaries")
    print(f"Remaining records: {len(data)}\n")

    # 2. Standardize departments
    standardize_departments(data)
    print("Standardized department names to lowercase\n")

    # 3. Remove invalid performance ratings
    removed_ratings = remove_invalid_performance_ratings(data)
    print(f"Removed {len(removed_ratings)} records with invalid performance ratings")
    print(f"Remaining records: {len(data)}\n")

    # 4. Fix hire date formatting
    fix_format_dates(data)
    print("Fixed hire date formatting\n")

    # 5. Remove invalid dates
    removed_dates = remove_invalid_dates(data)
    print(f"Removed {len(removed_dates)} records with invalid dates")
    print(f"Remaining records: {len(data)}\n")
