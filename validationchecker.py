from flask import Flask, request, jsonify
from azure.identity import DefaultAzureCredential
from azure.keyvault.certificates import CertificateClient
import requests
import uuid

app = Flask(__name__)

# Initialize Key Vault client
key_vault_name = "your-key-vault-name"
kv_uri = f"https://{key_vault_name}.vault.azure.net"
credential = DefaultAzureCredential()
certificate_client = CertificateClient(vault_url=kv_uri, credential=credential)

@app.route('/start', methods=['GET'])
def start():
    # Generate a unique webid
    webid = str(uuid.uuid4())

    # Retrieve certificate info from Key Vault
    certificate_name = "your-certificate-name"
    certificate = certificate_client.get_certificate(certificate_name)
    certificate_info = certificate.cer

    response = {
        'webid': webid,
        'certificate_info': certificate_info.decode('utf-8')
    }
    return jsonify(response)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    # Forward data to gateway for validation
    gateway_url = "http://your-gateway-url/validate"
    response = requests.post(gateway_url, json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
