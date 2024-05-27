import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Data
data = {
    'Group': ['A'] * 10 + ['B'] * 10 + ['C'] * 10,
    'Score': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 2, 2, 2, 2, 3, 2, 3, 2, 2]
}

df = pd.DataFrame(data)

# Perform ANOVA for each pair of groups
def perform_anova(group1, group2):
    formula = 'Score ~ C(Group)'
    model = ols(formula, df[df['Group'].isin([group1, group2])]).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    return anova_table

# Function to perform post hoc Tukey's HSD test
def perform_tukeyhsd():
    tukey_result = pairwise_tukeyhsd(df['Score'], df['Group'])
    return tukey_result

# Function to create comparison tables including ANOVA and Tukey's HSD results
def create_comparison_table(group1, group2):
    anova_result = perform_anova(group1, group2)
    tukey_result = perform_tukeyhsd()
    
    try:
        mean = df[df['Group'].isin([group1, group2])]['Score'].mean()
        median = df[df['Group'].isin([group1, group2])]['Score'].median()
        mode = df[df['Group'].isin([group1, group2])]['Score'].mode().iloc[0]
    except IndexError:
        mean = np.nan
        median = np.nan
        mode = np.nan
    
    # Format ANOVA p-value to standard format with 4 decimal places
    anova_p_value = '{:.4f}'.format(anova_result['PR(>F)'][0])
    
    table = pd.DataFrame({
        'Statistic': ['Mean', 'Median', 'Mode', 'F-statistic', 'p-value', 'Tukey HSD', 'ANOVA p-value'],
        'Group Comparison': [mean, median, mode, anova_result['F'][0], anova_p_value, str(tukey_result), anova_p_value]
    })
    return table

# Create comparison tables including ANOVA and Tukey's HSD results
print("Comparison of Group A with Group B:")
print(create_comparison_table('A', 'B'))
print("\nComparison of Group A with Group C:")
print(create_comparison_table('A', 'C'))
print("\nComparison of Group B with Group C:")
print(create_comparison_table('B', 'C'))


AB= create_comparison_table('A', 'B')
AC= create_comparison_table('A', 'C')
BC= create_comparison_table('B', 'C')

AB.to_csv("AB_new.csv")

