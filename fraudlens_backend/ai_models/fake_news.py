import pandas as pd
import numpy as np
import re
import string
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load cleaned dataset
df = pd.read_csv("Fraudlens/fraudlens_backend/ai_models/fake_news.csv")

# Drop empty rows (if any)
df.dropna(subset=['text', 'label'], inplace=True)

# Train-Test Split
X = df['text']  # News content
y = df['label']  # Target labels (1 = Fake, 0 = Real)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Text Vectorization using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")  
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train Logistic Regression Model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Predictions
y_pred = model.predict(X_test_tfidf)

# Model Evaluation
accuracy = accuracy_score(y_test, y_pred)

# Function to predict if a news article is fake
def predict_fake_news(news_text):
    news_vectorized = vectorizer.transform([news_text])
    prediction = model.predict(news_vectorized)[0]
    return {"result": "Fake News", "Accuracy": accuracy} if prediction == 1 else {"result": "Real News", "Accuracy": accuracy}

#Example run
#print(predict_fake_news("Donald Trump gets cheated on by his wife."))