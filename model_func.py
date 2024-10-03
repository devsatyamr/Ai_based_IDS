import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def load_and_prepare_data(network_data_path, bad_ips_path):
    # Load network data
    network_data = pd.read_csv(network_data_path)
    print("Network data loaded successfully.")
    
    # Assuming the network data does not have a label column
    X = network_data
    y = np.zeros(len(network_data))  # Dummy labels for compatibility
    print("Network data prepared successfully.")
    
    # Load bad IPs
    bad_ips_data = pd.read_csv(bad_ips_path)
    print("Bad IPs data loaded successfully.")
    
    # Extract the list of malicious IPs
    malicious_ips = bad_ips_data['IP'].tolist()
    print(f"Malicious IPs extracted: {malicious_ips}")
    
    return X, y, malicious_ips

def flag_malicious_ips(X, malicious_ips):
    flagged_ips = []
    
    for idx, row in X.iterrows():
        if row['Source'] in malicious_ips:
            flagged_ips.append(row['Source'])
        if row['Destination'] in malicious_ips:
            flagged_ips.append(row['Destination'])
    
    return sorted(set(flagged_ips))

def calculate_accuracy(X, y, malicious_ips):
    X['is_malicious'] = X.apply(lambda row: row['Source'] in malicious_ips or row['Destination'] in malicious_ips, axis=1)
    accuracy = (y == X['is_malicious']).mean()
    return accuracy

# Example usage
if __name__ == "__main__":
    network_data_path = 'dataset/final_transformed_network_traffic.csv'
    bad_ips_path = 'dataset/sample_bad_ips.csv'
    
    try:
        X, y, malicious_ips = load_and_prepare_data(network_data_path, bad_ips_path)
        flagged_ips = flag_malicious_ips(X, malicious_ips)
        accuracy = calculate_accuracy(X, y, malicious_ips)
        
        print(f"Flagged IPs: {flagged_ips}")
        print(f"Accuracy: {accuracy}")
    except Exception as e:
        print(f"An error occurred: {e}")