import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def analyze_production_data(df):
    """
    Analyzes production data to calculate average production times, accuracy rates, 
    and predict the impact of production time and quantity on error rates.

    Args:
        df (pd.DataFrame): DataFrame containing the production data.

    Returns:
        None
    """
    
    # Calculate production time
    df['SEND_DATE'] = pd.to_datetime(df['SEND_DATE'])
    df['RECEPTION_DATE'] = pd.to_datetime(df['RECEPTION_DATE'])
    df['PRODUCTION_TIME'] = (df['RECEPTION_DATE'] - df['SEND_DATE']).dt.days

    # Identify orders with and without errors
    df['HAS_ERRORS'] = (df['MISSING'] > 0) | (df['REJECTED'] > 0)

    # Calculate average production time for orders with errors
    avg_production_time_errors = df[df['HAS_ERRORS']]['PRODUCTION_TIME'].mean()

    # Calculate average production time for orders without errors
    avg_production_time_no_errors = df[~df['HAS_ERRORS']]['PRODUCTION_TIME'].mean()

    # Calculate average accuracy rate
    total_orders = len(df)
    orders_with_errors = len(df[df['HAS_ERRORS']])
    accuracy_rate = ((total_orders - orders_with_errors) / total_orders) * 100

    # --- Predictive Analysis ---
    # Prepare the data for predictive analysis
    X = df[['PRODUCTION_TIME', 'QTY']]
    y = df['HAS_ERRORS']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # --- Print Results ---
    print(f"Average Production Time (Orders with Errors): {avg_production_time_errors:.2f} days")
    print(f"Average Production Time (Orders without Errors): {avg_production_time_no_errors:.2f} days")
    print(f"Average Accuracy Rate: {accuracy_rate:.2f}%")

    # Determine which factor has a larger impact on error rates based on coefficients 
    # ... (code to interpret and compare coefficients) ...
    if abs(model.coef_[0]) > abs(model.coef_[1]):
        print("Production time has a larger impact on error rates.")
    else:
        print("Quantity has a larger impact on error rates.")

# Load the data from the Excel file
df = pd.read_excel("EXTERNAL_PRODUCTIONS_converted.xlsx")

# Analyze the production data
analyze_production_data(df)