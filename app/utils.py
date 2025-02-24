import jwt
from bson.objectid import ObjectId
from functools import wraps
from flask import request, jsonify
from app import app
from app.db.config import db
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('bearer')
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            current_user = db['users'].find_one({"_id" :ObjectId(data['user_id'])})
            if not current_user:
                return jsonify({'message' : 'User does not exist !!'}), 404

        except Exception as e:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        return  f(current_user, *args, **kwargs)
    return decorated