from flask import Flask, render_template, url_for, request, g
from app_blueprint import app_blueprint
from config import Config
from dotenv import load_dotenv

# Load environment variables from store.env file
load_dotenv(dotenv_path='store.env')

app = Flask(__name__)  # app itself
app.config.from_object(Config)  # access environment variables

# Register the blueprint
app.register_blueprint(app_blueprint)

# Register teardown function
@app.teardown_appcontext
def teardown_db(exception):
    # Get database connection within g and close (if it exists)
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)