from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys
import pandas as pd
sys.path.insert(0, '..')
from config import Config
from utils.data_processor import DataProcessor
from utils.analytics import AnalyticsEngine

# Initialize Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)
CORS(app)

# Initialize data processor
data_processor = DataProcessor(app.config['DATA_FILE_PATH'])
analytics_engine = AnalyticsEngine(data_processor)

# ========== ROUTES ==========

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/overall-metrics')
def get_overall_metrics():
    """Get overall metrics"""
    metrics = data_processor.get_overall_metrics()
    return jsonify({
        'success': True,
        'data': metrics,
        'timestamp': pd.Timestamp.now().isoformat()
    })

@app.route('/api/facility-metrics')
def get_facility_metrics():
    """Get facility-wise metrics"""
    facilities = data_processor.get_facility_metrics()
    return jsonify({
        'success': True,
        'data': facilities,
        'count': len(facilities)
    })

@app.route('/api/year-metrics')
def get_year_metrics():
    """Get year-wise metrics"""
    years = data_processor.get_year_metrics()
    return jsonify({
        'success': True,
        'data': years,
        'count': len(years)
    })

@app.route('/api/major-metrics')
def get_major_metrics():
    """Get major-wise metrics"""
    majors = data_processor.get_major_metrics()
    return jsonify({
        'success': True,
        'data': majors,
        'count': len(majors)
    })

@app.route('/api/time-metrics')
def get_time_metrics():
    """Get time-based metrics"""
    time_data = data_processor.get_time_metrics()
    return jsonify({
        'success': True,
        'data': time_data
    })

@app.route('/api/trend-analysis')
def get_trend_analysis():
    """Get trend analysis"""
    trend_data = analytics_engine.get_trend_analysis()
    return jsonify({
        'success': True,
        'data': trend_data
    })

@app.route('/api/insights')
def get_insights():
    """Get actionable insights"""
    insights = analytics_engine.get_insights()
    return jsonify({
        'success': True,
        'data': insights,
        'count': len(insights)
    })

@app.route('/api/filtered-data')
def get_filtered_data():
    """Get filtered data based on query parameters"""
    filters = {
        'facility': request.args.get('facility'),
        'year': request.args.get('year'),
        'major': request.args.get('major'),
        'score_range': request.args.get('score_range')
    }
    
    filtered_data = data_processor.get_filtered_data(filters)
    return jsonify({
        'success': True,
        'data': filtered_data,
        'count': len(filtered_data),
        'filters_applied': filters
    })

@app.route('/api/facilities')
def get_facilities():
    """Get list of all facilities"""
    if data_processor.df is not None and 'facility_rated' in data_processor.df.columns:
        facilities = sorted(data_processor.df['facility_rated'].unique().tolist())
        return jsonify({
            'success': True,
            'data': facilities
        })
    return jsonify({'success': False, 'data': []})

@app.route('/api/years')
def get_years():
    """Get list of all academic years"""
    if data_processor.df is not None and 'academic_year' in data_processor.df.columns:
        years = sorted(data_processor.df['academic_year'].unique().tolist())
        return jsonify({
            'success': True,
            'data': years
        })
    return jsonify({'success': False, 'data': []})

@app.route('/api/majors')
def get_majors():
    """Get list of all majors"""
    if data_processor.df is not None and 'major' in data_processor.df.columns:
        majors = sorted(data_processor.df['major'].unique().tolist())
        return jsonify({
            'success': True,
            'data': majors
        })
    return jsonify({'success': False, 'data': []})

@app.route('/api/dashboard-summary')
def get_dashboard_summary():
    """Get complete dashboard summary"""
    facilities = data_processor.get_facility_metrics()
    overall = data_processor.get_overall_metrics()
    overall['facilities_count'] = len(facilities)

    return jsonify({
        'success': True,
        'data': {
            'overall': overall,
            'facilities': facilities,
            'years': data_processor.get_year_metrics(),
            'majors': data_processor.get_major_metrics(),
            'time_analysis': data_processor.get_time_metrics(),
            'trends': analytics_engine.get_trend_analysis(),
            'insights': analytics_engine.get_insights()
        }
    })

@app.route('/api/filtered-dashboard-summary')
def get_filtered_dashboard_summary():
    """Get dashboard summary based on filters"""
    filters = {
        'facility': request.args.get('facility'),
        'year': request.args.get('year'),
        'major': request.args.get('major'),
        'score_range': request.args.get('score_range')
    }

    # Get filtered data
    filtered_data = data_processor.get_filtered_data(filters)

    if not filtered_data:
        return jsonify({
            'success': True,
            'data': {
                'overall': {'total_ratings': 0, 'average_score': 0, 'score_distribution': {}, 'category_distribution': {}},
                'facilities': [],
                'years': [],
                'majors': [],
                'time_analysis': {},
                'trends': [],
                'insights': []
            }
        })

    # Create a temporary dataframe from filtered data for calculations
    filtered_df = pd.DataFrame(filtered_data)

    # Calculate filtered metrics
    overall_metrics = data_processor.calculate_overall_metrics_from_df(filtered_df)
    facility_metrics = data_processor.calculate_facility_metrics_from_df(filtered_df)
    year_metrics = data_processor.calculate_year_metrics_from_df(filtered_df)
    major_metrics = data_processor.calculate_major_metrics_from_df(filtered_df)
    time_metrics = data_processor.calculate_time_metrics_from_df(filtered_df)

    # Add facilities_count to overall metrics
    overall_metrics['facilities_count'] = len(facility_metrics)

    # For trends and insights, use filtered data for more accurate analysis
    # Create filtered analytics engine if there's enough data
    if len(filtered_df) > 10:  # Only if we have meaningful data
        filtered_analytics = AnalyticsEngine(data_processor.__class__(None))
        filtered_analytics.data_processor.df = filtered_df
        trends = filtered_analytics.get_trend_analysis()
        insights = filtered_analytics.get_insights()
    else:
        # Fall back to full dataset trends if filtered data is too small
        trends = analytics_engine.get_trend_analysis()
        insights = analytics_engine.get_insights()

    return jsonify({
        'success': True,
        'data': {
            'overall': overall_metrics,
            'facilities': facility_metrics,
            'years': year_metrics,
            'majors': major_metrics,
            'time_analysis': time_metrics,
            'trends': trends,
            'insights': insights
        }
    })

# ========== STATIC FILES ==========

@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Resource not found',
        'message': str(error)
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': str(error)
    }), 500

# ========== APPLICATION START ==========

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    print("="*50)
    print("Campus Pulse Dashboard Starting...")
    print("="*50)
    print(f"Data loaded: {data_processor.df.shape[0]} records")
    print("API Endpoints:")
    print("  GET /api/overall-metrics")
    print("  GET /api/facility-metrics")
    print("  GET /api/year-metrics")
    print("  GET /api/major-metrics")
    print("  GET /api/filtered-data")
    print("  GET /api/insights")
    print("="*50)
    print("Dashboard available at: http://localhost:5000")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)