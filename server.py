from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from model_func import load_and_prepare_data, train_model_and_predict, flag_malicious_ips, calculate_accuracy

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    network_data = request.files['network_data']
    bad_ips = request.files['bad_ips']
    label_column = request.form['label_column']

    # Save uploaded files temporarily
    network_data.save('temp_network_data.csv')
    bad_ips.save('temp_bad_ips.csv')

    try:
        # Load and prepare data
        X, y, malicious_ips = load_and_prepare_data('temp_network_data.csv', 'temp_bad_ips.csv', label_column)

        # Train model and get predictions
        y_pred = train_model_and_predict(X, y)

        # Flag malicious IPs
        flagged_ips = flag_malicious_ips(X, malicious_ips)

        # Calculate accuracy
        accuracy = calculate_accuracy(X, y, malicious_ips)

        results = {
            'total_predictions': len(y_pred),
            'malicious_predictions': int(sum(y_pred)),
            'flagged_ips': flagged_ips,
            'num_flagged_ips': len(flagged_ips),
            'accuracy': accuracy
        }

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

    finally:
        # Clean up temporary files
        import os
        os.remove('temp_network_data.csv')
        os.remove('temp_bad_ips.csv')

if __name__ == '__main__':
    app.run(debug=True)