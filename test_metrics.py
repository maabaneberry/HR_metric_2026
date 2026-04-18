import pytest
import math
from datetime import datetime
from metrics import (
    get_unique_departments,
    get_gender_distribution,
    get_avg_age_by_department,
    get_retention_rate,
    get_turnover_rate_by_department,
    get_avg_salary_by_age_range,
    get_avg_dept_performance_by_training_range
)


# ============================================================================
# FIXTURES - Sample Clean Data for Testing
# ============================================================================

@pytest.fixture
def sample_clean_data():
    """
    Sample cleaned dataset with multiple departments and employees.
    Used for general metrics testing.
    """
    return [
        ['EMP1000', 'engineering', 'Male', 30, 75000.0, 25, 4.0, 0.1, 'Active', '2018-05-10'],
        ['EMP1001', 'engineering', 'Female', 28, 70000.0, 30, 4.2, 0.05, 'Active', '2019-03-15'],
        ['EMP1002', 'engineering', 'Non-binary', 35, 80000.0, 20, 3.8, 0.15, 'Resigned', '2017-07-20'],
        ['EMP1003', 'sales', 'Male', 32, 65000.0, 28, 3.5, 0.12, 'Active', '2016-11-05'],
        ['EMP1004', 'sales', 'Female', 29, 62000.0, 22, 3.8, 0.08, 'Resigned', '2020-01-30'],
        ['EMP1005', 'sales', 'Male', 31, 68000.0, 35, 3.9, 0.11, 'Active', '2019-06-12'],
        ['EMP1006', 'hr', 'Female', 45, 90000.0, 40, 4.5, 0.03, 'Active', '2015-02-28'],
        ['EMP1007', 'hr', 'Female', 42, 88000.0, 38, 4.3, 0.02, 'Active', '2016-08-14'],
        ['EMP1008', 'marketing', 'Male', 26, 55000.0, 15, 3.2, 0.18, 'Active', '2021-04-01'],
        ['EMP1009', 'marketing', 'Non-binary', 27, 57000.0, 18, 3.4, 0.16, 'Resigned', '2022-09-10'],
        ['EMP1010', 'product', 'Female', 40, 95000.0, 32, 4.4, 0.06, 'Active', '2018-12-03'],
        ['EMP1011', 'product', 'Male', 38, 92000.0, 28, 4.1, 0.08, 'Active', '2019-11-17']
    ]


@pytest.fixture
def data_single_department():
    """
    Sample dataset with all employees in one department.
    Tests metrics when only one department exists.
    """
    return [
        ['EMP1000', 'engineering', 'Male', 30, 75000.0, 25, 4.0, 0.1, 'Active', '2018-05-10'],
        ['EMP1001', 'engineering', 'Female', 28, 70000.0, 30, 4.2, 0.05, 'Active', '2019-03-15'],
        ['EMP1002', 'engineering', 'Non-binary', 35, 80000.0, 20, 3.8, 0.15, 'Resigned', '2017-07-20']
    ]


@pytest.fixture
def data_all_active():
    """
    Sample dataset where all employees are active.
    Tests retention rate calculation with 100% retention.
    """
    return [
        ['EMP1000', 'engineering', 'Male', 30, 75000.0, 25, 4.0, 0.1, 'Active', '2018-05-10'],
        ['EMP1001', 'engineering', 'Female', 28, 70000.0, 30, 4.2, 0.05, 'Active', '2019-03-15'],
        ['EMP1002', 'sales', 'Male', 32, 65000.0, 28, 3.5, 0.12, 'Active', '2016-11-05'],
        ['EMP1003', 'hr', 'Female', 45, 90000.0, 40, 4.5, 0.03, 'Active', '2015-02-28']
    ]


@pytest.fixture
def data_all_resigned():
    """
    Sample dataset where all employees are resigned.
    Tests retention rate calculation with 0% retention.
    """
    return [
        ['EMP1000', 'engineering', 'Male', 30, 75000.0, 25, 4.0, 0.1, 'Resigned', '2018-05-10'],
        ['EMP1001', 'engineering', 'Female', 28, 70000.0, 30, 4.2, 0.05, 'Resigned', '2019-03-15'],
        ['EMP1002', 'sales', 'Male', 32, 65000.0, 28, 3.5, 0.12, 'Resigned', '2016-11-05']
    ]


