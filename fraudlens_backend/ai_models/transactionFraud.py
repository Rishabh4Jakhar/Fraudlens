import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE  
from sklearn.preprocessing import LabelEncoder  
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
df = pd.read_csv("transactions.csv")

# Convert date and extract day of the week
df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], dayfirst=True, errors='coerce')
df["Transaction_Day"] = df["Transaction_Date"].dt.dayofweek

# Remove unwanted columns (State, Transaction_Location, Age, Gender)
df.drop(columns=["Transaction_ID", "Customer_ID", "Transaction_Date", "City", "Bank_Branch",
                 "Customer_Name", "Customer_Contact", "Customer_Email", 
                 "Transaction_Location", "State", "Age", "Gender"], inplace=True)

# Assign Higher Fraud Risk to `Transaction_Currency`
currency_risk = {
    "Bitcoin": 5.0,  # Strong fraud risk
    "USD": 1.0,  
    "EUR": 1.5,  
    "INR": 0.8,  
    "GBP": 1.7,  
    "JPY": 1.8
}
df["Currency_Risk"] = df["Transaction_Currency"].map(currency_risk).fillna(1.0)

# Introduce Device Risk Factor
device_risk = {
    "Unregistered": 3.5,  # High fraud risk
    "Unknown": 3.0,
    "Web Browser": 1.5,
    "Android App": 1.2,
    "iOS App": 1.0
}
df["Device_Risk"] = df["Device_Type"].map(device_risk).fillna(1.0)

# **Boost Feature Importance for `Transaction_Currency` & `Device_Type`**
df["Transaction_Currency_Encoded"] = df["Transaction_Currency"]
df["Device_Type_Encoded"] = df["Device_Type"]
df["Currency_Device_Interaction"] = df["Currency_Risk"] * df["Device_Risk"]  # Interaction effect

# Define Features & Target
X = df.drop(columns=["Is_Fraud"])  # Exclude target column
y = df["Is_Fraud"]  # Target variable

# Identify categorical columns
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

# Encode categorical columns using Label Encoding
label_encoders = {}
for col in categorical_features:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le  # Save encoder for later use

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Apply SMOTE (Include 90% Fraud Cases)
smote = SMOTE(sampling_strategy=0.9, random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# Train LightGBM Model (Force `Transaction_Currency` & `Device_Type` to be in Top Features)
lgb_model = lgb.LGBMClassifier(
    n_estimators=800,  # More trees for feature separation
    learning_rate=0.015, 
    max_depth=20, 
    boosting_type='gbdt', 
    objective='binary', 
    feature_fraction=0.8,  # Higher chance of selecting important features
    min_gain_to_split=0.3,  
    importance_type='gain',  # Focus on important splits
    random_state=42
)
lgb_model.fit(X_train_smote, y_train_smote)

# Evaluate Model
y_pred = lgb_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Plot Feature Importance to Check Key Fraud Indicators
feature_importance = pd.Series(lgb_model.feature_importances_, index=X.columns)
feature_importance.nlargest(10).plot(kind='barh')
plt.title("Top 10 Feature Importance (Boosted `Transaction_Currency` & `Device_Type`)")
plt.show()

# Function to Predict Fraud (Currency & Device Type Impact Increased Further)
def predict_fraud(transaction, fraud_threshold=0.35):  # Adjusted threshold for better fraud detection
    transaction_df = pd.DataFrame([transaction])

    # Remove ignored features before prediction
    transaction_df.drop(columns=["State", "Transaction_Location", "Age", "Gender"], errors='ignore', inplace=True)

    # Assign Currency Risk & Device Risk Multiplier
    transaction_df["Currency_Risk"] = transaction_df["Transaction_Currency"].map(currency_risk).fillna(1.0)
    transaction_df["Device_Risk"] = transaction_df["Device_Type"].map(device_risk).fillna(1.0)
    transaction_df["Currency_Device_Interaction"] = transaction_df["Currency_Risk"] * transaction_df["Device_Risk"]

    # Encode categorical features
    for col, le in label_encoders.items():
        if col in transaction_df.columns:
            transaction_df[col] = transaction_df[col].map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        else:
            print(f"Warning: Column '{col}' is missing in input transaction! Assigning default value.")
            transaction_df[col] = -1  # Assign unknown category
    
    # Align columns with training data
    transaction_df = transaction_df.reindex(columns=X.columns, fill_value=0)

    # Use predict_proba() to get fraud probability & Scale with Currency & Device Risk
    fraud_prob = lgb_model.predict_proba(transaction_df)[:, 1][0] * transaction_df["Currency_Device_Interaction"].values[0]

    return "Fraudulent" if fraud_prob > fraud_threshold else "Legitimate"

# Example Test Cases (Currency & Device Type Have Even Stronger Effect)
legit_transaction = {
    "Transaction_Amount": 200.0,  
    "Account_Balance": 5000.0,  
    "Transaction_Time": 14,  
    "Transaction_Day": 2,  
    "Days_Since_First_Transaction": 1500,  
    "Account_Type": "Savings",
    "Transaction_Type": "Card Payment",
    "Merchant_Category": "Grocery",
    "Merchant_ID": "M56789",
    "Transaction_Device": "iOS App",
    "Transaction_Description": "Supermarket Purchase",
    "Device_Type": "iOS App",
    "Transaction_Currency": "USD"
}

fraud_transaction = {
    "Transaction_Amount": 9500.0,  
    "Account_Balance": 200.0,  
    "Transaction_Time": 2,  
    "Transaction_Day": 6,  
    "Days_Since_First_Transaction": 3,  
    "Account_Type": "Checking",
    "Transaction_Type": "Wire Transfer",
    "Merchant_Category": "Cryptocurrency",
    "Merchant_ID": "M98765",
    "Transaction_Device": "Unknown",
    "Transaction_Description": "Bitcoin Purchase",
    "Device_Type": "Unregistered",
    "Transaction_Currency": "Bitcoin"
}

print("Legitimate Transaction Status:", predict_fraud(legit_transaction))
print("Fraudulent Transaction Status:", predict_fraud(fraud_transaction))