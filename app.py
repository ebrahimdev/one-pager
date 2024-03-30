from flask import Flask, request, send_from_directory, abort, jsonify
from flask_cors import CORS
import os
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)
CORS(app)

product = {
  "productName": "Ridge Wallet How To Use",
  "description": "Experience the ultimate in minimalist design with the Ridge Wallet. This RFID-blocking slim men's wallet is crafted from carbon fiber and aluminum, offering both durability and style. It features a mini wallet design with a money clip for ease of use and convenience, ensuring your cards and cash are secure yet easily accessible.",
  "price": "0.67C$",
  "imageResourceUrl": "https://ae01.alicdn.com/kf/Sc1935cf236594862a501d9a09071fbe1T/Carbon-Fiber-Slim-Aluminum-Men-Wallet-ID-Credit-Card-Holder-Mini-RFID-Wallet-Automatic-Pop-up.jpg",
  "storeName": "ModernCarry"
}


@app.route('/')
def home():
    return "Welcome to the URL Fetcher!"

@app.route('/fetch', methods=['POST'])
def fetch_url():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Remove all script tags
        for script in soup(["script", "style"]): # Also removing <style> tags to clean up further
            script.decompose()

        # Get the text back
        clean_html = str(soup)

        return jsonify({"html_content": clean_html})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/product', methods=['GET'])
def get_product():
    return jsonify(product)


@app.route('/image')
def get_image():
    # Get the resource_url from query parameters
    resource_url = request.args.get('resource_url')
    if not resource_url:
        abort(400, 'resource_url query parameter is required')

    # Extract the filename from the resource7_url
    filename = resource_url.split('/')[-1]

    # Ensure the filename is safe to use
    if '..' in filename or '/' in filename or '\\' in filename:
        abort(400, 'Invalid file name')

    image_directory = os.path.join(os.getcwd(), "images")
    image_path = os.path.join(image_directory, filename)

    # Create the directory if it doesn't exist
    if not os.path.exists(image_directory):
        os.makedirs(image_directory, exist_ok=True)

    # If the image doesn't exist locally, download it
    if not os.path.exists(image_path):
        try:
            response = requests.get(resource_url, stream=True)
            logging.info(f'Downloading image from {resource_url} to {image_path}')
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                abort(404)
        except requests.RequestException as e:
            logging.error(f'Failed to download image from {resource_url}: {e}')
            abort(404)
    
    logging.info(f'Serving image from {image_path}')
    return send_from_directory(image_directory, filename)


if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
