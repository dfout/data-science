import json
from datetime import datetime

def transform_data(file_path):
    """
    Transforms the SEND_DATE column to YYYY-MM-DD format and
    combines ARTICLE and SIZE columns into a new ARTICLE_SIZE column.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        list: The transformed data.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return []

    transformed_data = []
    for item in data:
        # Convert Unix timestamp to YYYY-MM-DD with error handling
        timestamp = item.get('SEND_DATE')
        if isinstance(timestamp, (int, float)):
            try:
                # Assuming timestamp is in seconds; adjust if in milliseconds
                if timestamp > 10**10:  # Consider it as milliseconds
                    timestamp /= 1000
                formatted_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            except ValueError:
                formatted_date = "Invalid Date"
        else:
            formatted_date = "Missing Date"
        
        item['SEND_DATE'] = formatted_date

        # Combine ARTICLE and SIZE columns
        article = item.get('ARTICLE', 'Unknown Article')
        size = item.get('SIZE', 'Unknown Size')
        item['ARTICLE_SIZE'] = f"{article}-{size}"

        transformed_data.append(item)

    return transformed_data

# Example usage
file_path = "EXTERNAL_PRODUCTIONS_converted.json"
transformed_data = transform_data(file_path)

# Output the transformed data
if transformed_data:
    print(json.dumps(transformed_data, indent=2))