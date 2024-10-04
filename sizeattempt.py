import pandas as pd
from scipy import stats

# Load the Excel data into a pandas DataFrame
df = pd.read_excel('EXTERNAL_PRODUCTIONS_converted.xlsx')

# Combine 'MISSING' and 'REJECTED' columns to create a 'TOTAL_ERRORS' column
df['TOTAL_ERRORS'] = df['MISSING'] + df['REJECTED']

# Group the data by 'SIZE' and calculate the total errors and total quantity for each size
grouped_by_size = df.groupby('SIZE').agg({'TOTAL_ERRORS': 'sum', 'QTY': 'sum'})

# Calculate the error rate for each size
grouped_by_size['ERROR_RATE'] = grouped_by_size['TOTAL_ERRORS'] / grouped_by_size['QTY']

# Perform an ANOVA test to determine if there is a significant difference in error rates between sizes
groups = []
for size, data in grouped_by_size.groupby('SIZE'):
    groups.append(data['ERROR_RATE'].dropna())
fvalue, pvalue = stats.f_oneway(*groups)

# Print the results
print(f"F-value: {fvalue}")
print(f"P-value: {pvalue}")

# Interpretation
if pvalue < 0.05:
    print("The p-value is less than 0.05, indicating that there is a significant difference in error rates between sizes.")
else:
    print("The p-value is greater than 0.05, indicating that there is no significant difference in error rates between sizes.")