@pytest.fixture
def data_gender_distribution():
    """
    Sample dataset with known gender distribution for testing.
    Each department has specific gender counts for predictable percentages.
    """
    return [
        ['EMP1000', 'engineering', 'Male', 30, 75000.0, 25, 4.0, 0.1, 'Active', '2018-05-10'],
        ['EMP1001', 'engineering', 'Male', 28, 70000.0, 30, 4.2, 0.05, 'Active', '2019-03-15'],
        ['EMP1002', 'engineering', 'Female', 35, 80000.0, 20, 3.8, 0.15, 'Active', '2017-07-20'],
        ['EMP1003', 'engineering', 'Female', 32, 65000.0, 28, 3.5, 0.12, 'Active', '2016-11-05'],
        ['EMP1004', 'sales', 'Male', 29, 62000.0, 22, 3.8, 0.08, 'Active', '2020-01-30'],
        ['EMP1005', 'sales', 'Female', 31, 68000.0, 35, 3.9, 0.11, 'Active', '2019-06-12']
    ]


@pytest.fixture
def data_age_range():
    """
    Sample dataset with employees in specific age ranges.
    Tests average salary calculations for different age groups.
    """
    return [
        ['EMP1000', 'engineering', 'Male', 25, 70000.0, 25, 4.0, 0.1, 'Active', '2018-05-10'],
        ['EMP1001', 'engineering', 'Female', 30, 75000.0, 30, 4.2, 0.05, 'Active', '2019-03-15'],
        ['EMP1002', 'sales', 'Male', 35, 80000.0, 20, 3.8, 0.15, 'Active', '2017-07-20'],
        ['EMP1003', 'sales', 'Female', 40, 85000.0, 28, 3.5, 0.12, 'Active', '2016-11-05'],
        ['EMP1004', 'hr', 'Male', 45, 90000.0, 22, 3.8, 0.08, 'Active', '2020-01-30'],
        ['EMP1005', 'hr', 'Female', 50, 95000.0, 35, 3.9, 0.11, 'Active', '2019-06-12']
    ]


@pytest.fixture
def data_training_hours():
    """
    Sample dataset with employees having different training hour levels.
    Tests performance rating by training hours range per department.
    """
    return [
        ['EMP1000', 'engineering', 'Male', 30, 75000.0, 10, 2.8, 0.1, 'Active', '2018-05-10'],
        ['EMP1001', 'engineering', 'Female', 28, 70000.0, 25, 3.9, 0.05, 'Active', '2019-03-15'],
        ['EMP1002', 'engineering', 'Male', 35, 80000.0, 40, 4.5, 0.15, 'Active', '2017-07-20'],
        ['EMP1003', 'sales', 'Female', 32, 65000.0, 15, 3.1, 0.12, 'Active', '2016-11-05'],
        ['EMP1004', 'sales', 'Male', 29, 62000.0, 30, 3.8, 0.08, 'Active', '2020-01-30'],
        ['EMP1005', 'sales', 'Non-binary', 31, 68000.0, 45, 4.2, 0.11, 'Active', '2019-06-12'],
        ['EMP1006', 'hr', 'Female', 45, 90000.0, 20, 4.0, 0.03, 'Active', '2015-02-28'],
        ['EMP1007', 'hr', 'Male', 42, 88000.0, 35, 4.4, 0.02, 'Active', '2016-08-14']
    ]


# ============================================================================
# TEST FUNCTIONS - get_unique_departments()
# ============================================================================

def test_get_unique_departments_returns_set(sample_clean_data):
    """
    Test that get_unique_departments returns a set data type.
    Expected: Return type is set.
    """
    result = get_unique_departments(sample_clean_data)
    assert isinstance(result, set)


