import math
from datetime import datetime


def read_hr_data(filename):
    """
    Read HR data from CSV file and return as a list of lists.
    
    The CSV file should have the following columns (in order):
    0. Employee_ID (string)
    1. Department (string)
    2. Gender (string)
    3. Age (integer)
    4. Salary (float)
    5. Training_Hours (integer)
    6. Performance_Rating (float)
    7. Overtime_Ratio (float)
    8. Status (string)
    9. Hire_Date (string)
    
    Args:
        filename (str): Path to the HR data CSV file
        
    Returns:
        list: A 2D list where each inner list represents one employee record
    """
    data = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        # Skip header row (index 0)
        for line in lines[1:]:
            row = line.strip().split(',')
            
            # Convert numeric columns to appropriate types
            row[3] = int(row[3])  # Age to integer
            
            try:
                row[4] = float(row[4])  # Salary to float
            except ValueError:
                row[4] = float('nan')  # Mark as NaN if invalid
            
            try:
                row[5] = int(row[5])  # Training_Hours to integer
            except ValueError:
                row[5] = 0
            
            try:
                row[6] = float(row[6])  # Performance_Rating to float
            except ValueError:
                row[6] = float('nan')
            
            try:
                row[7] = float(row[7])  # Overtime_Ratio to float
            except ValueError:
                row[7] = 0.0
            
            data.append(row)
    
    return data
