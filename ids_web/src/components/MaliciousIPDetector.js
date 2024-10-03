import React, { useState } from 'react';
import axios from 'axios';

function MaliciousIPDetector() {
    const [networkData, setNetworkData] = useState(null);
    const [badIPs, setBadIPs] = useState(null);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleNetworkDataUpload = (event) => {
        setNetworkData(event.target.files[0]);
    };

    const handleBadIPsUpload = (event) => {
        setBadIPs(event.target.files[0]);
    };

    const handleSubmit = async () => {
        if (!networkData || !badIPs) {
            alert('Please upload both files.');
            return;
        }

        setLoading(true);
        const formData = new FormData();
        formData.append('network_data', networkData);
        formData.append('bad_ips', badIPs);

        try {
            const response = await axios.post('http://localhost:5000/analyze', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setResults(response.data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the data.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-center mb-8 text-white">
                Malicious IP Detector
            </h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg shadow-md rounded-lg p-6">
                    <h2 className="text-2xl font-bold mb-4 text-white">Upload Network Data</h2>
                    <input
                        type="file"
                        accept=".csv"
                        onChange={handleNetworkDataUpload}
                        className="hidden"
                        id="network-data-upload"
                    />
                    <label
                        htmlFor="network-data-upload"
                        className="bg-violet-500 hover:bg-violet-700 text-white font-bold py-2 px-4 rounded inline-flex items-center cursor-pointer"
                    >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        Upload CSV
                    </label>
                    {networkData && <p className="mt-2 text-white">{networkData.name}</p>}
                </div>
                <div className="bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg shadow-md rounded-lg p-6">
                    <h2 className="text-2xl font-bold mb-4 text-white">Upload Bad IPs</h2>
                    <input
                        type="file"
                        accept=".csv"
                        onChange={handleBadIPsUpload}
                        className="hidden"
                        id="bad-ips-upload"
                    />
                    <label
                        htmlFor="bad-ips-upload"
                        className="bg-violet-500 hover:bg-violet-700 text-white font-bold py-2 px-4 rounded inline-flex items-center cursor-pointer"
                    >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        Upload CSV
                    </label>
                    {badIPs && <p className="mt-2 text-white">{badIPs.name}</p>}
                </div>
            </div>
            <button
                className={`w-full mt-6 py-2 px-4 rounded-lg text-white font-bold ${
                    loading
                        ? 'bg-gray-600 cursor-not-allowed'
                        : 'bg-blue-500 hover:bg-blue-600'
                }`}
                onClick={handleSubmit}
                disabled={loading}
            >
                {loading ? (
                    <svg className="animate-spin h-5 w-5 mr-3 inline-block" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                ) : (
                    'Analyze'
                )}
            </button>
            {results && (
                <div className="mt-8 bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg shadow-md rounded-lg p-6">
                    <h2 className="text-xl font-semibold mb-4 text-white">Results</h2>
                    <p className="text-white">{results.network_data_status}</p>
                    <p className="text-white">{results.network_data_prepared_status}</p>
                    <p className="text-white">{results.bad_ips_status}</p>
                    <p className="text-white">{results.malicious_ips_extracted}</p>
                    <p className="text-white">{results.flagged_ips}</p>
                    <p className="text-white">{results.accuracy}</p>
                </div>
            )}
        </div>
    );
}

export default MaliciousIPDetector;