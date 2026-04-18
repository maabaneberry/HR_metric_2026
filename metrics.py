import math
from datetime import datetime
from helper import read_hr_data


def get_department_headcount(data):
    # Count by department so we get a simple workforce size summary for each team.
    headcount = {}
    for entry in data:
        department = entry[1]
        if department not in headcount:
            headcount[department] = 1
        else:
            headcount[department] += 1

    return headcount


def get_unique_departments(data):
    # A set removes duplicates automatically, which is the simplest way to list departments once.
    set_departments = set()
    for entry in data:
        set_departments.add(entry[1])
    return set_departments


def get_gender_distribution(data):
    # Use nested dictionaries so each department can store its own gender counts and percentages.
    distribution = {}
    departments = get_unique_departments(data)
    for department in departments:
        distribution[department] = {}

    for entry in data:
        gender = entry[2]
        department = entry[1]
        if gender not in distribution[department]:
            distribution[department][gender] = 1
        else:
            distribution[department][gender] += 1

    for department, gender_dist in distribution.items():
        # Convert counts to percentages so departments of different sizes can be compared fairly.
        count_total = 0
        for gender, count in gender_dist.items():
            count_total += count

        for gender, count in gender_dist.items():
            gender_dist[gender] /= count_total
            gender_dist[gender] *= 100
            # Round to 2 decimals to match the assignment output format.
            gender_dist[gender] = round(gender_dist[gender], 2)

    return distribution


def get_avg_age_by_department(data):
    # Store a running total and count so each department average can be calculated efficiently.
    distribution = {}
    for entry in data:
        department = entry[1]
        age = entry[3]
        if department not in distribution:
            distribution[department] = [age, 1]
        else:
            distribution[department][0] += age
            distribution[department][1] += 1

    for department, array in distribution.items():
        # Round to 2 decimals so the result format stays consistent across metrics.
        distribution[department] = round(array[0] / array[1], 2)

    return distribution


def get_avg_salary_by_department(data):
    # Use totals and counts per department because average salary is a grouped aggregate.
    distribution = {}
    for entry in data:
        department = entry[1]
        salary = entry[4]
        if department not in distribution:
            distribution[department] = [salary, 1]
        else:
            distribution[department][0] += salary
            distribution[department][1] += 1

    for department, array in distribution.items():
        # Round to 2 decimals so salary outputs are easy to compare and report.
        distribution[department] = round(array[0] / array[1], 2)

    return distribution


def get_salary_dispersion_by_department(data):
    # Collect all salaries per department first because spread metrics need the full salary list.
    salaries_by_department = {}
    dispersion = {}

    for entry in data:
        department = entry[1]
        salary = entry[4]
        if department not in salaries_by_department:
            salaries_by_department[department] = [salary]
        else:
            salaries_by_department[department].append(salary)

    for department, salaries in salaries_by_department.items():
        # Variance and standard deviation show how widely salaries are spread within a department.
        avg_salary = sum(salaries) / len(salaries)
        variance = 0
        for salary in salaries:
            variance += (salary - avg_salary) ** 2
        variance /= len(salaries)

        dispersion[department] = {
            'min_salary': round(min(salaries), 2),
            'max_salary': round(max(salaries), 2),
            'salary_range': round(max(salaries) - min(salaries), 2),
            'std_dev': round(math.sqrt(variance), 2)
        }

    return dispersion


def get_avg_performance_by_department(data):
    # Group by department so we can compare typical performance across teams.
    distribution = {}
    for entry in data:
        department = entry[1]
        rating = entry[6]
        if department not in distribution:
            distribution[department] = [rating, 1]
        else:
            distribution[department][0] += rating
            distribution[department][1] += 1

    for department, array in distribution.items():
        # Round to 2 decimals to keep performance summaries consistent.
        distribution[department] = round(array[0] / array[1], 2)

    return distribution


def get_avg_training_hours_by_department(data):
    # Group training hours by department to compare development effort between teams.
    distribution = {}
    for entry in data:
        department = entry[1]
        training_hours = entry[5]
        if department not in distribution:
            distribution[department] = [training_hours, 1]
        else:
            distribution[department][0] += training_hours
            distribution[department][1] += 1

    for department, array in distribution.items():
        # Round to 2 decimals so the reported averages are consistent.
        distribution[department] = round(array[0] / array[1], 2)

    return distribution


