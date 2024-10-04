import json
from collections import Counter
from datetime import datetime, timedelta

def analyze_stock(file_path, month, year):
    """
    Analyzes the most frequently ordered articles and predicts stock needs.

    Args:
        file_path (str): The path to the JSON file containing order data.
        month (int): The month to predict stock for (1-12).
        year (int): The year to predict stock for.

    Returns:
        dict: A dictionary containing:
            - "most_frequent_articles": A list of the most frequently ordered articles.
            - "predicted_stock_needs": A dictionary mapping article to predicted stock need.
    """

    with open(file_path, 'r') as f:
        data = json.load(f)

    # 1. Analyze Most Frequently Ordered Articles
    article_counts = Counter([entry['ARTICLE'] for entry in data])
    most_frequent_articles = [article for article, count in article_counts.most_common(5)]  # Get top 5

    # 2. Predictive Analysis for Stock Needs
    predicted_stock_needs = {}

    for article in most_frequent_articles:
        # Filter data for the specific article and target month/year
        relevant_data = [
            entry for entry in data
            if entry['ARTICLE'] == article and
               datetime.fromtimestamp(entry['SEND_DATE'] / 1000).month == month and
               datetime.fromtimestamp(entry['SEND_DATE'] / 1000).year == year
        ]

        # Simple prediction: Calculate average monthly quantity ordered
        total_quantity_ordered = sum([entry['QTY'] for entry in relevant_data])
        average_monthly_quantity = total_quantity_ordered / len(relevant_data) if relevant_data else 0

        # Add buffer (e.g., 20% extra) to the prediction
        predicted_stock_needs[article] = int(average_monthly_quantity * 1.20) 

    return {
        "most_frequent_articles": most_frequent_articles,
        "predicted_stock_needs": predicted_stock_needs
    }

# Example usage:
file_path = 'EXTERNAL_PRODUCTIONS_converted.json'
analysis_results = analyze_stock(file_path, month=10, year=2023)  # Example: Predict for October 2023
print(analysis_results)