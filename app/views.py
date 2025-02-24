import jwt,json
from datetime import datetime, timedelta
from flask import request,jsonify

from app import app
from app.db.config import db
from app.utils import token_required
from bson.objectid import ObjectId
from bson import json_util
@app.post('/register')
def register():
    db['users'].insert_one(request.get_json())
    return {"status": "success", "message":"User registered successfully"}

@app.post('/login')
def login():
    credentials=request.get_json()
    if all([credentials.get('email'),credentials.get('password')]):
        user = db['users'].find_one(request.get_json())
        token = jwt.encode({
            'user_id': str(user.get('_id')),
            'exp' : datetime.now() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
        if user:
            return jsonify({"status": "success", "message":"User logged in successfully", "token": token}) ,200
    return jsonify({"status": "error", "message":"Invalid credentials"}),403

@app.post('/template')
@token_required
def create_template(current_user):
    body=request.get_json()
    db['templates'].insert_one({
        'user_id': current_user.get('_id'),
        'template_name': body.get('template_name'),
        "subject": body.get('subject'),
        "body": body.get('body')
    })
    return jsonify({"status": "success", "message":"Template Created"}),200

@app.route('/template/<string:template_id>',methods=['GET','PUT','DELETE'])
@token_required
def get_templates(current_user,template_id):
    if request.method =='GET':
        template = db['templates'].find_one({
                "user_id": ObjectId(current_user.get('_id')),
                "_id":ObjectId(template_id)
            })
        if not template:
            return jsonify({"message":"Template not found"}),400
        bson_dump = json_util.dumps(template)
        return jsonify({"template":json.loads(bson_dump)}),200
    if request.method == 'PUT':
        try:
            body=request.get_json()
            db['templates'].update_one({"user_id": ObjectId(current_user.get('_id')),"_id":ObjectId(template_id)}, 
                                    {"$set": {
                                        "template_name": body.get('template_name'),
                                        "subject": body.get('subject'),
                                        "body": body.get('body')}})
            return jsonify({
                "status": "success", 
                "message":"Template updated"}),200
        except Exception as e:
            return jsonify({"status": "error", 
                    "message":"Something went wrong"}),500
    if request.method == 'DELETE':
        try:
            db['templates'].delete_one({"user_id": ObjectId(current_user.get('_id')),"_id":ObjectId(template_id)})
            return jsonify({"status": "success", 
                    "message":"Template deleted"}),200
        except Exception as e:
            return jsonify({"status": "error", 
                    "message":"Something went wrong"}),500