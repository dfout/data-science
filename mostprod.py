import json
import matplotlib.pyplot as plt

def find_most_productive_lots(filename, metric="Fruits/Plant"):
  """
  Finds the most productive lots based on a specified metric and plots them.

  Args:
    filename: The name of the JSON file.
    metric: The metric to use for determining productivity (default: "Fruits/Plant").
  """

  with open(filename, 'r') as f:
    data = json.load(f)

  # Extract relevant data
  lots = [(item['Lots'], item[metric]) for item in data]

  # Sort lots by yield in descending order
  sorted_lots = sorted(lots, key=lambda x: x[1], reverse=True)

  # Take only the top 5 most productive lots
  top_5_lots = sorted_lots[:5]

  # Extract numerical lot positions
  lot_positions = range(len(top_5_lots))

  # Extract yield values
  yield_per_lot = [item[1] for item in top_5_lots]

  # Create bar chart
  plt.figure(figsize=(12, 6))
  plt.bar(lot_positions, yield_per_lot)
  plt.title(f"Top 5 Most Productive Lots Based on {metric}")
  plt.xlabel("Lot Position")
  plt.ylabel(metric)
  plt.xticks([i for i in range(len(top_5_lots))], [lot for lot, _ in top_5_lots], rotation=45)
  plt.show()

  return sorted_lots  # Still return the sorted list

# Example usage
filename = "Last projection (1st flowering) - 2022_converted.json"
most_productive = find_most_productive_lots(filename, metric="Ton/Lot")
  