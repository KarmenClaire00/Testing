# Soil pH Linear Regression Analysis

## Project Overview

This repository contains a comprehensive research project for modeling soil pH levels based on environmental and land-use factors using linear regression. The analysis is designed to support a full academic research paper on soil acidification management in agricultural areas.

**Study Title:** Modeling Soil pH Levels Based on Environmental and Land-Use Factors Using Linear Regression

**Study Location:** Dangcagan, Bukidnon, Philippines (6 barangays)
**Study Period:** June - October 2025
**Sample Size:** N = 90 soil samples

---

## Project Structure

```
/workspaces/Testing/
├── Soil_pH_Linear_Regression_Analysis.ipynb    # Main analysis notebook
├── ResearchData/
│   └── Research DATA everything.csv            # Dataset (90 observations)
├── analysis_modules/                           # Python package for reusable functions
│   ├── __init__.py
│   ├── data_loading.py                        # Load and validate data
│   ├── data_cleaning.py                       # Handle missing values, outliers
│   ├── assumptions.py                         # Test normality, VIF, homoscedasticity
│   ├── regression_model.py                    # Fit regression, extract statistics
│   ├── reporting.py                           # Generate academic tables
│   └── visualizations.py                      # Create publication-quality plots
├── requirements.txt                            # Python dependencies
└── README.md                                   # This file
```

---

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Libraries:**
- `pandas` (≥2.0.0) - Data manipulation
- `numpy` (≥1.24.0) - Numerical computing
- `statsmodels` (≥0.14.0) - Publication-quality regression & statistics ⭐
- `scikit-learn` (≥1.3.0) - Model evaluation metrics
- `matplotlib` (≥3.7.0) - Visualizations
- `seaborn` (≥0.13.0) - Statistical visualizations
- `scipy` (≥1.10.0) - Statistical tests

### 2. Set Python Path (if running from directory)

The notebook automatically imports the `analysis_modules` package. Ensure you're running from the project root directory.

---

## Workflow: Using This Analysis

### Phase 1: Data Exploration
The notebook begins with:
- Data loading and structure validation
- Missing value assessment
- Descriptive statistics
- Exploratory data analysis (EDA)

### Phase 2: Assumptions Testing (Pre-Modeling)
Before fitting the regression:
- **Normality Test**: Shapiro-Wilk test on dependent variable (pH)
- **Correlation Analysis**: Bivariate correlations to identify relationships
- **Distribution Visualization**: Histograms and Q-Q plots

### Phase 3: Model Specification
- **Formula**: `pH_reading ~ fertilizer_kg_ha + years_planted + lime_applied + organic_fertilizer + C(Crop)`
- **Method**: Ordinary Least Squares (OLS) via statsmodels
- **Software**: Python 3.x + statsmodels

### Phase 4: Model Estimation & Interpretation
Statsmodels provides:
- ✓ Regression coefficients with standard errors
- ✓ t-statistics and p-values (two-tailed)
- ✓ 95% confidence intervals for parameters
- ✓ R², Adjusted R², F-statistic
- ✓ AIC, BIC information criteria

### Phase 5: Assumptions Validation (Post-Modeling)
Statistical tests on residuals:
- **Normality**: Shapiro-Wilk test
- **Homoscedasticity**: Breusch-Pagan test
- **Independence**: Durbin-Watson statistic
- **Multicollinearity**: Variance Inflation Factor (VIF)

### Phase 6: Model Diagnostics
Visual inspection via 4-panel diagnostic plots:
1. Residuals vs Fitted (homoscedasticity)
2. Q-Q Plot (normality)
3. Histogram of residuals (normality)
4. Actual vs Predicted (prediction accuracy)

### Phase 7: Predictions & Applications
Generate predictions with 95% confidence intervals for farmyards with specific characteristics.

---

## Module Functions Reference

### data_loading.py
```python
from analysis_modules import load_data, validate_dataset, get_data_summary

df = load_data('ResearchData/Research DATA everything.csv')
validation = validate_dataset(df)
summary = get_data_summary(df)
```

### data_cleaning.py
```python
from analysis_modules import handle_missing_values, prepare_regression_data

df_clean, documentation = handle_missing_values(df)
df_regression = prepare_regression_data(df_clean)
```

### assumptions.py
```python
from analysis_modules import test_normality, calculate_vif, test_multicollinearity

normality = test_normality(data)
vif_results = calculate_vif(X_matrix)
multicollinearity = test_multicollinearity(X_matrix)
```

