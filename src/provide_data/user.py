from src.db.db import db
from pandas import DataFrame

cursor = db.cursor()

def get_user(userId):
    cursor.execute('SELECT * FROM user where userId = %s', (userId,))
    df = DataFrame(cursor.fetchall())
    try:
        df.columns = ["userId", "played", "won", "lost"]

        played, num_won, num_lost = (df["played"][0] if df["played"][0] is not None else 0, df["won"][0] if df["won"][0] is not None else 0, df["lost"][0] if df["lost"][0] is not None else 0)
    except:
        played, num_won, num_lost = (0, 0, 0)
    
    return int(played), int(num_won), int(num_lost)
