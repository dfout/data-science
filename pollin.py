import json
import matplotlib.pyplot as plt
import numpy as np

def plot_pollinator_fruit_per_plant_correlation(filename):
  """
  Plots the correlation between pollinators and fruit per plant, including a best-fit line.

  Args:
    filename: The name of the JSON file.
  """

  with open(filename, 'r') as f:
    data = json.load(f)

  # Extract relevant data
  pollinators = [item['Pollinators'] for item in data]
  fruits_per_plant = [item['Fruits/Plant'] for item in data]

  # Calculate correlation coefficient
  correlation_coefficient = np.corrcoef(pollinators, fruits_per_plant)[0, 1]

  # Create scatter plot
  plt.scatter(pollinators, fruits_per_plant, label="Data Points")

  # Calculate regression line coefficients
  slope, intercept = np.polyfit(pollinators, fruits_per_plant, 1)

  # Generate x values for the regression line
  x_fit = np.linspace(min(pollinators), max(pollinators), 100)

  # Calculate y values for the regression line
  y_fit = slope * x_fit + intercept

  # Plot the regression line
  plt.plot(x_fit, y_fit, color='red', label="Regression Line")

  # Set labels and title
  plt.xlabel("Pollinators")
  plt.ylabel("Fruits per Plant")
  plt.title(f"Correlation: {correlation_coefficient:.2f}")

  # Add legend
  plt.legend()

  # Show plot
  plt.show()

# Example usage
filename = "Last projection (1st flowering) - 2022_converted.json"
plot_pollinator_fruit_per_plant_correlation(filename)