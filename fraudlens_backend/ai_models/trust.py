import pandas as pd
import re
import requests
import socket
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)


def check_ip_address(url):
    try:
        ip = socket.gethostbyname(urlparse(url).netloc)
        return 1 if re.match(r'\d+\.\d+\.\d+\.\d+', ip) else 0
    except:
        return 0

def check_shortening_service(url):
    shortening_services = ["bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co"]
    return 1 if any(service in url for service in shortening_services) else 0

def check_ssl_state(domain):
    try:
        response = requests.get("https://" + domain, timeout=3)
        return 1 if response.url.startswith("https") else 0
    except:
        return 0

def check_google_index(url):
    try:
        google_api = f"https://www.google.com/search?q=site:{url}"
        response = requests.get(google_api)
        return 1 if "did not match any documents" not in response.text else 0
    except:
        return 0

def check_dns_record(domain):
    try:
        socket.gethostbyname(domain)
        return 1
    except:
        return 0

def check_web_traffic(domain):
    try:
        alexa_api = f"https://data.alexa.com/data?cli=10&url={domain}"
        response = requests.get(alexa_api)
        return 1 if "RANK" in response.text else 0
    except:
        return 0

def extract_features(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    features = {
        "having_IP": check_ip_address(url),
        "URL_Length": len(url),
        "Shortening_Service": check_shortening_service(url),
        "having_At_Symbol": 1 if "@" in url else 0,
        "double_slash_redirecting": 1 if "//" in url[7:] else 0,
        "Prefix_Suffix": 1 if "-" in domain else 0,
        "having_Sub_Domain": domain.count('.') - 1,
        "SSLfinal_State": check_ssl_state(domain),
        "Domain_registeration_length": check_dns_record(domain),
        "Favicon": check_ssl_state(domain),
        "port": 1 if ":" in domain else 0,
        "HTTPS_token": 1 if "https" in domain else 0,
        "Request_URL": check_google_index(url),
        "URL_of_Anchor": check_google_index(url),
        "Links_in_tags": check_google_index(url),
        "SFH": check_google_index(url),
        "Submitting_to_email": check_google_index(url),
        "Abnormal_URL": check_google_index(url),
        "Redirect": 1 if "redirect" in url else 0,
        "on_mouseover": 0,
        "RightClick": 0,
        "popUpWidnow": 0,
        "Iframe": 0,
        "age_of_domain": check_dns_record(domain),
        "DNSRecord": check_dns_record(domain),
        "web_traffic": check_web_traffic(domain),
        "Page_Rank": check_web_traffic(domain),
        "Google_Index": check_google_index(url),
        "Links_pointing_to_page": check_google_index(url),
        "Statistical_report": check_google_index(url)
    }
    
    return list(features.values())

# Load dataset and train model
df = pd.read_csv(r".\ai_models\phishtank.csv")
features = df.drop(columns=["index", "Result"])  # Remove unnecessary columns
target = df["Result"].replace(-1, 0)  # Convert -1 to 0

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42, stratify=target)
model = XGBClassifier(n_estimators=100, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Function to predict trust score
def predict_trust_score(url):
    feature_values = extract_features(url)
    prediction = model.predict_proba([feature_values])[:, 1][0]  # Probability of being a scam
    trust_score = (prediction) * 100  # Convert to percentage (Higher = Safer)
    return round(trust_score, 2)

#Input URL to get FLTS
#Returns as list in form [int score, str flag, str message]
def run_trust(url):
    trust_score = predict_trust_score(url)
    if trust_score>=90:
        return {"trust_score": int(trust_score), "risk_level": "Very Safe","action": "Trusted & legitimate. No action needed."}
    elif trust_score>=75:
        return {"trust_score": int(trust_score),"risk_level": "Mostly Safe","action": "Likely safe but review if necessary."}
    elif trust_score>=50:
        return {"trust_score": int(trust_score),"risk_level": "Suspicious","action": "Monitor closely. Needs further checks."}
    elif trust_score>=30:
        return {"trust_score": int(trust_score),"risk_level": "High Risk","action": "Possibly fraudulent. Manual review advised."}
    elif trust_score>=10:
        return {"trust_score": int(trust_score),"risk_level": "Dangerous","action": "Strong signs of fraud. Block or investigate immediately."}
    else:
        return {"trust_score": int(trust_score), "risk_level": "Critical Fraud", "action": "Confirmed scam/phishing. Immediate action required."}