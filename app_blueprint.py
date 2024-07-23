from flask import Blueprint, render_template, url_for, request, current_app, jsonify, g
from config import Config
from summon_function import SimulateSummon  # custom summon function
import os
import pymysql.cursors

app_blueprint = Blueprint('app_blueprint', __name__)
MULTI_SUMMON_AMOUNT = 10  # const variable set for multi-summon amount

# Page Formats
@app_blueprint.route('/')  # Home Page
def index():
    return render_template("index.html")

@app_blueprint.route('/summons')  # Summons Page
def summons():
    # Format page based on image/text selected
    choice = request.args.get('choice')

    if choice == 'opt2':
        return render_template("summons.html", choice='opt2')
    else:  # Set option 1 to be default
        return render_template("summons.html", choice='opt1')

# Database Connections Management
def get_db():
    # Establish new database connection within g object
    if 'db' not in g:
        g.db = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor 
        )
    return g.db

# Summon Functionality
@app_blueprint.route('/summon', methods=['POST'])
def summon():
    # Get table name for specific summom
    data = request.json  # gets data from POST data sent in Jscript
    tableName = data.get('tableName')
    if not tableName:
        return jsonify({'error':'Table name is required'})
    else:

        # Identify number of characters to summon
        multi_summon = data.get('multiSummon', False)  # default to false when not found
        summonAmount = 1  # default set to single summon
        if multi_summon:
            summonAmount = MULTI_SUMMON_AMOUNT 

        # Get database connection & generate characters
        db = get_db()  
        characters = []  # initialise empty list
        for i in range (summonAmount):
            character = SimulateSummon(db, tableName)
            characters.append(character)

        return jsonify ({'characters' : characters})  # convert to JSON response and send back