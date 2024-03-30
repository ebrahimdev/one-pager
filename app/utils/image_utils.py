# app/utils/image_utils.py
import os
import requests
from flask import current_app, abort
import logging

def save_image_from_url(resource_url):
    """
    Fetches an image from the given URL and saves it locally if it doesn't already exist.
    Returns the path to the local image.
    """
    filename = resource_url.split('/')[-1]

    if '..' in filename or '/' in filename or '\\' in filename:
        abort(400, 'Invalid file name')

    image_directory = os.path.join(current_app.root_path, "static", "images")
    if not os.path.exists(image_directory):
        os.makedirs(image_directory, exist_ok=True)

    image_path = os.path.join(image_directory, filename)
    if not os.path.exists(image_path):
        try:
            response = requests.get(resource_url, stream=True)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                abort(404)
        except requests.RequestException:
            abort(404)
    
    return image_path
