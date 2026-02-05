"""
Visualizations Module
Creates publication-quality plots for regression analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def plot_residual_diagnostics(model, figsize=(14, 10)):
    """
    Create comprehensive residual diagnostic plots.
    
    Parameters
    ----------
    model : RegressionResults
        Fitted statsmodels regression
    figsize : tuple
        Figure size
    
    Returns
    -------
    matplotlib.figure.Figure
        Diagnostic plots
    """
    residuals = model.resid
    fitted = model.fittedvalues
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle('Regression Diagnostics', fontsize=14, fontweight='bold')
    
    # 1. Residuals vs Fitted
    axes[0, 0].scatter(fitted, residuals, alpha=0.6, edgecolors='k', linewidth=0.5)
    axes[0, 0].axhline(y=0, color='r', linestyle='--', linewidth=2)
    axes[0, 0].set_xlabel('Fitted Values')
    axes[0, 0].set_ylabel('Residuals')
    axes[0, 0].set_title('(1) Residuals vs Fitted Values\n(Check homoscedasticity)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Q-Q Plot
    stats.probplot(residuals, dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title('(2) Q-Q Plot\n(Check normality of residuals)')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Histogram of Residuals
    axes[1, 0].hist(residuals, bins=20, edgecolor='black', alpha=0.7, color='skyblue')
    axes[1, 0].set_xlabel('Residuals')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('(3) Distribution of Residuals\n(Check normality)')
    axes[1, 0].axvline(x=0, color='r', linestyle='--', linewidth=2)
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Actual vs Predicted
    y_actual = fitted + residuals
    axes[1, 1].scatter(y_actual, fitted, alpha=0.6, edgecolors='k', linewidth=0.5)
    axes[1, 1].plot([y_actual.min(), y_actual.max()], [y_actual.min(), y_actual.max()], 
                     'r--', lw=2, label='Perfect prediction')
    axes[1, 1].set_xlabel('Actual Values')
    axes[1, 1].set_ylabel('Predicted Values')
    axes[1, 1].set_title('(4) Actual vs Predicted\n(Check prediction accuracy)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def plot_correlation_heatmap(df, variables, figsize=(10, 8)):
    """
    Create correlation heatmap for variables.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data
    variables : list
        Variables to correlate
    figsize : tuple
        Figure size
    
    Returns
    -------
    matplotlib.figure.Figure
        Heatmap figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    corr_matrix = df[variables].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                square=True, ax=ax, cbar_kws={'label': 'Correlation'})
    
    ax.set_title('Correlation Matrix of Variables', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig


def plot_variable_distributions(df, variables, figsize=(14, 6)):
    """
    Create distribution plots for multiple variables.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data
    variables : list
        Variables to plot
    figsize : tuple
        Figure size
    
    Returns
    -------
    matplotlib.figure.Figure
        Distribution plots
    """
    n_vars = len(variables)
    n_cols = 3
    n_rows = (n_vars + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()
    
    for idx, var in enumerate(variables):
        axes[idx].hist(df[var].dropna(), bins=20, edgecolor='black', alpha=0.7, color='skyblue')
        axes[idx].set_title(f'Distribution of {var}')
        axes[idx].set_xlabel(var)
        axes[idx].set_ylabel('Frequency')
        axes[idx].grid(True, alpha=0.3)
    
    # Remove empty subplots
    for idx in range(len(variables), len(axes)):
        fig.delaxes(axes[idx])
    
    plt.tight_layout()
    
    return fig


def plot_predictor_effects(df, y_col, predictors, figsize=(14, 6)):
    """
    Create scatter plots showing relationship between predictors and outcome.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data
    y_col : str
        Dependent variable column
    predictors : list
        Predictor variables to plot
    figsize : tuple
        Figure size
    
    Returns
    -------
    matplotlib.figure.Figure
        Effect plots
    """
    n_pred = len(predictors)
    n_cols = 3
    n_rows = (n_pred + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()
    
    for idx, pred in enumerate(predictors):
        axes[idx].scatter(df[pred], df[y_col], alpha=0.6, edgecolors='k', linewidth=0.5)
        
        # Add trend line if continuous variable
        if pd.api.types.is_numeric_dtype(df[pred]):
            z = np.polyfit(df[pred].dropna(), df[y_col][df[pred].notna()], 1)
            p = np.poly1d(z)
            x_range = np.linspace(df[pred].min(), df[pred].max(), 100)
            axes[idx].plot(x_range, p(x_range), "r-", linewidth=2, label='Trend')
            axes[idx].legend()
        
        axes[idx].set_xlabel(pred)
        axes[idx].set_ylabel(y_col)
        axes[idx].set_title(f'{y_col} vs {pred}')
        axes[idx].grid(True, alpha=0.3)
    
    # Remove empty subplots
    for idx in range(len(predictors), len(axes)):
        fig.delaxes(axes[idx])
    
    plt.tight_layout()
    
    return fig


def plot_model_comparison(models_dict, figsize=(10, 6)):
    """
    Compare R² and adjusted R² across multiple models.
    
    Parameters
    ----------
    models_dict : dict
        Dictionary of {model_name: RegressionResults}
    figsize : tuple
        Figure size
    
    Returns
    -------
    matplotlib.figure.Figure
        Comparison plot
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    model_names = list(models_dict.keys())
    r2_values = [models_dict[m].rsquared for m in model_names]
    adj_r2_values = [models_dict[m].rsquared_adj for m in model_names]
    
    x = np.arange(len(model_names))
    width = 0.35
    
    ax.bar(x - width/2, r2_values, width, label='R²', alpha=0.8)
    ax.bar(x + width/2, adj_r2_values, width, label='Adjusted R²', alpha=0.8)
    
    ax.set_xlabel('Model')
    ax.set_ylabel('R² / Adjusted R²')
    ax.set_title('Model Comparison: Goodness of Fit', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(model_names)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0, 1])
    
    plt.tight_layout()
    
    return fig


def save_figure(fig, filepath, dpi=300):
    """
    Save figure to file.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object
    filepath : str
        Output file path
    dpi : int
        Resolution (default 300 for publication)
    """
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
