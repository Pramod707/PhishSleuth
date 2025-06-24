import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# 1. Load Dataset
df = pd.read_csv("spam.csv", encoding='latin-1')[['v1', 'v2']]
df.columns = ['label', 'text']
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# 2. Split
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2)

# 3. Vectorize Text
vectorizer = TfidfVectorizer()
X_train_vect = vectorizer.fit_transform(X_train)

# 4. Train Model
model = MultinomialNB()
model.fit(X_train_vect, y_train)

# 5. Save Model and Vectorizer
joblib.dump(model, 'spam_model.pkl')
joblib.dump(vectorizer, 'spam_vectorizer.pkl')
print("✅ Model and vectorizer saved.")
