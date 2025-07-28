from flask import Flask
from config import Config
from models import db
from routes import api 
from auth_routes import API
import google.generativeai as gemini

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(api)
app.register_blueprint(API)

gemini.configure(api_key='AIzaSyBSvCe6OXLOMlz8pOwpK4R-q8YAP9piZeY')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)