### regression_model.py
```python
from analysis_modules import fit_multiple_regression, create_regression_table

model = fit_multiple_regression(df, formula='pH_reading ~ X1 + X2 + X3')
coef_table = create_regression_table(model)
predictions = model.get_prediction(new_data)
```

### reporting.py
```python
from analysis_modules import create_descriptive_stats_table, create_correlation_table

desc_table = create_descriptive_stats_table(df, variables=['pH_reading', 'fertilizer_kg_ha'])
corr_table = create_correlation_table(df, variables=['pH_reading', 'fertilizer_kg_ha'])
```

### visualizations.py
```python
from analysis_modules import plot_residual_diagnostics, plot_correlation_heatmap

fig1 = plot_residual_diagnostics(model)
fig2 = plot_correlation_heatmap(df, variables=['pH_reading', 'fertilizer_kg_ha'])
```

---

## Connecting Analysis to Research Paper Sections

### METHODOLOGY Section
The notebook provides content for:
- Model specification and estimation approach
- Variable definitions and measurement
- Sample characteristics
- Assumption testing procedures
- Software and analytical tools used

**Key Outputs:**
- Formula statement
- Data characteristics table
- Assumption test descriptions

### RESULTS Section
The notebook provides:
- Descriptive statistics (Table 1)
- Correlation matrix (Table 2)
- Regression coefficients table (Table 3)
- Model fit statistics (Table 4)
- Diagnostic plots (Figures 1-4)

**Key Outputs:**
- Model.summary() table
- Coefficient estimates with p-values
- R², Adjusted R², F-statistic
- RMSE and MAE values

### DISCUSSION Section
The notebook provides guidance for:
- Interpreting significant predictors
- Comparing to literature findings
- Acknowledging model limitations
- Practical implications for farmers
- Future research directions

**Key Outputs:**
- Coefficient interpretations
- Effect sizes and significance
- Assumption compliance assessment

---

## Understanding Key Statistics

### R² (Coefficient of Determination)
- **Range**: 0 to 1
- **Interpretation**: Proportion of pH variance explained by the model
- **Example**: R² = 0.523 means the model explains 52.3% of pH variation

### Adjusted R²
- **Formula**: 1 - (1 - R²) × (n - 1) / (n - k - 1)
- **Advantage**: Penalizes adding irrelevant predictors
- **Use when**: Comparing models with different numbers of predictors

### RMSE (Root Mean Squared Error)
- **Units**: Same as dependent variable (pH units)
- **Interpretation**: Average magnitude of prediction error
- **Example**: RMSE = 0.45 means predictions are off by ~0.45 pH units on average

### F-Statistic
- **Test**: Overall model significance (H₀: All β = 0)
- **Interpretation**: Ratio of explained variance to unexplained variance
- **Usually reported as**: F(df_model, df_residual) = value, p < .001

### p-values
- **α-level**: 0.05 (standard for social sciences and agriculture)
- **Interpretation**: Probability of observing coefficient if null hypothesis true
- **Convention**: p < 0.05 = statistically significant

### 95% Confidence Interval
- **Interpretation**: Range containing true parameter with 95% confidence
- **Example**: 95% CI [0.002, 0.014] means we're 95% confident the true β is between 0.002 and 0.014
- **Decision rule**: If CI doesn't include 0, then p < 0.05

### Variance Inflation Factor (VIF)
- **Interpretation**: How much variance is inflated due to multicollinearity
- **Thresholds**: VIF < 5 (good), VIF 5-10 (caution), VIF > 10 (problematic)
- **Formula**: VIF = 1 / (1 - R²ⱼ) where R²ⱼ is R² from regressing variable j on all others

---

## Assumptions of Linear Regression

1. **Linearity**: Relationship between predictors and outcome is linear
   - **Check**: Residuals vs Fitted plot

2. **Normality**: Residuals are approximately normally distributed
   - **Check**: Q-Q plot, Shapiro-Wilk test

3. **Homoscedasticity**: Constant variance of residuals across predictions
   - **Check**: Residuals vs Fitted plot, Breusch-Pagan test

4. **Independence**: Observations are independent
   - **Check**: Durbin-Watson statistic (for time-series data)

5. **No Multicollinearity**: Predictors not highly correlated
   - **Check**: VIF values (all < 5 preferred)

