import numpy as np
from flask import Flask, request
import pickle
from urllib.parse import urlparse
import re
import requests
import whois
import tldextract
import string
import datetime
from dateutil.relativedelta import relativedelta
from csv import reader
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

model = pickle.load(open('SVM_Model.pkl', 'rb'))

# Address Bar Features
def havingIP(url):
    index = url.find("://")
    split_url = url[index+3:]
    index = split_url.find("/")
    split_url = split_url[:index]
    split_url = split_url.replace(".", "")
    counter_hex = sum(1 for i in split_url if i in string.hexdigits)
    total_len = len(split_url)
    return 1 if counter_hex >= total_len else 0

sc = ['@','~','`','!','$','%','&']
def haveAtSign(url):
    for ch in sc:
        if ch in url:
            return 1
    return 0

def getLength(url):
    return 0 if len(url) < 54 else 1

def getDepth(url):
    return len([part for part in urlparse(url).path.split('/') if part != ''])

def redirection(url):
    pos = url.rfind('//')
    return 1 if pos > 6 else 0

def httpDomain(url):
    domain = urlparse(url).netloc
    return 1 if 'https' in domain else 0

shortening_services = r"(bit\.ly|goo\.gl|tinyurl\.com|ow\.ly|t\.co|bit\.do|is\.gd|cutt\.us|rb\.gy|shorte\.st|cli\.gs)"
def tinyURL(url):
    return 1 if re.search(shortening_services, url) else 0

def prefixSuffix(url):
    return 1 if '-' in urlparse(url).netloc else 0

# Domain Features
def domainAge(url):
    try:
        whois_res = whois.whois(url)
        creation_date = whois_res.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date is None:
            return 0
        return 0 if datetime.datetime.now() > creation_date + relativedelta(months=+6) else 1
    except:
        return 0

def domainEnd(domain_name):
    try:
        expiration_date = domain_name.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if expiration_date is None:
            return 0
        today = datetime.datetime.now()
        domainDate = abs((expiration_date - today).days)
        return 1 if (domainDate / 30) < 6 else 0
    except:
        return 0

# Tranco Web Traffic Integration
def web_traffic(url):
    try:
        domain = tldextract.extract(url).domain + '.' + tldextract.extract(url).suffix
        with open("tranco_top_sites.csv", 'r') as f:
            csv_reader = reader(f)
            for row in csv_reader:
                if domain.strip().lower() == row[1].strip().lower():
                    rank = int(row[0])
                    return 0 if rank < 100000 else 1
        return 1
    except:
        return 1

# HTML & JS Features
def iframe(response):
    if response == "":
        return 1
    return 0 if re.findall(r"[<iframe>|<frameBorder>]", response.text) else 1

def mouseOver(response):
    if response == "":
        return 1
    return 1 if re.findall("<script>.+onmouseover.+</script>", response.text) else 0

def forwarding(response):
    if response == "":
        return 1
    return 0 if len(response.history) <= 2 else 1

# Extra Feature - Known Safe List
def checkCSV(url):
    try:
        checkURL = urlparse(url).netloc
    except:
        return 1
    with open('Web_Scrapped_websites.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if row[0] == checkURL:
                return 0
    return 1

# Feature Extraction
def featureExtraction(url):
    features = []
    features.append(havingIP(url))
    features.append(haveAtSign(url))
    features.append(getLength(url))
    features.append(getDepth(url))
    features.append(redirection(url))
    features.append(httpDomain(url))
    features.append(tinyURL(url))
    features.append(prefixSuffix(url))

    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1

    features.append(dns)
    features.append(web_traffic(url))
    features.append(0 if dns == 1 else domainAge(url))
    features.append(0 if dns == 1 else domainEnd(domain_name))

    try:
        response = requests.get(url)
    except:
        response = ""

    features.append(iframe(response))
    features.append(mouseOver(response))
    features.append(forwarding(response))

    return features

# Routes
@app.route('/', methods=["GET", "POST"])
def home():
    return "Hello World"

@app.route('/post', methods=['POST'])
def predict():
    url = request.form['URL']
    dataPhish = checkCSV(url)

    if dataPhish == 0:
        return "0"

    features = featureExtraction(url)

    if features.count(0) == 15 or features.count(0) == 14:
        prediction = 0
    else:
        prediction = model.predict([features])[0]

    if prediction == 1 and dataPhish == 1:
        return "-1"
    else:
        return "1"

# ✅ Load spam classifier from sms-email-spam-classifier-main folder
spam_model = joblib.load("../sms-email-spam-classifier-main/model.pkl")
spam_vectorizer = joblib.load("../sms-email-spam-classifier-main/vectorizer.pkl")

@app.route('/predict_spam', methods=['POST'])
def predict_spam():
    message = request.form.get('message', '')
    if not message:
        return "Missing message", 400
    vector = spam_vectorizer.transform([message])
    prediction = spam_model.predict(vector)[0]
    return "spam" if prediction == 1 else "ham"

if __name__ == "__main__":
    app.run(debug=True)