def get_retention_rate(data):
    # Count active employees against the full dataset because retention is an overall proportion.
    active = 0
    total = 0
    for entry in data:
        if entry[8].lower() == "active":
            active += 1
            total += 1
        else:
            total += 1

    # Return a percentage so the result is easy to interpret in the report.
    return round(active / total * 100, 2)


def get_retention_rate_by_department(data):
    # Track active and total employees per department so retention problems can be located by team.
    distribution = {}
    for entry in data:
        department = entry[1]
        status = entry[8]
        if status.lower() == "active":
            if department not in distribution:
                distribution[department] = [1, 1]
            else:
                distribution[department][0] += 1
                distribution[department][1] += 1
        else:
            if department not in distribution:
                distribution[department] = [0, 1]
            else:
                distribution[department][1] += 1

    for department, array in distribution.items():
        # Convert to a percentage so departments can be compared even when sizes differ.
        distribution[department] = round(array[0] / array[1] * 100, 2)

    return distribution


def get_turnover_rate_by_department(data):
    # Track resigned and total employees per department to measure turnover at team level.
    distribution = {}
    for entry in data:
        department = entry[1]
        status = entry[8]
        if status.lower() == "resigned":
            if department not in distribution:
                distribution[department] = [1, 1]
            else:
                distribution[department][0] += 1
                distribution[department][1] += 1
        else:
            if department not in distribution:
                distribution[department] = [0, 1]
            else:
                distribution[department][1] += 1

    for department, array in distribution.items():
        # Use percentages so turnover is comparable across departments.
        distribution[department] = round(array[0] / array[1] * 100, 2)

    return distribution


def get_avg_salary_by_age_range(data, min_age, max_age):
    # Filter by an inclusive age range because the question asks for employees within the range.
    salary = 0
    count = 0
    for entry in data:
        if min_age <= entry[3] <= max_age:
            salary += entry[4]
            count += 1

    if count == 0:
        # Return 0.0 when no records match so the function handles empty ranges safely.
        return round(0.0, 2)
    return round(salary / count, 2)


def get_avg_dept_performance_by_training_range(data, min_hours, max_hours):
    # Filter by training range first, then group by department to compare training-linked performance.
    distribution = {}
    for entry in data:
        department = entry[1]
        rating = entry[6]
        hours = entry[5]
        if min_hours <= hours <= max_hours:
            if department not in distribution:
                distribution[department] = [rating, 1]
            else:
                distribution[department][0] += rating
                distribution[department][1] += 1

    for department, array in distribution.items():
        # Round to 2 decimals so departmental averages are easy to report.
        distribution[department] = round(array[0] / array[1], 2)

    return distribution


def get_avg_overtime_by_status(data):
    # Group by employment status to check whether overtime patterns differ for active and resigned staff.
    distribution = {}
    for entry in data:
        status = entry[8]
        overtime_ratio = entry[7]
        if status not in distribution:
            distribution[status] = [overtime_ratio, 1]
        else:
            distribution[status][0] += overtime_ratio
            distribution[status][1] += 1

    for status, array in distribution.items():
        # Round to 2 decimals for a clear summary metric.
        distribution[status] = round(array[0] / array[1], 2)

    return distribution


def get_salary_by_gender_within_department(data):
    # Group by department first to make gender salary comparisons fair within the same team.
    distribution = {}
    for entry in data:
        department = entry[1]
        gender = entry[2]
        salary = entry[4]

        if department not in distribution:
            distribution[department] = {}

        if gender not in distribution[department]:
            distribution[department][gender] = [salary, 1]
        else:
            distribution[department][gender][0] += salary
            distribution[department][gender][1] += 1

    for department, gender_distribution in distribution.items():
        for gender, array in gender_distribution.items():
            # Average within each subgroup so the result reflects typical pay, not total pay.
            gender_distribution[gender] = round(array[0] / array[1], 2)

    return distribution


