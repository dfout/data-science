import json
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

def analyze_pollinators_vs_fruits(dataset_path):
  """
  Analyzes the correlation between the number of pollinators and fruits per plant.

  Args:
    dataset_path: Path to the JSON file containing the dataset.

  Returns:
    None. Displays a scatter plot with regression line and correlation coefficient.
  """

  with open(dataset_path, 'r') as f:
    data = json.load(f)

  pollinators = [entry["Pollinators"] for entry in data]
  fruits_per_plant = [entry["Fruits/Plant"] for entry in data]

  # Calculate Pearson correlation coefficient
  correlation_coefficient, _ = pearsonr(pollinators, fruits_per_plant)

  # Create scatter plot
  plt.figure(figsize=(10, 6))
  plt.scatter(pollinators, fruits_per_plant, alpha=0.5)
  plt.title('Correlation between Pollinators and Fruits per Plant')
  plt.xlabel('Number of Pollinators')
  plt.ylabel('Fruits per Plant')

  # Add regression line
  m, b = np.polyfit(pollinators, fruits_per_plant, 1)  # Calculate regression line
  plt.plot(pollinators, m*np.array(pollinators) + b, color='red')  # Plot regression line

  # Display correlation coefficient on the plot
  plt.text(0.05, 0.95, f'Correlation: {correlation_coefficient:.2f}', 
           transform=plt.gca().transAxes, fontsize=12)

  plt.grid(True)
  plt.show()


# Replace 'Last projection (1st flowering) - 2022_converted.json' with the actual path
analyze_pollinators_vs_fruits('Last projection (1st flowering) - 2022_converted.json') 