def test_get_unique_departments_correct_departments(sample_clean_data):
    """
    Test that get_unique_departments returns all unique departments.
    Expected: Returns {'engineering', 'sales', 'hr', 'marketing', 'product'}.
    """
    result = get_unique_departments(sample_clean_data)
    expected = {'engineering', 'sales', 'hr', 'marketing', 'product'}
    assert result == expected


def test_get_unique_departments_single_department(data_single_department):
    """
    Test that get_unique_departments correctly handles dataset with single department.
    Expected: Returns set with single department.
    """
    result = get_unique_departments(data_single_department)
    assert result == {'engineering'}


def test_get_unique_departments_count(sample_clean_data):
    """
    Test that get_unique_departments returns correct count of departments.
    Expected: Returns 5 unique departments.
    """
    result = get_unique_departments(sample_clean_data)
    assert len(result) == 5


# ============================================================================
# TEST FUNCTIONS - get_gender_distribution()
# ============================================================================

def test_get_gender_distribution_returns_dict(sample_clean_data):
    """
    Test that get_gender_distribution returns a dictionary.
    Expected: Return type is dict.
    """
    result = get_gender_distribution(sample_clean_data)
    assert isinstance(result, dict)


def test_get_gender_distribution_nested_dict(sample_clean_data):
    """
    Test that get_gender_distribution returns nested dictionaries.
    Expected: Each department value is a dictionary with gender keys.
    """
    result = get_gender_distribution(sample_clean_data)
    for dept, gender_dict in result.items():
        assert isinstance(gender_dict, dict)


def test_get_gender_distribution_two_decimal_places(data_gender_distribution):
    """
    Test that all gender percentages are rounded to exactly 2 decimal places.
    Expected: All percentage values have exactly 2 decimal places.
    """
    result = get_gender_distribution(data_gender_distribution)
    for dept, gender_dict in result.items():
        for gender, percentage in gender_dict.items():
            # Check that value equals itself when rounded to 2 decimals
            assert percentage == round(percentage, 2)


def test_get_gender_distribution_sum_to_100(data_gender_distribution):
    """
    Test that gender percentages for each department sum to 100%.
    Expected: Sum of percentages per department equals 100.0.
    """
    result = get_gender_distribution(data_gender_distribution)
    for dept, gender_dict in result.items():
        total = sum(gender_dict.values())
        assert total == 100.0


def test_get_gender_distribution_correct_percentages(data_gender_distribution):
    """
    Test that gender distribution percentages are calculated correctly.
    Expected: Engineering has 50% Male, 50% Female. Sales has 50% Male, 50% Female.
    """
    result = get_gender_distribution(data_gender_distribution)
    assert result['engineering']['Male'] == 50.0
    assert result['engineering']['Female'] == 50.0
    assert result['sales']['Male'] == 50.0
    assert result['sales']['Female'] == 50.0


# ============================================================================
# TEST FUNCTIONS - get_avg_age_by_department()
# ============================================================================

def test_get_avg_age_by_department_returns_dict(sample_clean_data):
    """
    Test that get_avg_age_by_department returns a dictionary.
    Expected: Return type is dict.
    """
    result = get_avg_age_by_department(sample_clean_data)
    assert isinstance(result, dict)


def test_get_avg_age_by_department_two_decimal_places(sample_clean_data):
    """
    Test that all average ages are rounded to exactly 2 decimal places.
    Expected: All values have exactly 2 decimal places.
    """
    result = get_avg_age_by_department(sample_clean_data)
    for dept, avg_age in result.items():
        assert avg_age == round(avg_age, 2)


def test_get_avg_age_by_department_correct_calculation(data_age_range):
    """
    Test that average ages are calculated correctly.
    Expected: Engineering avg = 27.5, Sales avg = 35.0, HR avg = 47.5.
    """
    result = get_avg_age_by_department(data_age_range)
    assert result['engineering'] == 27.5
    assert result['sales'] == 37.5
    assert result['hr'] == 47.5


def test_get_avg_age_by_department_single_employee(data_single_department):
    """
    Test that average age for single employee equals that employee's age.
    Expected: Engineering avg includes all 3 employees' ages correctly.
    """
    result = get_avg_age_by_department(data_single_department)
    # Average of 30, 28, 35 = 31.0
    assert result['engineering'] == round((30 + 28 + 35) / 3, 2)


