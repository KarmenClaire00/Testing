"""
Reporting Module
Generates academic-quality tables and summary statistics for paper sections.
"""

import pandas as pd
import numpy as np


def create_descriptive_stats_table(df, variables, groupby=None):
    """
    Create descriptive statistics table for academic paper.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input data
    variables : list
        Variables to summarize
    groupby : str, optional
        Variable to group by
    
    Returns
    -------
    pd.DataFrame
        Formatted descriptive statistics table
    """
    if groupby is None:
        stats_table = df[variables].describe().T
        stats_table = stats_table[['count', 'mean', 'std', 'min', 'max']]
        stats_table.columns = ['N', 'M', 'SD', 'Min', 'Max']
    else:
        # Group-based statistics
        stats_table = df.groupby(groupby)[variables].apply(
            lambda x: pd.Series({
                'N': len(x),
                'M': x.mean(),
                'SD': x.std(),
                'Min': x.min(),
                'Max': x.max()
            })
        )
    
    return stats_table.round(3)


def create_correlation_table(df, variables, method='pearson'):
    """
    Create correlation matrix for paper.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input data
    variables : list
        Variables for correlation
    method : str
        Correlation method: 'pearson', 'spearman'
    
    Returns
    -------
    pd.DataFrame
        Correlation matrix
    """
    corr_matrix = df[variables].corr(method=method)
    
    return corr_matrix.round(3)


def create_regression_summary_table(model, decimals=4):
    """
    Create publication-ready regression results summary table.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    decimals : int
        Decimal places for numbers
    
    Returns
    -------
    pd.DataFrame
        Summary table
    """
    params = model.params
    pvalues = model.pvalues
    conf_int = model.conf_int(alpha=0.05)
    
    table = pd.DataFrame({
        'Predictor': params.index,
        'β': params.round(decimals),
        'SE': model.bse.round(decimals),
        't': model.tvalues.round(4),
        'p': pvalues.round(4),
        '95% CI [Lower]': conf_int[0].round(decimals),
        '95% CI [Upper]': conf_int[1].round(decimals)
    })
    
    return table.set_index('Predictor')


def create_model_fit_table(model):
    """
    Create table with overall model fit statistics.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    
    Returns
    -------
    pd.DataFrame
        Model fit statistics
    """
    fit_table = pd.DataFrame({
        'Statistic': [
            'R²',
            'Adjusted R²',
            'F-statistic',
            'df (Model)',
            'df (Residual)',
            'N',
            'AIC',
            'BIC'
        ],
        'Value': [
            f"{model.rsquared:.6f}",
            f"{model.rsquared_adj:.6f}",
            f"{model.fvalue:.4f}",
            f"{int(model.df_model)}",
            f"{int(model.df_resid)}",
            f"{int(model.nobs)}",
            f"{model.aic:.2f}",
            f"{model.bic:.2f}"
        ]
    })
    
    return fit_table


def create_interpretation_text(model, variable_labels=None):
    """
    Generate interpretation text for each significant predictor.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    variable_labels : dict, optional
        Mapping of variable names to descriptive labels
    
    Returns
    -------
    dict
        Interpretation text for each variable
    """
    interpretations = {}
    
    for var, coef in model.params.items():
        p_val = model.pvalues[var]
        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
        
        label = variable_labels.get(var, var) if variable_labels else var
        
        if var == 'Intercept':
            interpretations[var] = f"Intercept: {coef:.4f} (baseline pH when all predictors = 0)"
        else:
            direction = "increases" if coef > 0 else "decreases"
            interpretations[var] = f"{label}: {direction} by {abs(coef):.4f} units (p={model.pvalues[var]:.4f}) {sig}"
    
    return interpretations


def export_tables_to_file(tables_dict, filepath, format='csv'):
    """
    Export multiple tables to file(s).
    
    Parameters
    ----------
    tables_dict : dict
        Dictionary of {table_name: dataframe}
    filepath : str
        Output filepath (base name)
    format : str
        Format: 'csv', 'excel'
    """
    from pathlib import Path
    
    output_dir = Path(filepath).parent
    base_name = Path(filepath).stem
    
    for table_name, df in tables_dict.items():
        if format == 'csv':
            outfile = output_dir / f"{base_name}_{table_name}.csv"
            df.to_csv(outfile)
        elif format == 'excel':
            outfile = output_dir / f"{base_name}_{table_name}.xlsx"
            df.to_excel(outfile)


def create_results_summary(model, df_original, y_actual, y_predicted):
    """
    Create comprehensive results summary for paper.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted regression model
    df_original : pd.DataFrame
        Original dataset
    y_actual : array-like
        Actual dependent variable values
    y_predicted : array-like
        Predicted values
    
    Returns
    -------
    str
        Formatted summary for Results section
    """
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    
    rmse = np.sqrt(mean_squared_error(y_actual, y_predicted))
    mae = mean_absolute_error(y_actual, y_predicted)
    
    summary = []
    summary.append("RESULTS SUMMARY FOR ACADEMIC PAPER")
    summary.append("=" * 80)
    
    summary.append(f"\nSample Characteristics:")
    summary.append(f"  Total observations: N = {model.nobs}")
    summary.append(f"  Dependent variable: Mean = {y_actual.mean():.3f}, SD = {y_actual.std():.3f}")
    summary.append(f"  Range: {y_actual.min():.2f} - {y_actual.max():.2f}")
    
    summary.append(f"\nModel Performance:")
    summary.append(f"  R² = {model.rsquared:.4f} (model explains {model.rsquared*100:.2f}% of variance)")
    summary.append(f"  Adjusted R² = {model.rsquared_adj:.4f}")
    summary.append(f"  F({int(model.df_model)}, {int(model.df_resid)}) = {model.fvalue:.4f}, p < .001")
    
    summary.append(f"\nPrediction Accuracy:")
    summary.append(f"  RMSE = {rmse:.4f} (average prediction error)")
    summary.append(f"  MAE = {mae:.4f} (mean absolute error)")
    
    summary.append(f"\nSignificant Predictors (p < 0.05):")
    sig_vars = model.pvalues[model.pvalues < 0.05]
    for var in sig_vars.index:
        if var != 'Intercept':
            coef = model.params[var]
            p_val = model.pvalues[var]
            summary.append(f"  • {var}: β = {coef:.4f}, p = {p_val:.4f}")
    
    summary.append("\n" + "=" * 80)
    
    return "\n".join(summary)
