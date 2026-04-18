import pytest
import math
from datetime import datetime
from cleaner import (
    remove_null_salaries,
    standardize_departments,
    remove_invalid_performance_ratings,
    fix_format_dates,
    remove_invalid_dates
)


# ============================================================================
# FIXTURES - Sample Data for Testing
# ============================================================================

@pytest.fixture
def data_with_null_salaries():
    """
    Sample dataset containing records with null salaries (NaN values).
    Tests ability to identify and remove null salary entries.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2015-04-01'],
        ['EMP1001', 'Engineering', 'Male', 45, float('nan'), 16, 0.7, 0.08, 'Resigned', '2016-10-01'],
        ['EMP1002', 'Marketing', 'Non-binary', 30, 90000.0, 34, 2.5, 0.39, 'Active', '2016-12-01'],
        ['EMP1003', 'HR', 'Non-binary', 37, float('nan'), 30, 3.3, 0.01, 'Active', '2023-02-01'],
        ['EMP1004', 'Sales', 'Female', 28, 75000.0, 22, 4.1, 0.15, 'Active', '2018-05-15']
    ]


@pytest.fixture
def data_with_mixed_case_departments():
    """
    Sample dataset containing department names in various cases.
    Tests ability to standardize to lowercase.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2015-04-01'],
        ['EMP1001', 'ENGINEERING', 'Male', 45, 250000.0, 16, 0.7, 0.08, 'Resigned', '2016-10-01'],
        ['EMP1002', 'marketing', 'Non-binary', 30, 90000.0, 34, 2.5, 0.39, 'Active', '2016-12-01'],
        ['EMP1003', 'Sales', 'Non-binary', 37, 90000.0, 30, 3.3, 0.01, 'Active', '2023-02-01'],
        ['EMP1004', 'PrOdUcT', 'Female', 28, 75000.0, 22, 4.1, 0.15, 'Active', '2018-05-15']
    ]


@pytest.fixture
def data_with_invalid_ratings():
    """
    Sample dataset containing performance ratings outside the valid range [0, 5].
    Tests ability to identify and remove invalid rating entries.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2015-04-01'],
        ['EMP1001', 'Engineering', 'Male', 45, 250000.0, 16, 0.7, 0.08, 'Resigned', '2016-10-01'],
        ['EMP1002', 'Marketing', 'Non-binary', 30, 90000.0, 34, 25.5, 0.39, 'Active', '2016-12-01'],
        ['EMP1003', 'HR', 'Non-binary', 37, 90000.0, 30, 3.3, 0.01, 'Active', '2023-02-01'],
        ['EMP1004', 'Sales', 'Female', 28, 75000.0, 22, -1.5, 0.15, 'Active', '2018-05-15']
    ]


@pytest.fixture
def data_with_mixed_date_formats():
    """
    Sample dataset containing hire dates in different formats (YYYY-MM-DD and DD/MM/YYYY).
    Tests ability to convert dates to standard YYYY-MM-DD format.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2015-04-01'],
        ['EMP1001', 'Engineering', 'Male', 45, 250000.0, 16, 0.7, 0.08, 'Resigned', '15/10/2016'],
        ['EMP1002', 'Marketing', 'Non-binary', 30, 90000.0, 34, 2.5, 0.39, 'Active', '01/12/2016'],
        ['EMP1003', 'HR', 'Non-binary', 37, 90000.0, 30, 3.3, 0.01, 'Active', '2023-02-01'],
        ['EMP1004', 'Sales', 'Female', 28, 75000.0, 22, 4.1, 0.15, 'Active', '2018-05-15']
    ]


@pytest.fixture
def data_with_invalid_dates():
    """
    Sample dataset containing invalid hire dates (outside 2015-2025 range or logically invalid).
    Tests ability to identify and remove invalid date entries.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2014-04-01'],  # Before 2015
        ['EMP1001', 'Engineering', 'Male', 45, 250000.0, 16, 0.7, 0.08, 'Resigned', '2026-10-01'],  # After 2025
        ['EMP1002', 'Marketing', 'Non-binary', 30, 90000.0, 34, 2.5, 0.39, 'Active', '2023-02-29'],  # Invalid: 2023 not leap year
        ['EMP1003', 'HR', 'Non-binary', 37, 90000.0, 30, 3.3, 0.01, 'Active', '2021-03-05'],  # Valid
        ['EMP1004', 'Sales', 'Female', 28, 75000.0, 22, 4.1, 0.15, 'Active', '2022-13-05'],  # Invalid month
        ['EMP1005', 'Product', 'Male', 35, 95000.0, 25, 3.9, 0.12, 'Active', '2020-02-29']  # Valid: 2020 is leap year
    ]


@pytest.fixture
def data_no_nulls():
    """
    Sample dataset with no null salary entries.
    Tests that function works correctly when no nulls are present.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2015-04-01'],
        ['EMP1001', 'Engineering', 'Male', 45, 250000.0, 16, 0.7, 0.08, 'Resigned', '2016-10-01'],
        ['EMP1002', 'Marketing', 'Non-binary', 30, 90000.0, 34, 2.5, 0.39, 'Active', '2016-12-01']
    ]