---

## Common Issues & Solutions

### Issue: Non-normal residuals
**Solutions:**
- Transform dependent variable (log, square root)
- Increase sample size (n > 30 becomes more robust)
- Use robust standard errors

### Issue: Heteroscedasticity (non-constant variance)
**Solutions:**
- Weighted least squares (WLS)
- Robust standard errors (HC3, HC4)
- Transform variables

### Issue: High VIF (multicollinearity)
**Solutions:**
- Remove redundant predictors
- Combine correlated variables
- Use ridge regression or LASSO

### Issue: Outliers affecting results
**Solutions:**
- Investigate cause (data entry error vs. genuine extreme value)
- Robust regression (Huber, bisquare weights)
- Remove if justified by domain knowledge

---

## Running the Notebook

### Via Jupyter
```bash
cd /workspaces/Testing
jupyter notebook Soil_pH_Linear_Regression_Analysis.ipynb
```

### Key Checkpoints
Run cells sequentially:
1. **Cell 1**: Import libraries ✓
2. **Cell 2**: Load data ✓
3. **Cell 3**: Check for missing values ✓
4. **Cells 4-8**: Clean data and EDA ✓
5. **Cells 9-10**: Pre-modeling assumptions ✓
6. **Cells 11-13**: Fit regression model ✓
7. **Cells 14-15**: Post-modeling diagnostics ✓
8. **Cell 16**: Model summary ✓

All cells should execute without errors.

---

## Exporting Results

### Save Regression Summary
```python
# Print full summary
print(model_sm.summary())

# Export to text file
with open('regression_summary.txt', 'w') as f:
    f.write(str(model_sm.summary()))
```

### Save Tables
```python
from analysis_modules import export_tables_to_file

tables = {
    'descriptive_stats': desc_table,
    'correlation': corr_table,
    'regression': coef_table
}
export_tables_to_file(tables, 'output/results', format='csv')
```

### Save Figures
```python
from analysis_modules import save_figure

save_figure(fig, 'output/diagnostic_plots.png', dpi=300)
```

---

## Citation & References

For papers using this analysis, cite:

```bibtex
@article{dangcagan_2025,
  title={Modeling Soil pH Levels Based on Environmental and Land-Use Factors Using Linear Regression},
  author={[Your names]},
  year={2025},
  address={Dangcagan, Bukidnon, Philippines}
}
```

Key references integrated in analysis:
- Delgadillo-Duran et al. (2020) - Regression models for soil properties
- Arunrat et al. (2020) - Soil pH management
- Yigini et al. (2022) - Correlational designs
- Correndo et al. (2021) - Linear regression in environmental studies
- Ngetich et al. (2023) - Predictive models for agriculture

---

## File Output Organization

Suggested directory structure for paper materials:
```
/paper_output/
├── tables/
│   ├── Table1_Descriptive_Stats.csv
│   ├── Table2_Correlation_Matrix.csv
│   ├── Table3_Regression_Results.csv
│   └── Table4_Model_Fit.csv
├── figures/
│   ├── Figure1_pH_Distribution.png
│   ├── Figure2_QQ_Plot.png
│   ├── Figure3_Correlation_Heatmap.png
│   ├── Figure4_Diagnostic_Plots.png
│   └── Figure5_Actual_vs_Predicted.png
└── supplementary/
    ├── regression_summary.txt
    ├── assumptions_tests.txt
    └── analysis_log.txt
```

---

## Support & Troubleshooting

### Import Errors
If you encounter `ModuleNotFoundError: No module named 'analysis_modules'`:
```python
import sys
sys.path.insert(0, '/workspaces/Testing')
import analysis_modules
```

### Data File Not Found
Ensure the CSV file path is correct:
```python
import os
os.listdir('ResearchData/')  # Check available files
```

### Version Compatibility
Check installed versions:
```python
import pandas as pd
import statsmodels as sm
print(f"pandas: {pd.__version__}")
print(f"statsmodels: {sm.__version__}")
```

---

## Contact & Questions

For questions about this analysis pipeline or methodology:
- Review the docstrings in each module (e.g., `help(fit_multiple_regression)`)
- Check assumptions.py for statistical test details
- Consult regression_model.py for model fitting specifics

---

**Last Updated:** February 2026
**Python Version:** 3.8+
**Status:** Production-ready for academic publication
