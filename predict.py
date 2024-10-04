import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load the dataset
file_path = 'EXTERNAL_PRODUCTIONS_converted.xlsx'
df = pd.read_excel(file_path)

# Feature Engineering
# Calculate time to fulfillment in days
df['TIME_TO_COMPLETION'] = (df['RECEPTION_DATE'] - df['SEND_DATE']).dt.days

# Fill missing values in MISSING and REJECTED columns with 0 (assuming no error if NaN)
df['MISSING'].fillna(0, inplace=True)
df['REJECTED'].fillna(0, inplace=True)

# Create an 'ERROR' column where we flag orders with either missing or rejected items
df['ERROR'] = (df['MISSING'] > 0) | (df['REJECTED'] > 0)

# Features: TIME_TO_COMPLETION and QTY
X = df[['TIME_TO_COMPLETION', 'QTY']].fillna(0)  # Fill missing values with 0
y = df['ERROR'].astype(int)  # Convert boolean to int for classification

# Split data into training and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Use Random Forest Classifier with class weighting to handle imbalanced data
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Display the results
print(f"Accuracy: {accuracy:.2f}")
print("Confusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(class_report)

# Optionally, show the importance of features
importances = model.feature_importances_
feature_names = X.columns
feature_importances = pd.Series(importances, index=feature_names).sort_values(ascending=False)

print("\nFeature Importances:")
print(feature_importances)
