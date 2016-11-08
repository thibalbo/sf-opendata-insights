from flask import Flask
import yaml
app = Flask(__name__)

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

from app import views
