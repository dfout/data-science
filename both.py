import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler

def analyze_order_fulfillment(filename):
    """
    Analyzes order fulfillment time, accuracy, and predicts errors based on time to completion and quantity.

    Args:
        filename: The path to the Excel file containing the order data.

    Returns:
        A tuple containing:
        - Average production time for orders with errors
        - Average production time for orders without errors
        - Order fulfillment accuracy rate
        - Accuracy, confusion matrix, and classification report of the predictive model
    """
    
    # Read data into a DataFrame
    df = pd.read_excel(filename)

    # Convert SEND_DATE and RECEPTION_DATE to datetime, coercing invalid dates to NaT
    df['SEND_DATE'] = pd.to_datetime(df['SEND_DATE'], errors='coerce')
    df['RECEPTION_DATE'] = pd.to_datetime(df['RECEPTION_DATE'], errors='coerce')

    # Drop rows with NaT in date columns (optional, depending on your data requirements)
    df = df.dropna(subset=['SEND_DATE', 'RECEPTION_DATE'])

    # Fill NaN in 'MISSING' and 'REJECTED' columns with 0, assuming no errors for missing values
    df['MISSING'] = df['MISSING'].fillna(0)
    df['REJECTED'] = df['REJECTED'].fillna(0)

    # Calculate time to fulfillment in days
    df['Time_to_Fulfillment'] = (df['RECEPTION_DATE'] - df['SEND_DATE']).dt.days

    # Calculate average production time for orders with errors (MISSING or REJECTED >= 1)
    with_errors = df[(df['MISSING'] >= 1) | (df['REJECTED'] >= 1)]
    avg_time_with_errors = with_errors['Time_to_Fulfillment'].mean()

    # Calculate average production time for orders without errors (MISSING == 0 and REJECTED == 0)
    without_errors = df[(df['MISSING'] == 0) & (df['REJECTED'] == 0)]
    avg_time_without_errors = without_errors['Time_to_Fulfillment'].mean()

    # Calculate overall order fulfillment accuracy rate
    total_orders = df.shape[0]
    accurate_orders = without_errors.shape[0]
    accuracy_rate = (accurate_orders / total_orders) * 100 if total_orders > 0 else 0

    # Feature Engineering for Prediction
    df['ERRORS'] = (df['MISSING'] > 0) | (df['REJECTED'] > 0)

    # Select relevant features for prediction
    X = df[['Time_to_Fulfillment', 'QTY']]
    y = df['ERRORS'].astype(int)  # 1 if there are errors, 0 otherwise

    # Handle any NaN or infinite values in features (if any)
    X = X.replace([np.inf, -np.inf], np.nan).dropna()

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train a Random Forest Classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_scaled, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test_scaled)

    # Calculate accuracy, confusion matrix, and classification report
    accuracy = accuracy_score(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    # Feature importance analysis
    feature_importances = pd.Series(model.feature_importances_, index=X.columns)

    # Print the results
    print("\n--- Production Time & Accuracy Analysis ---")
    print(f"Average production time for orders with errors: {avg_time_with_errors:.2f} days")
    print(f"Average production time for orders without errors: {avg_time_without_errors:.2f} days")
    print(f"Order fulfillment accuracy rate: {accuracy_rate:.2f}%")

    print("\n--- Predictive Model Analysis ---")
    print(f"Model Accuracy: {accuracy:.2f}")
    print(f"Confusion Matrix:\n{confusion}")
    print(f"Classification Report:\n{report}")
    print(f"Feature Importances:\n{feature_importances}")

    return avg_time_with_errors, avg_time_without_errors, accuracy_rate, accuracy, confusion, report

# Assuming the filename is correct
filename = "EXTERNAL_PRODUCTIONS_converted.xlsx"
results = analyze_order_fulfillment(filename)
