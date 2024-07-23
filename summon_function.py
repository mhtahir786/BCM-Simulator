import pymysql
import random

def SimulateSummon(db, tableName):

    try:
        # Get all characters and probabiities
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {tableName}")  #f used so tableName value can be accessed
        characters = cursor.fetchall()

        # Find total probability (not exactly 100 but 99.9 recurring)
        totalProbability = 0
        for record in characters:
            totalProbability += record['probability']
        
        # Generate a random float within range of probabilities, uniform ensures a float (boundaries inclusive)
        randomNum = random.uniform(0, totalProbability)

        # Find character after the cumulative probability
        cumulativeProbability = 0
        for character in characters:
            cumulativeProbability += character['probability']
            if randomNum <= cumulativeProbability:
                return character  # returns next character after probability (may not be the closest one, but is quicker)
    
    # Print any errors caught
    except Exception as e:
        print(f"Error : {e}")

    finally:
        # Close and return character
        cursor.close()
    
    return None  # Fail scenario when no character is generated