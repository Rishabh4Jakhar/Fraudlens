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

# **Target Encoding for `Transaction_Currency` (Fraud Likelihood)**
currency_fraud_prob = df.groupby("Transaction_Currency")["Is_Fraud"].mean().to_dict()
df["Transaction_Currency_Encoded"] = df["Transaction_Currency"].map(currency_fraud_prob).fillna(0.5)
df["Transaction_Currency_Encoded"] += np.random.uniform(-0.01, 0.01, df.shape[0])  

# **Force Splitting on `Transaction_Currency`**
df["Transaction_Currency_Dup1"] = df["Transaction_Currency_Encoded"]*5
df["Transaction_Currency_Dup2"] = df["Transaction_Currency_Encoded"]*5
df["Transaction_Currency_Dup1"] += np.random.uniform(-0.01, 0.01, df.shape[0])
df["Transaction_Currency_Dup2"] += np.random.uniform(-0.01, 0.01, df.shape[0])


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

# Train LightGBM Model (Boosting `Transaction_Currency`)
lgb_model = lgb.LGBMClassifier(
    n_estimators=1000,  
    learning_rate=0.015,  
    max_depth=25,  
    boosting_type='gbdt',  
    objective='binary',  
    feature_fraction=0.5,  # Forces stronger feature selection
    min_gain_to_split=2.0,  # Makes currency duplicates more attractive
    importance_type='gain',  
    lambda_l1=2.0,  # Adds regularization to prevent overfitting
    random_state=42
)




weights = np.ones(df.shape[0])  
weights[df["Transaction_Currency_Dup1"] > 0.5] *= 2  # Boost impact
weights[df["Transaction_Currency_Dup2"] > 0.5] *= 2  # Boost impact

lgb_model.fit(X_train_smote, y_train_smote, sample_weight=weights)



# Evaluate Model
y_pred = lgb_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# **Plot Feature Importance (Currency Should Now Be Among Top 3)**
feature_importance = pd.Series(lgb_model.feature_importances_, index=X.columns)
feature_importance.nlargest(20).plot(kind='barh')
plt.title("Top 10 Feature Importance (Boosted `Transaction_Currency`)")
plt.show()

# Function to Predict Fraud
def predict_fraud(transaction, fraud_threshold=0.2):  
    transaction_df = pd.DataFrame([transaction])

    # Remove ignored features before prediction
    transaction_df.drop(columns=["State", "Transaction_Location", "Age", "Gender"], errors='ignore', inplace=True)

    # Apply Target Encoding for `Transaction_Currency`
    transaction_df["Transaction_Currency_Encoded"] = transaction_df["Transaction_Currency"].map(currency_fraud_prob).fillna(0.5)

    # **Force Splitting on `Transaction_Currency`**
    transaction_df["Transaction_Currency_Dup1"] = transaction_df["Transaction_Currency_Encoded"]
    transaction_df["Transaction_Currency_Dup2"] = transaction_df["Transaction_Currency_Encoded"]
    transaction_df["Currency_Transaction_Amount"] = transaction_df["Transaction_Currency_Encoded"] * transaction_df["Transaction_Amount"]

    # Encode categorical features
    for col, le in label_encoders.items():
        if col in transaction_df.columns:
            transaction_df[col] = transaction_df[col].map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        else:
            print(f"Warning: Column '{col}' is missing in input transaction! Assigning default value.")
            transaction_df[col] = -1  # Assign unknown category
    
    # Align columns with training data
    transaction_df = transaction_df.reindex(columns=X.columns, fill_value=0)

    # Use predict_proba() to get fraud probability
    fraud_prob = lgb_model.predict_proba(transaction_df)[:, 1][0]

    return "Fraudulent" if fraud_prob > fraud_threshold else "Legitimate"

# Example Test Cases
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
    "Transaction_Amount": 9500000.0,  # Extremely high transaction amount
    "Account_Balance": 2000.0,  # Low balance, likely insufficient funds
    "Transaction_Time": 2,  # Unusual hour for transactions (2 AM)
    "Transaction_Day": 6,  # Weekend transaction (higher risk)
    "Days_Since_First_Transaction": 1,  # New account, high-risk behavior
    "Account_Type": "Checking",  # Checking account often used for daily transactions, not large transfers
    "Transaction_Type": "Wire Transfer",  # High-risk transaction type
    "Merchant_Category": "Cryptocurrency",  # Cryptocurrency transactions are high-risk
    "Merchant_ID": "M98765",  # Unrecognized merchant
    "Transaction_Device": "Unknown",  # Device not registered to the account
    "Transaction_Description": "Bitcoin Purchase",  # Common fraud pattern
    "Device_Type": "Unregistered",  # Device never seen before
    "Transaction_Currency": "Bitcoin"  # High-risk currency
}


print("Legitimate Transaction Status:", predict_fraud(legit_transaction))
print("Fraudulent Transaction Status:", predict_fraud(fraud_transaction))
