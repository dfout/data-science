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
        dict: A dictionary containing:
            - "most_frequent_articles": A list of the most frequently ordered articles.
            - "predicted_stock_needs": A dictionary mapping article to predicted stock need.
    """

    article_counts = defaultdict(int)
    reception_dates = defaultdict(list)

    with open(file_path, 'r') as f:
        data = json.load(f)

        for record in data:
            article = record.get('ARTICLE')
            reception_timestamp = record.get('RECEPTION_DATE')
            qty = record.get('QTY')

            if article and reception_timestamp and qty is not None:
                reception_date = datetime.fromtimestamp(reception_timestamp / 1000)  # Convert ms to date
                article_counts[article] += qty  # Aggregate total quantity ordered
                reception_dates[article].append(reception_date)

    # Sort articles by their total order count
    most_frequent_articles = sorted(article_counts.items(), key=lambda item: item[1], reverse=True)
    most_frequent_articles_list = [article for article, _ in most_frequent_articles[:5]]  # Top 5 articles

    # Predict stock requirements based on historical ordering patterns
    predicted_stock_needs = predict_stock_requirements(reception_dates)

    return {
        "most_frequent_articles": most_frequent_articles_list,
        "predicted_stock_needs": predicted_stock_needs
    }


def predict_stock_requirements(reception_dates):
    """
    Predicts stock levels based on past monthly order patterns using a simple moving average.

    Args:
        reception_dates (dict): Dictionary with reception dates for each article.

    Returns:
        dict: Predicted stock level for each article in units per month.
    """
    stock_predictions = {}
    
    for article, dates in reception_dates.items():
        # Summarize monthly orders
        monthly_orders = Counter(date.strftime('%Y-%m') for date in dates)

        # Convert monthly data to a list of counts for stock prediction
        order_counts = list(monthly_orders.values())
        
        if len(order_counts) >= 3:
            # Simple average of last 3 months for stock prediction
            predicted_stock = sum(order_counts[-3:]) // 3
        elif order_counts:
            predicted_stock = sum(order_counts) // len(order_counts)  # Average all available data
        else:
            predicted_stock = 0  # No orders found

        stock_predictions[article] = predicted_stock
    
    return stock_predictions


# Example usage:
file_path = 'EXTERNAL_PRODUCTIONS_converted.json'
analysis_results = analyze_articles(file_path)

# Print the results
print(analysis_results)