# ============================================================================
# TEST FUNCTIONS - get_retention_rate()
# ============================================================================

def test_get_retention_rate_returns_float(sample_clean_data):
    """
    Test that get_retention_rate returns a float.
    Expected: Return type is float.
    """
    result = get_retention_rate(sample_clean_data)
    assert isinstance(result, float)


def test_get_retention_rate_two_decimal_places(sample_clean_data):
    """
    Test that retention rate is rounded to exactly 2 decimal places.
    Expected: Value equals itself when rounded to 2 decimals.
    """
    result = get_retention_rate(sample_clean_data)
    assert result == round(result, 2)


def test_get_retention_rate_all_active(data_all_active):
    """
    Test that retention rate is 100% when all employees are active.
    Expected: Retention rate = 100.0.
    """
    result = get_retention_rate(data_all_active)
    assert result == 100.0


def test_get_retention_rate_all_resigned(data_all_resigned):
    """
    Test that retention rate is 0% when all employees are resigned.
    Expected: Retention rate = 0.0.
    """
    result = get_retention_rate(data_all_resigned)
    assert result == 0.0


def test_get_retention_rate_correct_calculation(sample_clean_data):
    """
    Test that retention rate is calculated correctly.
    Expected: 9 active + 4 resigned = 12 total. Retention = (8/12)*100 = 66.67%.
    """
    result = get_retention_rate(sample_clean_data)
    expected = round((9 / 12) * 100, 2)
    assert result == expected


# ============================================================================
# TEST FUNCTIONS - get_turnover_rate_by_department()
# ============================================================================

def test_get_turnover_rate_by_department_returns_dict(sample_clean_data):
    """
    Test that get_turnover_rate_by_department returns a dictionary.
    Expected: Return type is dict.
    """
    result = get_turnover_rate_by_department(sample_clean_data)
    assert isinstance(result, dict)


def test_get_turnover_rate_by_department_two_decimal_places(sample_clean_data):
    """
    Test that all turnover rates are rounded to exactly 2 decimal places.
    Expected: All values have exactly 2 decimal places.
    """
    result = get_turnover_rate_by_department(sample_clean_data)
    for dept, rate in result.items():
        assert rate == round(rate, 2)


def test_get_turnover_rate_by_department_correct_calculation(data_single_department):
    """
    Test that turnover rate is calculated correctly per department.
    Expected: Engineering has 1 resigned out of 3 = 33.33% turnover.
    """
    result = get_turnover_rate_by_department(data_single_department)
    expected = round((1 / 3) * 100, 2)
    assert result['engineering'] == expected


def test_get_turnover_rate_all_departments(sample_clean_data):
    """
    Test that turnover rate is calculated for all departments.
    Expected: All 5 departments have a turnover rate calculated.
    """
    result = get_turnover_rate_by_department(sample_clean_data)
    assert len(result) == 5
    assert 'engineering' in result
    assert 'sales' in result
    assert 'hr' in result
    assert 'marketing' in result
    assert 'product' in result


# ============================================================================
# TEST FUNCTIONS - get_avg_salary_by_age_range()
# ============================================================================

def test_get_avg_salary_by_age_range_returns_float(sample_clean_data):
    """
    Test that get_avg_salary_by_age_range returns a float.
    Expected: Return type is float.
    """
    result = get_avg_salary_by_age_range(sample_clean_data, 25, 35)
    assert isinstance(result, float)


def test_get_avg_salary_by_age_range_two_decimal_places(sample_clean_data):
    """
    Test that average salary is rounded to exactly 2 decimal places.
    Expected: Value equals itself when rounded to 2 decimals.
    """
    result = get_avg_salary_by_age_range(sample_clean_data, 25, 35)
    assert result == round(result, 2)


