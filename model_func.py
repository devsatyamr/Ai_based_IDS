import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def load_and_prepare_data(network_data_path, bad_ips_path, label_column):
    # Load network data
    network_data = pd.read_csv(network_data_path)
    
    # Check if the label column exists
    if label_column not in network_data.columns:
        raise ValueError(f"Network data CSV must contain a '{label_column}' column.")
    
    X = network_data.drop(label_column, axis=1)
    y = network_data[label_column]

    # Load bad IPs
    bad_ips_data = pd.read_csv(bad_ips_path)
    
    # Check if the first column contains IPs
    ip_column = bad_ips_data.columns[0]
    if bad_ips_data[ip_column].dtype != object:
        raise ValueError("Bad IPs CSV must have IP addresses in the first column.")
    
    malicious_ips = set(bad_ips_data[ip_column].astype(str))

    return X, y, malicious_ips

def train_model_and_predict(X, y):
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    y_pred = model.predict(X)
    return y_pred

def flag_malicious_ips(X, malicious_ips):
    source_columns = [col for col in X.columns if col.startswith('Source_')]
    flagged_ips = []

    for idx, row in X.iterrows():
        for col in source_columns:
            if row[col] == 1:
                ip = col.split('_', 1)[1]
                if ip in malicious_ips:
                    flagged_ips.append(ip)

    return sorted(set(flagged_ips))

def calculate_accuracy(X, y, malicious_ips):
    source_columns = [col for col in X.columns if col.startswith('Source_')]
    X['is_malicious'] = X[source_columns].apply(lambda row: any(col.split('_', 1)[1] in malicious_ips for col, val in row.items() if val == 1), axis=1)
    accuracy = (y == X['is_malicious']).mean()
    return accuracy