@pytest.fixture
def data_all_nulls():
    """
    Sample dataset where all salary entries are null.
    Tests that function correctly removes all records.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, float('nan'), 31, 3.7, 0.23, 'Resigned', '2015-04-01'],
        ['EMP1001', 'Engineering', 'Male', 45, float('nan'), 16, 0.7, 0.08, 'Resigned', '2016-10-01'],
        ['EMP1002', 'Marketing', 'Non-binary', 30, float('nan'), 34, 2.5, 0.39, 'Active', '2016-12-01']
    ]


@pytest.fixture
def data_all_valid_ratings():
    """
    Sample dataset with all valid performance ratings.
    Tests that function doesn't remove any records when all ratings are valid.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 0.0, 0.23, 'Resigned', '2015-04-01'],
        ['EMP1001', 'Engineering', 'Male', 45, 250000.0, 16, 5.0, 0.08, 'Resigned', '2016-10-01'],
        ['EMP1002', 'Marketing', 'Non-binary', 30, 90000.0, 34, 2.5, 0.39, 'Active', '2016-12-01']
    ]


@pytest.fixture
def data_all_valid_dates():
    """
    Sample dataset with all valid hire dates in correct format.
    Tests that function doesn't remove any records when all dates are valid.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2015-01-01'],
        ['EMP1001', 'Engineering', 'Male', 45, 250000.0, 16, 0.7, 0.08, 'Resigned', '2020-06-15'],
        ['EMP1002', 'Marketing', 'Non-binary', 30, 90000.0, 34, 2.5, 0.39, 'Active', '2025-12-30']
    ]


@pytest.fixture
def data_feb_leap_year():
    """
    Sample dataset for testing February leap year validation.
    Tests edge cases around February dates in leap and non-leap years.
    """
    return [
        ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2020-02-29'],  # Valid leap year
        ['EMP1001', 'Engineering', 'Male', 45, 250000.0, 16, 0.7, 0.08, 'Resigned', '2021-02-28'],  # Valid non-leap
        ['EMP1002', 'Marketing', 'Non-binary', 30, 90000.0, 34, 2.5, 0.39, 'Active', '2024-02-29'],  # Valid leap year
        ['EMP1003', 'HR', 'Non-binary', 37, 90000.0, 30, 3.3, 0.01, 'Active', '2023-02-29']  # Invalid non-leap
    ]


# ============================================================================
# TEST FUNCTIONS - remove_null_salaries()
# ============================================================================

def test_remove_null_salaries_with_nulls(data_with_null_salaries):
    """
    Test that remove_null_salaries correctly removes records with NaN salaries.
    Expected: 3 records remain (2 had null salaries were removed).
    """
    original_length = len(data_with_null_salaries)
    data_with_null_salaries = remove_null_salaries(data_with_null_salaries)
    assert len(data_with_null_salaries) == 3
    # Verify no NaN values remain
    for record in data_with_null_salaries:
        assert not math.isnan(record[4])


def test_remove_null_salaries_no_nulls(data_no_nulls):
    """
    Test that remove_null_salaries doesn't remove anything when no nulls exist.
    Expected: All 3 records remain unchanged.
    """
    original_length = len(data_no_nulls)
    data_no_nulls = remove_null_salaries(data_no_nulls)
    assert len(data_no_nulls) == original_length


def test_remove_null_salaries_all_nulls(data_all_nulls):
    """
    Test that remove_null_salaries removes all records when all have null salaries.
    Expected: 0 records remain (all 3 were removed).
    """
    data_all_nulls = remove_null_salaries(data_all_nulls)
    assert len(data_all_nulls) == 0


def test_remove_null_salaries_preserves_data_integrity(data_with_null_salaries):
    """
    Test that remove_null_salaries preserves the integrity of non-null records.
    Expected: Remaining records are unmodified (all fields intact).
    """
    data_with_null_salaries = remove_null_salaries(data_with_null_salaries)
    # Check first record is preserved exactly
    assert data_with_null_salaries[0] == ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2015-04-01']


# ============================================================================
# TEST FUNCTIONS - standardize_departments()
# ============================================================================

def test_standardize_departments_mixed_case(data_with_mixed_case_departments):
    """
    Test that standardize_departments converts all department names to lowercase.
    Expected: All department names at index 1 are lowercase.
    """
    standardize_departments(data_with_mixed_case_departments)
    for record in data_with_mixed_case_departments:
        assert record[1] == record[1].lower()


def test_standardize_departments_already_lowercase(data_with_mixed_case_departments):
    """
    Test that departments already in lowercase remain unchanged.
    Expected: 'engineering' stays as 'engineering', 'marketing' stays as 'marketing'.
    """
    standardize_departments(data_with_mixed_case_departments)
    assert data_with_mixed_case_departments[2][1] == 'marketing'


def test_standardize_departments_preserves_other_fields(data_with_mixed_case_departments):
    """
    Test that standardize_departments only modifies department names, not other fields.
    Expected: All other fields (employee ID, gender, salary, etc.) remain unchanged.
    """
    original_first_record = data_with_mixed_case_departments[0][:]
    standardize_departments(data_with_mixed_case_departments)
    # Check that only index 1 (department) changed
    assert data_with_mixed_case_departments[0][0] == original_first_record[0]  # Employee ID
    assert data_with_mixed_case_departments[0][2] == original_first_record[2]  # Gender
    assert data_with_mixed_case_departments[0][4] == original_first_record[4]  # Salary


def test_standardize_departments_returns_none(data_with_mixed_case_departments):
    """
    Test that standardize_departments returns None (modifies in place).
    Expected: Function returns None.
    """
    result = standardize_departments(data_with_mixed_case_departments)
    assert result is None


# ============================================================================
# TEST FUNCTIONS - remove_invalid_performance_ratings()
# ============================================================================

def test_remove_invalid_ratings_with_invalid(data_with_invalid_ratings):
    """
    Test that remove_invalid_performance_ratings correctly removes records with ratings outside [0, 5].
    Expected: 3 records remain (2 had invalid ratings and were removed).
    """
    original_length = len(data_with_invalid_ratings)
    data_with_invalid_ratings = remove_invalid_performance_ratings(data_with_invalid_ratings)
    assert len(data_with_invalid_ratings) == 3
    # Verify all remaining ratings are in valid range
    for record in data_with_invalid_ratings:
        assert 0 <= record[6] <= 5


def test_remove_invalid_ratings_all_valid(data_all_valid_ratings):
    """
    Test that remove_invalid_performance_ratings doesn't remove anything when all ratings are valid.
    Expected: All 3 records remain unchanged.
    """
    original_length = len(data_all_valid_ratings)
    data_all_valid_ratings = remove_invalid_performance_ratings(data_all_valid_ratings)
    assert len(data_all_valid_ratings) == original_length


def test_remove_invalid_ratings_boundary_values(data_all_valid_ratings):
    """
    Test that boundary values (0.0 and 5.0) are correctly treated as valid.
    Expected: Records with ratings of 0.0 and 5.0 are preserved.
    """
    data_all_valid_ratings = remove_invalid_performance_ratings(data_all_valid_ratings)
    # Check that boundaries are preserved
    assert any(record[6] == 0.0 for record in data_all_valid_ratings)
    assert any(record[6] == 5.0 for record in data_all_valid_ratings)


def test_remove_invalid_ratings_preserves_data_integrity(data_with_invalid_ratings):
    """
    Test that remove_invalid_performance_ratings preserves the integrity of valid records.
    Expected: Remaining records are unmodified.
    """
    data_with_invalid_ratings = remove_invalid_performance_ratings(data_with_invalid_ratings)
    assert data_with_invalid_ratings[0] == ['EMP1000', 'HR', 'Male', 46, 140000.0, 31, 3.7, 0.23, 'Resigned', '2015-04-01']


# ============================================================================
# TEST FUNCTIONS - fix_format_dates()
# ============================================================================

def test_fix_format_dates_converts_dd_mm_yyyy(data_with_mixed_date_formats):
    """
    Test that fix_format_dates converts DD/MM/YYYY format to YYYY-MM-DD.
    Expected: '15/10/2016' becomes '2016-10-15', '01/12/2016' becomes '2016-12-01'.
    """
    fix_format_dates(data_with_mixed_date_formats)
    assert data_with_mixed_date_formats[1][9] == '2016-10-15'
    assert data_with_mixed_date_formats[2][9] == '2016-12-01'


def test_fix_format_dates_preserves_yyyy_mm_dd(data_with_mixed_date_formats):
    """
    Test that fix_format_dates preserves dates already in YYYY-MM-DD format.
    Expected: Dates already in correct format remain unchanged.
    """
    fix_format_dates(data_with_mixed_date_formats)
    assert data_with_mixed_date_formats[0][9] == '2015-04-01'
    assert data_with_mixed_date_formats[3][9] == '2023-02-01'


def test_fix_format_dates_preserves_other_fields(data_with_mixed_date_formats):
    """
    Test that fix_format_dates only modifies hire dates, not other fields.
    Expected: All fields except index 9 (hire date) remain unchanged.
    """
    original_first_record = data_with_mixed_date_formats[0][:]
    fix_format_dates(data_with_mixed_date_formats)
    for i in range(9):
        assert data_with_mixed_date_formats[0][i] == original_first_record[i]


def test_fix_format_dates_returns_none(data_with_mixed_date_formats):
    """
    Test that fix_format_dates returns None (modifies in place).
    Expected: Function returns None.
    """
    result = fix_format_dates(data_with_mixed_date_formats)
    assert result is None


# ============================================================================
# TEST FUNCTIONS - remove_invalid_dates()
# ============================================================================

def test_remove_invalid_dates_with_invalid(data_with_invalid_dates):
    """
    Test that remove_invalid_dates correctly removes records with invalid hire dates.
    Expected: 2 records remain (4 had invalid dates and were removed).
    """
    original_length = len(data_with_invalid_dates)
    data_with_invalid_dates = remove_invalid_dates(data_with_invalid_dates)
    assert len(data_with_invalid_dates) == 2


def test_remove_invalid_dates_year_before_2015(data_with_invalid_dates):
    """
    Test that remove_invalid_dates removes entries with year before 2015.
    Expected: Records with dates before 2015-01-01 are removed.
    """
    data_with_invalid_dates = remove_invalid_dates(data_with_invalid_dates)
    for record in data_with_invalid_dates:
        year = int(record[9].split('-')[0])
        assert year >= 2015


def test_remove_invalid_dates_year_after_2025(data_with_invalid_dates):
    """
    Test that remove_invalid_dates removes entries with year after 2025.
    Expected: Records with dates after 2025-12-31 are removed.
    """
    data_with_invalid_dates = remove_invalid_dates(data_with_invalid_dates)
    for record in data_with_invalid_dates:
        year = int(record[9].split('-')[0])
        assert year <= 2025


def test_remove_invalid_dates_leap_year_validation(data_feb_leap_year):
    """
    Test that remove_invalid_dates correctly validates February dates in leap/non-leap years.
    Expected: Feb 29 in non-leap years is removed, Feb 29 in leap years is kept.
    """
    data_feb_leap_year = remove_invalid_dates(data_feb_leap_year)
    # Should have 3 records (2020 and 2024 are leap years, 2023 is not)
    assert len(data_feb_leap_year) == 3
    # Check that 2023-02-29 was removed
    assert not any('2023-02-29' in record[9] for record in data_feb_leap_year)


def test_remove_invalid_dates_invalid_month(data_with_invalid_dates):
    """
    Test that remove_invalid_dates removes entries with invalid months.
    Expected: Records with months < 1 or > 12 are removed.
    """
    data_with_invalid_dates = remove_invalid_dates(data_with_invalid_dates)
    for record in data_with_invalid_dates:
        month = int(record[9].split('-')[1])
        assert 1 <= month <= 12


def test_remove_invalid_dates_all_valid(data_all_valid_dates):
    """
    Test that remove_invalid_dates doesn't remove anything when all dates are valid.
    Expected: All 3 records remain unchanged.
    """
    original_length = len(data_all_valid_dates)
    data_all_valid_dates = remove_invalid_dates(data_all_valid_dates)
    assert len(data_all_valid_dates) == original_length


def test_remove_invalid_dates_boundary_years(data_all_valid_dates):
    """
    Test that boundary years (2015 and 2025) are correctly treated as valid.
    Expected: Records with year 2015 and 2025 are preserved.
    """
    data_all_valid_dates = remove_invalid_dates(data_all_valid_dates)
    years = [int(record[9].split('-')[0]) for record in data_all_valid_dates]
    assert 2015 in years or 2025 in years  # At least one boundary is present


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
