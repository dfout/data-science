import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def analyze_production(file):
    """
    Analyzes production data from an Excel file.

    Args:
        filename (str): The name of the Excel file.

    Returns:
        None. Prints results to the console.
    """

    df = pd.read_excel(file)

    # Calculate production time
    df["SEND_DATE"] = pd.to_datetime(df["SEND_DATE"], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df["RECEPTION_DATE"] = pd.to_datetime(df["RECEPTION_DATE"], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df["PRODUCTION_TIME"] = (df["RECEPTION_DATE"] - df["SEND_DATE"]).dt.days

    # Identify orders with and without errors
    df["HAS_ERRORS"] = (df["MISSING"] > 0) | (df["REJECTED"] > 0)

    # Calculate average production time for orders with errors
    avg_production_time_with_errors = df[df["HAS_ERRORS"] == True]["PRODUCTION_TIME"].mean()

    # Calculate average production time for orders without errors
    avg_production_time_without_errors = df[df["HAS_ERRORS"] == False]["PRODUCTION_TIME"].mean()

    # Calculate accuracy rate
    total_orders = len(df)
    accurate_orders = len(df[df["HAS_ERRORS"] == False])
    accuracy_rate = (accurate_orders / total_orders) * 100

    print(f"Average Production Time (Orders with Errors): {avg_production_time_with_errors:.2f} days")
    print(f"Average Production Time (Orders without Errors): {avg_production_time_without_errors:.2f} days")
    print(f"Average Accuracy Rate: {accuracy_rate:.2f}%")

    # Predictive Analysis: Does quantity or production time affect error rates more?
    # Ensure QTY and PRODUCTION_TIME are numeric
    df["QTY"] = pd.to_numeric(df["QTY"], errors='coerce')  # Convert to numeric and coerce errors
    df["PRODUCTION_TIME"] = pd.to_numeric(df["PRODUCTION_TIME"], errors='coerce')  # Ensure it's numeric

    # Prepare data for regression 
    X = df[["QTY", "PRODUCTION_TIME"]].fillna(df[["QTY", "PRODUCTION_TIME"]].mean())  # Replace potential NaN values with column mean
    y = df["HAS_ERRORS"].astype(int)  # Convert boolean to int for regression

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Get the coefficients (impact) of quantity and production time
    quantity_impact = model.coef_[0]
    production_time_impact = model.coef_[1]

    print("\nPredictive Analysis:")
    if abs(quantity_impact) > abs(production_time_impact):
        print("Quantity of items has a greater impact on error rates than production time.")
    elif abs(quantity_impact) < abs(production_time_impact):
        print("Production time has a greater impact on error rates than the quantity of items.")
    else:
        print("Quantity and production time have a similar impact on error rates.")

# Example usage:
analyze_production("EXTERNAL_PRODUCTIONS_converted.xlsx")