def get_avg_tenure_by_status(data, reference_date=None):
    # Use a reference date so tenure is measured from a consistent endpoint.
    if reference_date is None:
        reference_date = datetime.today()

    distribution = {}
    for entry in data:
        status = entry[8]
        hire_date = datetime.strptime(entry[9], "%Y-%m-%d")
        # Use 365.25 to account for leap years in a simple, readable way.
        tenure_years = (reference_date - hire_date).days / 365.25

        if status not in distribution:
            distribution[status] = [tenure_years, 1]
        else:
            distribution[status][0] += tenure_years
            distribution[status][1] += 1

    for status, array in distribution.items():
        # Average tenure by status helps compare whether one group tends to stay longer.
        distribution[status] = round(array[0] / array[1], 2)

    return distribution


if __name__ == "__main__":
    # Load cleaned data from CSV file
    data = read_hr_data('cleaned_dataset.csv')
    print(f"Loaded {len(data)} employee records\n")

    print("=" * 70)
    print("METRICS CALCULATION")
    print("=" * 70)

    # Test metrics functions
    # Uncomment the lines below to test each metrics function
    # You can modify the function arguments to test different inputs

    # 1. Get unique departments
    depts = get_unique_departments(data)
    print(f"\nUnique departments: {depts}")

    # 2. Get department headcount
    headcount = get_department_headcount(data)
    print(f"\nDepartment headcount:")
    for dept, count in headcount.items():
        print(f"  {dept}: {count}")

    # 3. Get gender distribution per department
    gender_dist = get_gender_distribution(data)
    print(f"\nGender distribution by department:")
    for dept, dist in gender_dist.items():
        print(f"  {dept}: {dist}")

    # 4. Get average age per department
    avg_age = get_avg_age_by_department(data)
    print(f"\nAverage age by department:")
    for dept, age in avg_age.items():
        print(f"  {dept}: {age}")

    # 5. Get average salary per department
    avg_salary = get_avg_salary_by_department(data)
    print(f"\nAverage salary by department:")
    for dept, salary in avg_salary.items():
        print(f"  {dept}: R{salary}")

    # 6. Get salary dispersion per department
    salary_dispersion = get_salary_dispersion_by_department(data)
    print(f"\nSalary dispersion by department:")
    for dept, spread in salary_dispersion.items():
        print(f"  {dept}: {spread}")

    # 7. Get average performance rating per department
    avg_performance = get_avg_performance_by_department(data)
    print(f"\nAverage performance by department:")
    for dept, rating in avg_performance.items():
        print(f"  {dept}: {rating}")

    # 8. Get average training hours per department
    avg_training = get_avg_training_hours_by_department(data)
    print(f"\nAverage training hours by department:")
    for dept, hours in avg_training.items():
        print(f"  {dept}: {hours}")

    # 9. Get retention rate
    retention = get_retention_rate(data)
    print(f"\nOverall retention rate: {retention}%")

    # 10. Get retention rate per department
    retention_by_department = get_retention_rate_by_department(data)
    print(f"\nRetention rate by department:")
    for dept, rate in retention_by_department.items():
        print(f"  {dept}: {rate}%")

    # 11. Get turnover rate per department
    turnover = get_turnover_rate_by_department(data)
    print(f"\nTurnover rate by department:")
    for dept, rate in turnover.items():
        print(f"  {dept}: {rate}%")

    # 12. Get average salary for age range
    avg_sal_age = get_avg_salary_by_age_range(data, 25, 35)
    print(f"\nAverage salary for employees aged 25-35: R{avg_sal_age}")

    # 13. Get average department performance by training hours range
    avg_perf_training = get_avg_dept_performance_by_training_range(data, 20, 40)
    print(f"\nAverage performance rating by department for employees with 20-40 training hours:")
    for dept, rating in avg_perf_training.items():
        print(f"  {dept}: {rating}")

    # 14. Get average overtime ratio by employee status
    overtime_by_status = get_avg_overtime_by_status(data)
    print(f"\nAverage overtime ratio by status:")
    for status, overtime in overtime_by_status.items():
        print(f"  {status}: {overtime}")

    # 15. Get average salary by gender within each department
    salary_by_gender = get_salary_by_gender_within_department(data)
    print(f"\nAverage salary by gender within department:")
    for dept, salaries in salary_by_gender.items():
        print(f"  {dept}: R{salaries}")

    # 16. Get average tenure in years by employee status
    tenure_by_status = get_avg_tenure_by_status(data)
    print(f"\nAverage tenure by status:")
    for status, tenure in tenure_by_status.items():
        print(f"  {status}: {tenure} years")
