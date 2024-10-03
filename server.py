from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from model_func import load_and_prepare_data, flag_malicious_ips, calculate_accuracy

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        network_data_file = request.files['network_data']
        bad_ips_file = request.files['bad_ips']
        
        network_data_path = 'temp_network_data.csv'
        bad_ips_path = 'temp_bad_ips.csv'
        
        network_data_file.save(network_data_path)
        bad_ips_file.save(bad_ips_path)
        
        X, y, malicious_ips = load_and_prepare_data(network_data_path, bad_ips_path)
        flagged_ips = flag_malicious_ips(X, malicious_ips)
        accuracy = calculate_accuracy(X, y, malicious_ips)
        
        response = {
            "network_data_status": "Network data loaded successfully.",
            "network_data_prepared_status": "Network data prepared successfully.",
            "bad_ips_status": "Bad IPs data loaded successfully.",
            "malicious_ips_extracted": f"Malicious IPs extracted: {malicious_ips}",
            "flagged_ips": f"Flagged IPs: {flagged_ips}",
            "accuracy": f"Accuracy: {accuracy}"
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)