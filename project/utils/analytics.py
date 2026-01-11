import pandas as pd
import numpy as np
from datetime import datetime

class AnalyticsEngine:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.df = data_processor.df
    
    def get_trend_analysis(self):
        """Analyze trends over time"""
        if self.df is None or self.df.empty or 'timestamp' not in self.df.columns:
            return {}
        
        # Monthly trend
        self.df['month_year'] = self.df['timestamp'].dt.to_period('M').astype(str)
        monthly_trend = self.df.groupby('month_year')['satisfaction_score'].mean().reset_index()
        
        # Convert to list for chart
        trend_data = {
            'labels': monthly_trend['month_year'].tolist(),
            'scores': monthly_trend['satisfaction_score'].round(2).tolist()
        }
        
        return trend_data
    
    def get_correlation_analysis(self):
        """Calculate correlations between variables"""
        if self.df is None or self.df.empty:
            return {}
        
        # Create correlation matrix
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            correlation_matrix = self.df[numeric_cols].corr().round(3)
            
            # Convert to dictionary
            correlations = {}
            for col in correlation_matrix.columns:
                correlations[col] = correlation_matrix[col].to_dict()
            
            return correlations
        
        return {}
    
    def get_insights(self):
        """Generate actionable insights"""
        if self.df is None or self.df.empty:
            return []
        
        insights = []
        
        # Facility insights
        facility_stats = self.df.groupby('facility_rated')['satisfaction_score'].mean()
        best_facility = facility_stats.idxmax()
        worst_facility = facility_stats.idxmin()
        
        insights.append({
            'type': 'performance',
            'title': '🏆 Best Performing Facility',
            'description': f'{best_facility} has the highest average satisfaction score',
            'value': round(facility_stats.max(), 2),
            'recommendation': f'Replicate best practices from {best_facility}'
        })
        
        insights.append({
            'type': 'improvement',
            'title': '⚠️ Priority Improvement',
            'description': f'{worst_facility} needs immediate attention',
            'value': round(facility_stats.min(), 2),
            'recommendation': f'Focus improvement efforts on {worst_facility}'
        })
        
        # Trend insight
        if 'academic_year' in self.df.columns:
            year_trend = self.df.groupby('academic_year')['satisfaction_score'].mean()
            if len(year_trend) > 1:
                trend = 'increasing' if year_trend.iloc[-1] > year_trend.iloc[0] else 'decreasing'
                insights.append({
                    'type': 'trend',
                    'title': '📈 Satisfaction Trend',
                    'description': f'Overall satisfaction is {trend} over the years',
                    'value': round(year_trend.iloc[-1], 2),
                    'recommendation': 'Continue current initiatives' if trend == 'increasing' else 'Review current strategies'
                })
        
        # Time insight
        if 'hour' in self.df.columns:
            self.df['time_category'] = self.df['hour'].apply(
                lambda x: 'Morning' if 5 <= x < 12 else 
                         ('Afternoon' if 12 <= x < 17 else 
                         ('Evening' if 17 <= x < 22 else 'Night'))
            )
            time_stats = self.df.groupby('time_category')['satisfaction_score'].mean()
            best_time = time_stats.idxmax()
            
            insights.append({
                'type': 'time',
                'title': '⏰ Best Time Period',
                'description': f'Highest satisfaction during {best_time}',
                'value': round(time_stats.max(), 2),
                'recommendation': f'Schedule important activities during {best_time}'
            })
        
        return insights