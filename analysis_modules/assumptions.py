"""
Assumptions Testing Module
Tests regression assumptions: normality, linearity, homoscedasticity, multicollinearity.
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor


def test_normality(data, test_type='shapiro'):
    """
    Test normality of residuals or dependent variable.
    
    Parameters
    ----------
    data : array-like
        Data to test (residuals or variable)
    test_type : str
        Test method: 'shapiro', 'anderson', 'ks'
    
    Returns
    -------
    dict
        Test results with interpretation
    """
    if test_type == 'shapiro':
        stat, p_value = stats.shapiro(data)
        test_name = 'Shapiro-Wilk Test'
    elif test_type == 'anderson':
        result = stats.anderson(data)
        stat = result.statistic
        p_value = result.critical_values[2]  # 5% level
        test_name = 'Anderson-Darling Test'
    elif test_type == 'ks':
        # Kolmogorov-Smirnov test
        stat, p_value = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data)))
        test_name = 'Kolmogorov-Smirnov Test'
    else:
        raise ValueError(f"Unknown test_type: {test_type}")
    
    return {
        'test_name': test_name,
        'statistic': stat,
        'p_value': p_value,
        'normal_at_05': p_value > 0.05,
        'interpretation': 'Approximately normally distributed' if p_value > 0.05 else 'May not be normally distributed'
    }


def calculate_vif(X_df):
    """
    Calculate Variance Inflation Factor (VIF) for multicollinearity detection.
    
    Parameters
    ----------
    X_df : pd.DataFrame
        Feature matrix
    
    Returns
    -------
    pd.DataFrame
        VIF values for each variable
    """
    vif_data = pd.DataFrame()
    vif_data['Variable'] = X_df.columns
    vif_data['VIF'] = [variance_inflation_factor(X_df.values, i) for i in range(X_df.shape[1])]
    
    return vif_data.sort_values('VIF', ascending=False)


def test_multicollinearity(X_df, vif_threshold=5):
    """
    Test for multicollinearity and correlation issues.
    
    Parameters
    ----------
    X_df : pd.DataFrame
        Feature matrix
    vif_threshold : float
        VIF threshold (typically 5-10)
    
    Returns
    -------
    dict
        Multicollinearity assessment
    """
    vif_data = calculate_vif(X_df)
    
    problematic = vif_data[vif_data['VIF'] > vif_threshold]
    
    return {
        'vif_data': vif_data,
        'problematic_vars': problematic['Variable'].tolist() if len(problematic) > 0 else [],
        'multicollinearity_detected': len(problematic) > 0,
        'interpretation': f"Multicollinearity detected in {len(problematic)} variables" if len(problematic) > 0 else "No problematic multicollinearity detected (all VIF < {})".format(vif_threshold)
    }


def test_homoscedasticity(residuals, fitted_values):
    """
    Test for homoscedasticity (Breusch-Pagan test).
    
    Parameters
    ----------
    residuals : array-like
        Model residuals
    fitted_values : array-like
        Fitted values
    
    Returns
    -------
    dict
        Homoscedasticity test results
    """
    from statsmodels.stats.diagnostic import het_breuschpagan
    
    bp_stat, bp_pvalue, _, _ = het_breuschpagan(residuals, fitted_values)
    
    return {
        'test_name': 'Breusch-Pagan Test',
        'statistic': bp_stat,
        'p_value': bp_pvalue,
        'homoscedastic_at_05': bp_pvalue > 0.05,
        'interpretation': 'Homoscedasticity assumption appears satisfied' if bp_pvalue > 0.05 else 'Heteroscedasticity detected'
    }


def test_independence(residuals):
    """
    Test for independence of residuals (Durbin-Watson).
    
    Parameters
    ----------
    residuals : array-like
        Model residuals
    
    Returns
    -------
    dict
        Independence test results
    """
    from statsmodels.stats.stattools import durbin_watson
    
    dw_stat = durbin_watson(residuals)
    
    # DW = 2 means no autocorrelation; range is 0-4
    # DW < 2: positive correlation; DW > 2: negative correlation
    
    return {
        'test_name': 'Durbin-Watson Test',
        'statistic': dw_stat,
        'range': (0, 4),
        'neutral_value': 2,
        'interpretation': f'DW={dw_stat:.3f}. Values close to 2 indicate independence. <2: positive autocorr; >2: negative autocorr'
    }


def get_qq_plot_data(residuals):
    """
    Get data for Q-Q plot (quantile-quantile plot).
    
    Parameters
    ----------
    residuals : array-like
        Model residuals
    
    Returns
    -------
    tuple
        (theoretical_quantiles, sample_quantiles)
    """
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(residuals)))
    sample_quantiles = np.sort(residuals)
    
    return theoretical_quantiles, sample_quantiles


def generate_assumptions_report(test_results):
    """
    Generate formatted assumptions testing report.
    
    Parameters
    ----------
    test_results : dict
        Dictionary of assumption test results
    
    Returns
    -------
    str
        Formatted report
    """
    report = []
    report.append("\n" + "=" * 70)
    report.append("LINEAR REGRESSION ASSUMPTIONS TESTING")
    report.append("=" * 70)
    
    if 'normality' in test_results:
        nt = test_results['normality']
        report.append(f"\n1. NORMALITY OF RESIDUALS")
        report.append(f"   Test: {nt['test_name']}")
        report.append(f"   Statistic: {nt['statistic']:.6f}")
        report.append(f"   p-value: {nt['p_value']:.6f}")
        report.append(f"   Result: {nt['interpretation']}")
    
    if 'multicollinearity' in test_results:
        mc = test_results['multicollinearity']
        report.append(f"\n2. MULTICOLLINEARITY (VIF < 5 preferred)")
        report.append(f"   {mc['interpretation']}")
        if len(mc['problematic_vars']) > 0:
            report.append(f"   Problematic variables: {', '.join(mc['problematic_vars'])}")
    
    if 'homoscedasticity' in test_results:
        hc = test_results['homoscedasticity']
        report.append(f"\n3. HOMOSCEDASTICITY (BREUSCH-PAGAN)")
        report.append(f"   Statistic: {hc['statistic']:.6f}")
        report.append(f"   p-value: {hc['p_value']:.6f}")
        report.append(f"   Result: {hc['interpretation']}")
    
    if 'independence' in test_results:
        ind = test_results['independence']
        report.append(f"\n4. INDEPENDENCE (DURBIN-WATSON)")
        report.append(f"   Statistic: {ind['statistic']:.6f}")
        report.append(f"   {ind['interpretation']}")
    
    report.append("\n" + "=" * 70)
    
    return "\n".join(report)
