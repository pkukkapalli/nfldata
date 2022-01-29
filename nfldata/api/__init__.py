from flask import Flask, request
from http.client import BAD_REQUEST
from flask_cors import CORS

from nfldata.api.coaches import CoachesDao

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/coaches', methods=['GET'])
def all_coaches():
    coaches_dao = CoachesDao()
    query = request.args['query'] if 'query' in request.args else None

    limit = None
    if 'limit' in request.args:
        try:
            limit = int(request.args['limit'])
        except ValueError:
            return 'limit parameter must be a number', BAD_REQUEST
    
    coaches = coaches_dao.lookup_coaches(query=query, limit=limit)
    return { 'response': [dict(coach) for coach in coaches] }