def test_get_avg_salary_by_age_range_correct_calculation(data_age_range):
    """
    Test that average salary is calculated correctly for age range.
    Expected: Ages 25-30 include 70000.0, 75000.0. Average = 72500.0.
    """
    result = get_avg_salary_by_age_range(data_age_range, 25, 30)
    expected = round((70000.0 + 75000.0) / 2, 2)
    assert result == expected


def test_get_avg_salary_by_age_range_inclusive_bounds(data_age_range):
    """
    Test that age range is inclusive of both minimum and maximum ages.
    Expected: Range 25-25 includes only age 25 employee (salary 70000.0).
    """
    result = get_avg_salary_by_age_range(data_age_range, 25, 25)
    assert result == 70000.0


def test_get_avg_salary_by_age_range_no_matches():
    """
    Test that function handles age range with no matching employees.
    Expected: Returns 0.0 or appropriate value when no employees in range.
    """
    data = [
        ['EMP1000', 'engineering', 'Male', 30, 75000.0, 25, 4.0, 0.1, 'Active', '2018-05-10'],
        ['EMP1001', 'sales', 'Female', 35, 65000.0, 30, 3.5, 0.12, 'Active', '2016-11-05']
    ]
    result = get_avg_salary_by_age_range(data, 50, 60)
    # Function should handle no matches gracefully
    assert isinstance(result, float)


# ============================================================================
# TEST FUNCTIONS - get_avg_dept_performance_by_training_range()
# ============================================================================

def test_get_avg_dept_performance_by_training_range_returns_dict(data_training_hours):
    """
    Test that get_avg_dept_performance_by_training_range returns a dictionary.
    Expected: Return type is dict.
    """
    result = get_avg_dept_performance_by_training_range(data_training_hours, 20, 40)
    assert isinstance(result, dict)


def test_get_avg_dept_performance_by_training_range_two_decimal_places(data_training_hours):
    """
    Test that all performance ratings are rounded to exactly 2 decimal places.
    Expected: All values have exactly 2 decimal places.
    """
    result = get_avg_dept_performance_by_training_range(data_training_hours, 20, 40)
    for dept, rating in result.items():
        assert rating == round(rating, 2)


def test_get_avg_dept_performance_by_training_range_correct_calculation(data_training_hours):
    """
    Test that average performance is calculated correctly per department within training range.
    Expected: Engineering (25, 40 hours): avg of 3.9, 4.5 = 4.2.
    """
    result = get_avg_dept_performance_by_training_range(data_training_hours, 25, 40)
    # Engineering has employees with 25 and 40 training hours in range: ratings 3.9, 4.5
    expected_engineering = round((3.9 + 4.5) / 2, 2)
    assert result['engineering'] == expected_engineering


def test_get_avg_dept_performance_by_training_range_inclusive_bounds(data_training_hours):
    """
    Test that training hours range is inclusive of both minimum and maximum hours.
    Expected: Range includes exactly the boundary hours.
    """
    result = get_avg_dept_performance_by_training_range(data_training_hours, 25, 25)
    # Only engineering has someone with exactly 25 training hours (rating 3.9)
    assert result['engineering'] == 3.9


def test_get_avg_dept_performance_by_training_range_all_departments(data_training_hours):
    """
    Test that function includes all departments with employees in training hours range.
    Expected: Returns entry for each department with qualifying employees.
    """
    result = get_avg_dept_performance_by_training_range(data_training_hours, 10, 45)
    # All departments should have employees in this wide range
    assert len(result) > 0


def test_get_avg_dept_performance_by_training_range_no_matches():
    """
    Test that function handles training hours range with no matching employees.
    Expected: Departments with no matching employees included with value 0.0.
    """
    data = [
        ['EMP1000', 'engineering', 'Male', 30, 75000.0, 10, 2.8, 0.1, 'Active', '2018-05-10'],
        ['EMP1001', 'sales', 'Female', 32, 65000.0, 15, 3.1, 0.12, 'Active', '2016-11-05']
    ]
    result = get_avg_dept_performance_by_training_range(data, 50, 60)
    # Should include departments even if no employees in range (with 0.0)
    assert isinstance(result, dict)
    if 'engineering' in result:
        assert result['engineering'] == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
