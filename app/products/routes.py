from flask import Blueprint, jsonify, abort, request, send_from_directory
from app.utils.fetch import fetch_and_clean_html
from app.utils.image_utils import save_image_from_url
from app.services.product_service import add_product as add_product_service
from app.models import Product
from . import bp
import os

@bp.route('/<int:product_id>')
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.productName,
            'description': product.description,
            'price': product.price,
            'imageResourceUrl': product.imageResourceUrl,
            'storeName': product.storeName,
            'status': product.status
        })
    else:
        return jsonify({'error': 'Product not found'}), 404


@bp.route('/fetch', methods=['POST'])
def fetch_url():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        clean_html = fetch_and_clean_html(url)
        return jsonify({"html_content": clean_html})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@bp.route('/image')
def get_image():
    resource_url = request.args.get('resource_url')
    if not resource_url:
        abort(400, 'resource_url query parameter is required')

    try:
        image_path = save_image_from_url(resource_url)
        return send_from_directory(os.path.dirname(image_path), os.path.basename(image_path))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/add-product', methods=['POST'])
def add_product():
    print("*********we at least got here*********")
    data = request.get_json()
    if not data or not data.get('productName') or not data.get('price'):
        return jsonify({'error': 'Missing required fields: productName and price'}), 400

    name = data.get('productName')
    description = data.get('description', '')
    price = data.get('price')
    imageResourceUrl = data.get('imageResourceUrl', '')
    storeName = data.get('storeName', '')
    status = data.get('status', 'fetched') 
    product = add_product_service(name, description, price, imageResourceUrl, storeName, status)

    if product:
        return jsonify({'message': 'Product added successfully', 'product': {
            'id': product.id,
            'productName': product.productName,
            'description': product.description,
            'price': product.price,
            'imageResourceUrl': product.imageResourceUrl,
            'storeName': product.storeName,
            'status': product.status
        }}), 201
    else:
        return jsonify({'error': 'Failed to add product'}), 500