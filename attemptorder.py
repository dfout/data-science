import pandas as pd

def analyze_production(file):
    """
    Analyzes production data from an Excel file to calculate:

    - Average production time for orders with errors.
    - Average production time for orders without errors.
    - Average accuracy rate.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        None: Prints the results to the console.
    """
    # Load the Excel file into a pandas DataFrame
    try:
        df = pd.read_excel(file)
    except FileNotFoundError:
        print(f"Error: File not found at 'EXTERNAL_PRODUCTIONS_converted.xlsx'. Please check the file path.")
        return

    # Convert date columns to datetime objects (assuming they are in a recognizable format)
    df['SEND_DATE'] = pd.to_datetime(df['SEND_DATE'])
    df['RECEPTION_DATE'] = pd.to_datetime(df['RECEPTION_DATE'])

    # Calculate production time in days
    df['PRODUCTION_TIME'] = (df['RECEPTION_DATE'] - df['SEND_DATE']).dt.days

    # Identify orders with and without errors
    df['ERRORS'] = (df['MISSING'] > 0) | (df['REJECTED'] > 0)

    # Calculate average production times
    average_time_with_errors = df[df['ERRORS']]['PRODUCTION_TIME'].mean()
    average_time_without_errors = df[~df['ERRORS']]['PRODUCTION_TIME'].mean()

    # Calculate accuracy rate
    total_orders = len(df)
    accurate_orders = len(df[~df['ERRORS']])
    accuracy_rate = (accurate_orders / total_orders) * 100

    # Print the results
    print("Production Analysis:")
    print(f"Average Production Time (Orders with Errors): {average_time_with_errors:.2f} days")
    print(f"Average Production Time (Orders without Errors): {average_time_without_errors:.2f} days")
    print(f"Average Accuracy Rate: {accuracy_rate:.2f}%")

# Call the function to perform the analysis
analyze_production("EXTERNAL_PRODUCTIONS_converted.xlsx") 