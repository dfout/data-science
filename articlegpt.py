import json
from collections import defaultdict, Counter
from datetime import datetime

def analyze_articles(file_path):
    """
    Analyzes a JSON file containing article data, identifies the most
    frequently ordered articles, and suggests stock levels based on ordering patterns.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        tuple: A tuple containing:
            - A sorted list of tuples (article, count) representing the 
              most frequently ordered articles and their order counts.
            - A dictionary mapping each article to a summarized reception frequency.
            - A stock prediction based on past order frequency.
    """

    article_counts = defaultdict(int)
    reception_dates = defaultdict(list)

    with open(file_path, 'r') as f:
        data = json.load(f)

        for record in data:
            article = record.get('ARTICLE')
            reception_timestamp = record.get('RECEPTION_DATE')
            
            if article and reception_timestamp:
                reception_date = datetime.fromtimestamp(reception_timestamp / 1000)  # Convert ms to date
                article_counts[article] += 1
                reception_dates[article].append(reception_date)

    # Sort articles by their order count
    sorted_articles = sorted(article_counts.items(), key=lambda item: item[1], reverse=True)

    # Summarize reception frequency by month
    summarized_receptions = {
        article: summarize_receptions(dates)
        for article, dates in reception_dates.items()
    }

    # Predict stock requirements based on historical ordering patterns
    stock_predictions = predict_stock_requirements(summarized_receptions)

    return sorted_articles, summarized_receptions, stock_predictions


def summarize_receptions(dates):
    """
    Summarizes the reception dates by counting how many orders occurred per month.
    
    Args:
        dates (list): List of datetime objects representing reception dates.
    
    Returns:
        dict: A dictionary summarizing the count of receptions per month.
    """
    monthly_counts = Counter(date.strftime('%Y-%m') for date in dates)
    return dict(monthly_counts)


def predict_stock_requirements(summarized_receptions):
    """
    Predicts stock levels based on past monthly order patterns using a simple moving average.

    Args:
        summarized_receptions (dict): Dictionary with monthly reception counts.

    Returns:
        dict: Predicted stock level for each article.
    """
    stock_predictions = {}
    
    for article, monthly_data in summarized_receptions.items():
        # Convert monthly data to a list of counts for stock prediction
        monthly_orders = list(monthly_data.values())
        
        if len(monthly_orders) >= 3:
            # Simple average of last 3 months for stock prediction
            predicted_stock = sum(monthly_orders[-3:]) // 3
        else:
            predicted_stock = sum(monthly_orders) // len(monthly_orders)  # Average all available data

        stock_predictions[article] = predicted_stock
    
    return stock_predictions

# Example usage:
file_path = 'EXTERNAL_PRODUCTIONS_converted.json'
sorted_articles, summarized_receptions, stock_predictions = analyze_articles(file_path)

# Print the most frequently ordered articles
print("Most Frequently Ordered Articles:")
for article, count in sorted_articles:
    print(f"- {article}: {count} orders")

# Print stock predictions
print("\nPredicted Stock Requirements (based on average monthly orders):")
for article, predicted_stock in stock_predictions.items():
    print(f"- {article}: Predicted stock level: {predicted_stock} units")
