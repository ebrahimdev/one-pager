from flask import render_template
from . import bp

@bp.route('/')
def home():
    return "Welcome to the Flask"
