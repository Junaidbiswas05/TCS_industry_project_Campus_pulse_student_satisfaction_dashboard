import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate 1200 entries
num_entries = 1200

# Create lists for different columns
# Academic years
academic_years = ['2021-2022', '2022-2023', '2023-2024', '2024-2025']

# Majors
majors = ['Computer Science', 'Mechanical Engineering', 'Electrical Engineering',
          'Civil Engineering', 'Business Administration', 'Biology',
          'Psychology', 'Mathematics', 'Physics', 'Chemistry',
          'English Literature', 'History', 'Economics', 'Architecture']

# Facilities to be rated
facilities = ['Library', 'Hostel', 'Cafeteria', 'Sports Complex',
              'Computer Lab', 'Classrooms', 'Medical Center',
              'Administration Office', 'Auditorium', 'Parking']

# Generate student IDs
student_ids = [f'STU{10000 + i}' for i in range(num_entries)]

# Generate data
data = []

for i in range(num_entries):
    student_id = student_ids[i]
    academic_year = np.random.choice(academic_years, p=[0.2, 0.3, 0.3, 0.2])
    major = np.random.choice(majors)
    facility_rated = np.random.choice(facilities)

    # Generate satisfaction score (1-5 scale) with some distribution pattern
    # Some facilities tend to have better/worse ratings
    if facility_rated in ['Library', 'Sports Complex', 'Computer Lab']:
        # These generally have higher ratings
        satisfaction_score = np.random.choice([4, 5], p=[0.3, 0.7])
    elif facility_rated in ['Hostel', 'Parking', 'Administration Office']:
        # These generally have lower ratings
        satisfaction_score = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
    else:
        # Balanced distribution for others
        satisfaction_score = np.random.randint(1, 6)

    # Generate timestamps (spread over last 4 years)
    year = int(academic_year[:4])
    month = np.random.randint(1, 13)
    day = np.random.randint(1, 29)
    hour = np.random.randint(9, 18)
    minute = np.random.randint(0, 60)
    second = np.random.randint(0, 60)

    timestamp = datetime(year, month, day, hour, minute, second)

    # Add some comments (optional field with some missing values)
    comments = ""
    if np.random.random() < 0.3:  # 30% chance of having a comment
        comment_templates = [
            f"Good experience with {facility_rated.lower()}",
            f"Needs improvement in {facility_rated.lower()}",
            f"Satisfactory services at {facility_rated.lower()}",
            f"Poor maintenance of {facility_rated.lower()}",
            f"Excellent facilities at {facility_rated.lower()}",
            f"Could be better at {facility_rated.lower()}",
            f"Very happy with {facility_rated.lower()} services",
            f"Disappointed with {facility_rated.lower()} condition"
        ]
        comments = np.random.choice(comment_templates)

    data.append({
        'student_id': student_id,
        'academic_year': academic_year,
        'major': major,
        'facility_rated': facility_rated,
        'satisfaction_score': satisfaction_score,
        'timestamp': timestamp,
        'comments': comments
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('campus_pulse_student_satisfaction.csv', index=False)

print(f"Dataset created with {len(df)} entries")
print("\nDataset Head:")
print(df.head())
print("\nDataset Info:")
print(df.info())
print("\nMissing Values:")
print(df.isnull().sum())
print("\nSatisfaction Score Distribution:")
print(df['satisfaction_score'].value_counts().sort_index())

# Generate summary statistics
print("\nSummary Statistics:")
print(f"Total records: {len(df)}")
print(f"Unique students: {df['student_id'].nunique()}")
print(f"Unique facilities: {df['facility_rated'].nunique()}")
print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Average satisfaction score: {df['satisfaction_score'].mean():.2f}")
