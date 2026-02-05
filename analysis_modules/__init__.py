"""
Soil pH Linear Regression Analysis - Module Package
Analysis modules for processing and modeling soil pH data.
"""

from .data_loading import load_data, validate_dataset, get_data_summary
from .data_cleaning import handle_missing_values, detect_outliers, prepare_regression_data, get_cleaning_report
from .assumptions import (
    test_normality, calculate_vif, test_multicollinearity,
    test_homoscedasticity, test_independence, generate_assumptions_report
)
from .regression_model import (
    fit_multiple_regression, extract_regression_summary, extract_coefficients_table,
    create_regression_table, get_residuals, generate_model_report, make_prediction
)
from .reporting import (
    create_descriptive_stats_table, create_correlation_table, create_regression_summary_table,
    create_model_fit_table, create_interpretation_text, export_tables_to_file,
    create_results_summary
)
from .visualizations import (
    plot_residual_diagnostics, plot_correlation_heatmap, plot_variable_distributions,
    plot_predictor_effects, plot_model_comparison, save_figure
)

__all__ = [
    # Data loading
    'load_data', 'validate_dataset', 'get_data_summary',
    
    # Data cleaning
    'handle_missing_values', 'detect_outliers', 'prepare_regression_data', 'get_cleaning_report',
    
    # Assumptions testing
    'test_normality', 'calculate_vif', 'test_multicollinearity',
    'test_homoscedasticity', 'test_independence', 'generate_assumptions_report',
    
    # Regression modeling
    'fit_multiple_regression', 'extract_regression_summary', 'extract_coefficients_table',
    'create_regression_table', 'get_residuals', 'generate_model_report', 'make_prediction',
    
    # Reporting
    'create_descriptive_stats_table', 'create_correlation_table', 'create_regression_summary_table',
    'create_model_fit_table', 'create_interpretation_text', 'export_tables_to_file',
    'create_results_summary',
    
    # Visualizations
    'plot_residual_diagnostics', 'plot_correlation_heatmap', 'plot_variable_distributions',
    'plot_predictor_effects', 'plot_model_comparison', 'save_figure'
]

__version__ = '1.0.0'
