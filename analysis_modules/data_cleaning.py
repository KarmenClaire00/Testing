"""
Data Cleaning Module
Handles missing value imputation, outlier detection, and data preparation.
"""

import pandas as pd
import numpy as np
from scipy import stats


def handle_missing_values(df, strategy='documented'):
    """
    Handle missing values in dataset with documented strategy.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataset
    strategy : str
        Strategy: 'remove', 'mean_impute', 'group_mean', 'documented'
    
    Returns
    -------
    pd.DataFrame, dict
        Cleaned dataset and cleaning documentation
    """
    df_clean = df.copy()
    documentation = {
        'original_n': len(df),
        'missing_by_variable': {},
        'imputation_strategy': {},
        'rows_removed': 0
    }
    
    # For pH (dependent variable): Remove rows with missing pH
    if 'pH_reading' in df_clean.columns:
        initial_n = len(df_clean)
        df_clean = df_clean[df_clean['pH_reading'].notna()]
        documentation['rows_removed'] = initial_n - len(df_clean)
        documentation['missing_by_variable']['pH_reading'] = f"Removed {documentation['rows_removed']} rows"
    
    # For fertilizer_kg_ha: Impute with group means (by Barangay and Crop)
    if 'fertilizer_kg_ha' in df_clean.columns:
        missing_count = df_clean['fertilizer_kg_ha'].isnull().sum()
        if missing_count > 0:
            df_clean['fertilizer_kg_ha'] = df_clean.groupby(['Barangay', 'Crop'])['fertilizer_kg_ha'].transform(
                lambda x: x.fillna(x.mean())
            )
            # Fill remaining with overall mean
            df_clean['fertilizer_kg_ha'] = df_clean['fertilizer_kg_ha'].fillna(
                df_clean['fertilizer_kg_ha'].mean()
            )
            documentation['imputation_strategy']['fertilizer_kg_ha'] = 'Group mean (Barangay×Crop), then overall mean'
            documentation['missing_by_variable']['fertilizer_kg_ha'] = missing_count
    
    # For years_planted: Impute with mean
    if 'years_planted' in df_clean.columns:
        missing_count = df_clean['years_planted'].isnull().sum()
        if missing_count > 0:
            df_clean['years_planted'] = df_clean['years_planted'].fillna(
                df_clean['years_planted'].mean()
            )
            documentation['imputation_strategy']['years_planted'] = 'Overall mean'
            documentation['missing_by_variable']['years_planted'] = missing_count
    
    documentation['final_n'] = len(df_clean)
    
    return df_clean, documentation


def detect_outliers(df, column, method='iqr', threshold=1.5):
    """
    Detect outliers in a column.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataset
    column : str
        Column name to check
    method : str
        Method: 'iqr', 'zscore'
    threshold : float
        Threshold for outlier detection
    
    Returns
    -------
    dict
        Outlier information
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - threshold * IQR
        upper = Q3 + threshold * IQR
        outliers = df[(df[column] < lower) | (df[column] > upper)]
    
    elif method == 'zscore':
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        outliers = df[np.abs(stats.zscore(df[column].dropna())) > threshold]
    
    return {
        'column': column,
        'method': method,
        'n_outliers': len(outliers),
        'pct_outliers': len(outliers) / len(df) * 100,
        'outlier_indices': outliers.index.tolist()
    }


def prepare_regression_data(df):
    """
    Prepare data for regression analysis with proper encoding.
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset
    
    Returns
    -------
    pd.DataFrame
        Dataset with encoded variables ready for regression
    """
    df_reg = df.copy()
    
    # Create dummy variables for Crop (with drop_first=True for reference category)
    crop_dummies = pd.get_dummies(df_reg['Crop'], prefix='Crop', drop_first=True)
    df_reg = pd.concat([df_reg, crop_dummies], axis=1)
    
    # Create dummy variables for Barangay (optional, for advanced models)
    barangay_dummies = pd.get_dummies(df_reg['Barangay'], prefix='Barangay', drop_first=True)
    df_reg = pd.concat([df_reg, barangay_dummies], axis=1)
    
    return df_reg


def get_cleaning_report(df_original, df_clean):
    """
    Generate cleaning report comparing original and cleaned data.
    
    Parameters
    ----------
    df_original : pd.DataFrame
        Original dataset
    df_clean : pd.DataFrame
        Cleaned dataset
    
    Returns
    -------
    str
        Formatted cleaning report
    """
    report = []
    report.append("=" * 70)
    report.append("DATA CLEANING REPORT")
    report.append("=" * 70)
    report.append(f"\nOriginal dataset: {len(df_original)} observations, {len(df_original.columns)} variables")
    report.append(f"Cleaned dataset:  {len(df_clean)} observations, {len(df_clean.columns)} variables")
    report.append(f"Rows removed:     {len(df_original) - len(df_clean)}")
    report.append(f"Data retention:   {len(df_clean)/len(df_original)*100:.1f}%")
    
    return "\n".join(report)
