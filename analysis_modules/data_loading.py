"""
Data Loading Module
Handles loading and initial validation of soil pH research data from Excel or CSV formats.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_data(filepath):
    """
    Load research data from Excel or CSV file.
    
    Parameters
    ----------
    filepath : str
        Path to the data file (CSV or Excel)
    
    Returns
    -------
    pd.DataFrame
        Loaded dataset with initial validation
    
    Raises
    ------
    FileNotFoundError
        If file does not exist
    ValueError
        If file format is unsupported
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    if filepath.suffix.lower() == '.csv':
        df = pd.read_csv(filepath)
    elif filepath.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")
    
    return df


def validate_dataset(df):
    """
    Validate loaded dataset structure and content.
    
    Parameters
    ----------
    df : pd.DataFrame
        Loaded dataset
    
    Returns
    -------
    dict
        Validation report with structure information
    """
    required_columns = ['pH_reading', 'Barangay', 'Crop', 
                       'fertilizer_kg_ha', 'years_planted', 'lime_applied']
    
    report = {
        'n_rows': len(df),
        'n_cols': len(df.columns),
        'columns': df.columns.tolist(),
        'missing_required': []
    }
    
    for col in required_columns:
        if col not in df.columns:
            report['missing_required'].append(col)
    
    return report


def get_data_summary(df):
    """
    Get comprehensive summary of loaded data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Loaded dataset
    
    Returns
    -------
    dict
        Summary statistics and info
    """
    summary = {
        'n_observations': len(df),
        'n_features': len(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'missing_counts': df.isnull().sum().to_dict(),
        'missing_pct': (df.isnull().sum() / len(df) * 100).to_dict()
    }
    
    return summary
