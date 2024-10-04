import json
from collections import defaultdict

def analyze_articles(file_path):
    """
    Analyzes a JSON file containing article data and identifies the most
    frequently ordered articles and their reception patterns.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        tuple: A tuple containing:
            - A sorted list of tuples (article, count) representing the 
              most frequently ordered articles and their order counts.
            - A dictionary mapping each article to a list of its reception dates.
    """

    article_counts = defaultdict(int)
    reception_dates = defaultdict(list)

    with open(file_path, 'r') as f:
        data = json.load(f)

        for record in data:
            article = record.get('ARTICLE')
            reception_date = record.get('RECEPTION_DATE')
            if article and reception_date:
                article_counts[article] += 1
                reception_dates[article].append(reception_date)

    sorted_articles = sorted(article_counts.items(), key=lambda item: item[1], reverse=True)

    return sorted_articles, reception_dates

# Example usage:
file_path = 'EXTERNAL_PRODUCTIONS_converted.json'
sorted_articles, reception_dates = analyze_articles(file_path)

print("Most Frequently Ordered Articles:")
for article, count in sorted_articles:
    print(f"- {article}: {count} orders")

print("\nReception Dates:")
for article, dates in reception_dates.items():
    print(f"- {article}: {dates}") 