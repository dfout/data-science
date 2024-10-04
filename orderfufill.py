import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def analyze_production_data(df):
    """
    Analyzes production data to calculate average production times, accuracy rates,
    and build a predictive model for error rates.

    Args:
        df (pd.DataFrame): DataFrame containing production data.

    Returns:
        None
    """
    
    # Convert date columns to datetime objects
    df['SEND_DATE'] = pd.to_datetime(df['SEND_DATE'])
    df['RECEPTION_DATE'] = pd.to_datetime(df['RECEPTION_DATE'])

    # Calculate production time
    df['PRODUCTION_TIME'] = (df['RECEPTION_DATE'] - df['SEND_DATE']).dt.days

    # Identify orders with errors
    df['HAS_ERRORS'] = (df['MISSING'] > 0) | (df['REJECTED'] > 0)

    # Calculate average production time for orders with and without errors
    avg_production_time_errors = df[df['HAS_ERRORS']]['PRODUCTION_TIME'].mean()
    avg_production_time_no_errors = df[~df['HAS_ERRORS']]['PRODUCTION_TIME'].mean()

    # Calculate overall accuracy rate
    accuracy_rate = (1 - (df['HAS_ERRORS'].sum() / len(df))) * 100

    print(f"Average production time for orders with errors: {avg_production_time_errors:.2f} days")
    print(f"Average production time for orders without errors: {avg_production_time_no_errors:.2f} days")
    print(f"Overall accuracy rate: {accuracy_rate:.2f}%")

    # Prepare data for predictive analysis
    X = df[['PRODUCTION_TIME', 'QTY']]
    y = df['HAS_ERRORS']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build and train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    train_accuracy = model.score(X_train, y_train) * 100
    test_accuracy = model.score(X_test, y_test) * 100

    print(f"Training accuracy: {train_accuracy:.2f}%")
    print(f"Testing accuracy: {test_accuracy:.2f}%")

    # Determine which feature has a greater effect (without showing coefficients)
    importance = model.coef_[0]  
    if abs(importance[0]) > abs(importance[1]):
        print("Production time has a stronger influence on error rates.")
    else:
        print("Quantity of items has a stronger influence on error rates.")

# Load the data (assuming the file is in the same directory)
df = pd.read_excel("EXTERNAL_PRODUCTIONS_converted.xlsx")

# Perform analysis
analyze_production_data(df)