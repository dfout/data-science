import json
from collections import Counter
from datetime import datetime

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
               datetime.utcfromtimestamp(entry['SEND_DATE'] / 1000).month == month and
               datetime.utcfromtimestamp(entry['SEND_DATE'] / 1000).year == year
        ]

        # If no data for the specified month/year, use historical data
        if not relevant_data:
            # Use data from all months for that article
            relevant_data = [
                entry for entry in data
                if entry['ARTICLE'] == article
            ]

        if relevant_data:
            # Calculate the total quantity ordered for the article over all months
            total_quantity_ordered = sum([entry['QTY'] for entry in relevant_data])
            # Calculate the number of unique months present in the data for that article
            unique_months = len(set((datetime.utcfromtimestamp(entry['SEND_DATE'] / 1000).month,
                                     datetime.utcfromtimestamp(entry['SEND_DATE'] / 1000).year)
                                    for entry in relevant_data))
            # Calculate average monthly quantity ordered
            average_monthly_quantity = total_quantity_ordered / unique_months if unique_months > 0 else 0
            
            # Add buffer (e.g., 20% extra) to the prediction
            predicted_stock_needs[article] = int(average_monthly_quantity * 1.20)
        else:
            predicted_stock_needs[article] = "No data available for this article"

    return {
        "most_frequent_articles": most_frequent_articles,
        "predicted_stock_needs": predicted_stock_needs
    }

# Example usage:
file_path = 'EXTERNAL_PRODUCTIONS_converted.json'
analysis_results = analyze_stock(file_path, month=10, year=2023)  # Example: Predict for October 2023
print(analysis_results)

