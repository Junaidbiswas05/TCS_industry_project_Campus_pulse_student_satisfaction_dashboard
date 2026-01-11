import pandas as pd
import numpy as np
from datetime import datetime
import json

class DataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and preprocess data"""
        try:
            self.df = pd.read_csv(self.data_path)
            
            # Ensure proper data types
            if 'timestamp' in self.df.columns:
                self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
                self.df['year'] = self.df['timestamp'].dt.year
                self.df['month'] = self.df['timestamp'].dt.month
                self.df['day_name'] = self.df['timestamp'].dt.day_name()
                self.df['hour'] = self.df['timestamp'].dt.hour
            
            # Categorize satisfaction scores
            if 'satisfaction_score' in self.df.columns:
                self.df['satisfaction_category'] = self.df['satisfaction_score'].apply(
                    lambda x: 'Low' if x <= 2 else ('Medium' if x <= 3 else 'High')
                )
                
            print(f"Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            # Create sample data if file not found
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data if file not found"""
        np.random.seed(42)
        num_entries = 1000
        
        data = {
            'student_id': [f'STU{10000 + i}' for i in range(num_entries)],
            'academic_year': np.random.choice(['2021-2022', '2022-2023', '2023-2024'], num_entries),
            'major': np.random.choice(['Computer Science', 'Mechanical', 'Electrical', 'Civil', 'Business'], num_entries),
            'facility_rated': np.random.choice(['Library', 'Hostel', 'Cafeteria', 'Sports', 'Lab'], num_entries),
            'satisfaction_score': np.random.randint(1, 6, num_entries),
            'timestamp': pd.date_range(start='2021-01-01', periods=num_entries, freq='H'),
        }
        
        self.df = pd.DataFrame(data)
        print(f"Sample data created: {self.df.shape[0]} rows")
    
    def get_overall_metrics(self):
        """Calculate overall metrics"""
        if self.df is None or self.df.empty:
            return {}
        
        total_ratings = len(self.df)
        avg_score = self.df['satisfaction_score'].mean()
        median_score = self.df['satisfaction_score'].median()
        std_score = self.df['satisfaction_score'].std()
        
        # Score distribution
        score_counts = self.df['satisfaction_score'].value_counts().sort_index()
        score_distribution = {
            str(score): int(count) for score, count in score_counts.items()
        }
        
        # Category distribution
        if 'satisfaction_category' in self.df.columns:
            category_counts = self.df['satisfaction_category'].value_counts()
            category_distribution = {
                category: int(count) for category, count in category_counts.items()
            }
        else:
            category_distribution = {}
        
        return {
            'total_ratings': int(total_ratings),
            'average_score': float(round(avg_score, 2)),
            'median_score': float(round(median_score, 2)),
            'std_deviation': float(round(std_score, 2)),
            'score_distribution': score_distribution,
            'category_distribution': category_distribution,
            'date_range': {
                'start': str(self.df['timestamp'].min()) if 'timestamp' in self.df.columns else None,
                'end': str(self.df['timestamp'].max()) if 'timestamp' in self.df.columns else None
            }
        }
    
    def get_facility_metrics(self):
        """Calculate facility-wise metrics"""
        if self.df is None or self.df.empty:
            return []
        
        facility_stats = self.df.groupby('facility_rated').agg({
            'satisfaction_score': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        
        # Flatten column names
        facility_stats.columns = ['_'.join(col).strip() for col in facility_stats.columns.values]
        
        # Convert to list of dictionaries
        facilities = []
        for facility, row in facility_stats.iterrows():
            facilities.append({
                'facility': str(facility),
                'total_ratings': int(row['satisfaction_score_count']),
                'average_score': float(row['satisfaction_score_mean']),
                'std_deviation': float(row['satisfaction_score_std']),
                'min_score': float(row['satisfaction_score_min']),
                'max_score': float(row['satisfaction_score_max']),
                'rank': 0  # Will be updated after sorting
            })
        
        # Sort by average score and assign ranks
        facilities.sort(key=lambda x: x['average_score'], reverse=True)
        for i, facility in enumerate(facilities, 1):
            facility['rank'] = i
        
        return facilities
    
    def get_year_metrics(self):
        """Calculate year-wise metrics"""
        if self.df is None or self.df.empty or 'academic_year' not in self.df.columns:
            return []
        
        year_stats = self.df.groupby('academic_year').agg({
            'satisfaction_score': ['count', 'mean', 'std']
        }).round(2)
        
        years = []
        for year, row in year_stats.iterrows():
            years.append({
                'academic_year': str(year),
                'total_ratings': int(row[('satisfaction_score', 'count')]),
                'average_score': float(row[('satisfaction_score', 'mean')]),
                'std_deviation': float(row[('satisfaction_score', 'std')])
            })
        
        return years
    
    def get_major_metrics(self):
        """Calculate major-wise metrics"""
        if self.df is None or self.df.empty or 'major' not in self.df.columns:
            return []
        
        major_stats = self.df.groupby('major').agg({
            'satisfaction_score': ['count', 'mean', 'std']
        }).round(2)
        
        majors = []
        for major, row in major_stats.iterrows():
            majors.append({
                'major': str(major),
                'total_ratings': int(row[('satisfaction_score', 'count')]),
                'average_score': float(row[('satisfaction_score', 'mean')]),
                'std_deviation': float(row[('satisfaction_score', 'std')])
            })
        
        # Sort by total ratings
        majors.sort(key=lambda x: x['total_ratings'], reverse=True)
        return majors[:10]  # Return top 10 only
    
    def get_time_metrics(self):
        """Calculate time-based metrics"""
        if self.df is None or self.df.empty or 'hour' not in self.df.columns:
            return {}
        
        # Time of day categories
        def categorize_time(hour):
            if 5 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 17:
                return 'Afternoon'
            elif 17 <= hour < 22:
                return 'Evening'
            else:
                return 'Night'
        
        self.df['time_of_day'] = self.df['hour'].apply(categorize_time)
        
        time_stats = self.df.groupby('time_of_day').agg({
            'satisfaction_score': ['count', 'mean']
        }).round(2)
        
        time_data = {}
        for time, row in time_stats.iterrows():
            time_data[str(time)] = {
                'total_ratings': int(row[('satisfaction_score', 'count')]),
                'average_score': float(row[('satisfaction_score', 'mean')])
            }
        
        return time_data
    
    def get_filtered_data(self, filters):
        """Get filtered data based on user input"""
        filtered_df = self.df.copy()

        # Apply filters
        if 'facility' in filters and filters['facility']:
            filtered_df = filtered_df[filtered_df['facility_rated'].str.lower() == filters['facility'].lower()]

        if 'year' in filters and filters['year']:
            filtered_df = filtered_df[filtered_df['academic_year'].str.lower() == filters['year'].lower()]

        if 'major' in filters and filters['major']:
            filtered_df = filtered_df[filtered_df['major'].str.lower() == filters['major'].lower()]

        if 'score_range' in filters and filters['score_range']:
            try:
                min_score, max_score = map(int, filters['score_range'].split('-'))
                filtered_df = filtered_df[
                    (filtered_df['satisfaction_score'] >= min_score) &
                    (filtered_df['satisfaction_score'] <= max_score)
                ]
            except ValueError:
                # If score_range is not in 'min-max' format, skip the filter
                pass

        return filtered_df.to_dict('records')

    def calculate_overall_metrics_from_df(self, df):
        """Calculate overall metrics from a given dataframe"""
        if df is None or df.empty:
            return {
                'total_ratings': 0,
                'average_score': 0.0,
                'median_score': 0.0,
                'std_deviation': 0.0,
                'score_distribution': {},
                'category_distribution': {},
                'date_range': {'start': None, 'end': None}
            }

        total_ratings = len(df)
        avg_score = df['satisfaction_score'].mean()
        median_score = df['satisfaction_score'].median()
        std_score = df['satisfaction_score'].std()

        # Score distribution
        score_counts = df['satisfaction_score'].value_counts().sort_index()
        score_distribution = {
            str(score): int(count) for score, count in score_counts.items()
        }

        # Category distribution
        if 'satisfaction_category' in df.columns:
            category_counts = df['satisfaction_category'].value_counts()
            category_distribution = {
                category: int(count) for category, count in category_counts.items()
            }
        else:
            category_distribution = {}

        return {
            'total_ratings': int(total_ratings),
            'average_score': float(round(avg_score, 2)),
            'median_score': float(round(median_score, 2)),
            'std_deviation': float(round(std_score, 2)),
            'score_distribution': score_distribution,
            'category_distribution': category_distribution,
            'date_range': {
                'start': str(df['timestamp'].min()) if 'timestamp' in df.columns else None,
                'end': str(df['timestamp'].max()) if 'timestamp' in df.columns else None
            }
        }

    def calculate_facility_metrics_from_df(self, df):
        """Calculate facility metrics from a given dataframe"""
        if df is None or df.empty or 'facility_rated' not in df.columns:
            return []

        facility_stats = df.groupby('facility_rated').agg({
            'satisfaction_score': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)

        # Flatten column names
        facility_stats.columns = ['_'.join(col).strip() for col in facility_stats.columns.values]

        # Convert to list of dictionaries
        facilities = []
        for facility, row in facility_stats.iterrows():
            facilities.append({
                'facility': str(facility),
                'total_ratings': int(row['satisfaction_score_count']),
                'average_score': float(row['satisfaction_score_mean']),
                'std_deviation': float(row['satisfaction_score_std']),
                'min_score': float(row['satisfaction_score_min']),
                'max_score': float(row['satisfaction_score_max']),
                'rank': 0  # Will be updated after sorting
            })

        # Sort by average score and assign ranks
        facilities.sort(key=lambda x: x['average_score'], reverse=True)
        for i, facility in enumerate(facilities, 1):
            facility['rank'] = i

        return facilities

    def calculate_year_metrics_from_df(self, df):
        """Calculate year metrics from a given dataframe"""
        if df is None or df.empty or 'academic_year' not in df.columns:
            return []

        year_stats = df.groupby('academic_year').agg({
            'satisfaction_score': ['count', 'mean', 'std']
        }).round(2)

        years = []
        for year, row in year_stats.iterrows():
            years.append({
                'academic_year': str(year),
                'total_ratings': int(row[('satisfaction_score', 'count')]),
                'average_score': float(row[('satisfaction_score', 'mean')]),
                'std_deviation': float(row[('satisfaction_score', 'std')])
            })

        return years

    def calculate_major_metrics_from_df(self, df):
        """Calculate major metrics from a given dataframe"""
        if df is None or df.empty or 'major' not in df.columns:
            return []

        major_stats = df.groupby('major').agg({
            'satisfaction_score': ['count', 'mean', 'std']
        }).round(2)

        majors = []
        for major, row in major_stats.iterrows():
            majors.append({
                'major': str(major),
                'total_ratings': int(row[('satisfaction_score', 'count')]),
                'average_score': float(row[('satisfaction_score', 'mean')]),
                'std_deviation': float(row[('satisfaction_score', 'std')])
            })

        # Sort by total ratings
        majors.sort(key=lambda x: x['total_ratings'], reverse=True)
        return majors[:10]  # Return top 10 only

    def calculate_time_metrics_from_df(self, df):
        """Calculate time metrics from a given dataframe"""
        if df is None or df.empty or 'hour' not in df.columns:
            return {}

        # Time of day categories
        def categorize_time(hour):
            if 5 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 17:
                return 'Afternoon'
            elif 17 <= hour < 22:
                return 'Evening'
            else:
                return 'Night'

        df_copy = df.copy()
        df_copy['time_of_day'] = df_copy['hour'].apply(categorize_time)

        time_stats = df_copy.groupby('time_of_day').agg({
            'satisfaction_score': ['count', 'mean']
        }).round(2)

        time_data = {}
        for time, row in time_stats.iterrows():
            time_data[str(time)] = {
                'total_ratings': int(row[('satisfaction_score', 'count')]),
                'average_score': float(row[('satisfaction_score', 'mean')])
            }

        return time_data
