import json
import matplotlib.pyplot as plt
from scipy.stats import linregress

def analyze_pollinators_vs_fruit(json_file):
  """
  Analyzes the correlation between pollinators and fruits per plant from a JSON dataset.

  Args:
    json_file: Path to the JSON file containing the dataset.

  Returns:
    None. Displays a scatter plot with regression line and correlation coefficient.
  """

  with open(json_file, 'r') as f:
    data = json.load(f)

  pollinators = [entry['Pollinators'] for entry in data]
  fruits_per_plant = [entry['Fruits\/Plant'] for entry in data]

  # Perform linear regression
  slope, intercept, r_value, p_value, std_err = linregress(pollinators, fruits_per_plant)

  # Create scatter plot
  plt.figure(figsize=(10, 6))
  plt.scatter(pollinators, fruits_per_plant, alpha=0.7)
  plt.xlabel('Number of Pollinators')
  plt.ylabel('Fruits per Plant')
  plt.title('Correlation between Pollinators and Fruits per Plant')

  # Add regression line
  plt.plot(pollinators, [slope * x + intercept for x in pollinators], color='red', label='Regression Line')

  # Display correlation coefficient
  plt.annotate(f'Correlation Coefficient (r): {r_value:.2f}', xy=(0.05, 0.95), xycoords='axes fraction')

  plt.legend()
  plt.grid(True)
  plt.show()

# Replace 'your_file.json' with the actual path to your JSON file
analyze_pollinators_vs_fruit('Last projection (1st flowering) - 20222_converted.json') 