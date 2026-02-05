"""
Regression Model Module
Fits multiple linear regression with statsmodels for publication-quality output.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols


def fit_multiple_regression(df, formula, method='ols'):
    """
    Fit multiple linear regression model using statsmodels.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data with all variables
    formula : str
        Patsy formula for regression (e.g., 'pH_reading ~ rainfall + fertilizer')
    method : str
        Fitting method: 'ols' (ordinary least squares)
    
    Returns
    -------
    statsmodels.regression.linear_model.RegressionResults
        Fitted model object with full statistical output
    """
    if method == 'ols':
        model = ols(formula, data=df).fit()
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return model


def extract_regression_summary(model):
    """
    Extract key statistics from fitted regression model.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    
    Returns
    -------
    dict
        Summary statistics
    """
    summary = {
        'n_obs': int(model.nobs),
        'n_params': int(model.df_model) + 1,
        'dof_resid': int(model.df_resid),
        'dof_model': int(model.df_model),
        'r_squared': float(model.rsquared),
        'adj_r_squared': float(model.rsquared_adj),
        'f_statistic': float(model.fvalue),
        'f_pvalue': float(model.f_pvalue),
        'aic': float(model.aic),
        'bic': float(model.bic),
        'log_likelihood': float(model.llf)
    }
    
    return summary


def extract_coefficients_table(model):
    """
    Extract regression coefficients with statistics as DataFrame.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    
    Returns
    -------
    pd.DataFrame
        Coefficients table with confidence intervals
    """
    coef_table = model.summary2().tables[1]
    
    return coef_table


def create_regression_table(model, decimals=4):
    """
    Create publication-quality regression results table.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    decimals : int
        Decimal places for rounding
    
    Returns
    -------
    pd.DataFrame
        Formatted table for academic publication
    """
    # Extract coefficient information
    params = model.params
    pvalues = model.pvalues
    conf_int = model.conf_int(alpha=0.05)
    
    table = pd.DataFrame({
        'Coefficient': params.round(decimals),
        'Std. Error': model.bse.round(decimals),
        't-statistic': model.tvalues.round(4),
        'p-value': pvalues.round(4),
        '95% CI Lower': conf_int[0].round(decimals),
        '95% CI Upper': conf_int[1].round(decimals)
    })
    
    return table


def get_residuals(model):
    """
    Get model residuals and fitted values.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    
    Returns
    -------
    dict
        Residuals and fitted values
    """
    return {
        'residuals': model.resid,
        'fitted_values': model.fittedvalues,
        'predicted_values': model.fittedvalues
    }


def generate_model_report(model):
    """
    Generate formatted model summary report for academic paper.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    
    Returns
    -------
    str
        Formatted report
    """
    report = []
    report.append("\n" + "=" * 80)
    report.append("MULTIPLE LINEAR REGRESSION RESULTS")
    report.append("=" * 80)
    
    summary = extract_regression_summary(model)
    
    report.append(f"\nModel Fit Statistics:")
    report.append(f"  Sample Size (N):              {summary['n_obs']}")
    report.append(f"  Number of Parameters:        {summary['n_params']}")
    report.append(f"  Degrees of Freedom (Total):  {summary['n_obs'] - 1}")
    report.append(f"  Degrees of Freedom (Model):  {summary['dof_model']}")
    report.append(f"  Degrees of Freedom (Error):  {summary['dof_resid']}")
    
    report.append(f"\nModel Performance:")
    report.append(f"  R-Squared:                   {summary['r_squared']:.6f}")
    report.append(f"  Adjusted R-Squared:          {summary['adj_r_squared']:.6f}")
    report.append(f"  F-Statistic:                 {summary['f_statistic']:.4f}")
    report.append(f"  F-Statistic p-value:         {summary['f_pvalue']:.2e}")
    
    report.append(f"\nInterpretation:")
    report.append(f"  The model explains {summary['r_squared']*100:.2f}% of the variation in the dependent variable.")
    
    if summary['f_pvalue'] < 0.05:
        report.append(f"  The overall model is statistically significant (p < 0.05).")
    else:
        report.append(f"  The overall model is NOT statistically significant (p >= 0.05).")
    
    report.append("\n" + "-" * 80)
    report.append("COEFFICIENT ESTIMATES")
    report.append("-" * 80)
    
    coef_table = create_regression_table(model)
    report.append(str(coef_table))
    
    report.append("\n" + "=" * 80)
    
    return "\n".join(report)


def make_prediction(model, new_data, confidence=0.95):
    """
    Make predictions with confidence intervals on new data.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    new_data : pd.DataFrame
        New data for prediction
    confidence : float
        Confidence level (default 0.95 for 95% CI)
    
    Returns
    -------
    dict
        Predictions with confidence intervals
    """
    predictions = model.get_prediction(new_data)
    pred_summary = predictions.summary_frame(alpha=1-confidence)
    
    return {
        'predicted_mean': pred_summary['mean'],
        'mean_se': pred_summary['mean_se'],
        'mean_ci_lower': pred_summary['mean_ci_lower'],
        'mean_ci_upper': pred_summary['mean_ci_upper'],
        'obs_ci_lower': pred_summary['obs_ci_lower'],
        'obs_ci_upper': pred_summary['obs_ci_upper'],
        'table': pred_summary
    }
