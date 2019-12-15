from flask import Flask, request
from flask_restful import Resource, Api
import json
import os
from src.update_data.user import update_list_users
from src.provide_data.user import get_user

app = Flask(__name__)
api = Api(app)

class User(Resource):
  """
    Update database with finished game data
  """
  def post(self):
    try:
      users = request.get_json()["users"]
    except:
      return {"error": "users not provided"}, 400
    
    try:
      winner = request.get_json()["winner"]
    except:
      return {"error": "winner not provided"}, 400

    success = update_list_users(users, winner)
    
    if success:
      return {"success": "user updated successfully"}, 201
    else:
      return {"error": "can't update user"}, 500
  
  def get(self):
    try:
      userId = request.args.get('userId')
    except:
      return {"error": "'userId' not provided"}, 400
    
    played, won, lost = get_user(userId)
    return {"played": played, "won": won, "lost": lost}, 200

api.add_resource(User, '/user')

def make_migration():
  if not os.path.exists("/app/migrations"):
    os.system('sh -c "python manage.py db init"')
  
  success = False
  while not success:
    response = os.system('sh -c "python manage.py db migrate && python manage.py db upgrade"')
    success = True if response == 0 else False
    if success: break

if __name__ == "__main__":
    make_migration()
    app.run(debug=True, host= '0.0.0.0', port=6000)