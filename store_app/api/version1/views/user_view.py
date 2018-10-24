from flask import request, make_response, jsonify

from flask_restful import Resource, Api
from store_app.api.version1 import bp, user_model
from store_app.api.version1.errors import error_response

user_api = Api(bp)

class UserRegister(Resource):
    def post(self):
        data = request.get_json(force =True) or {}		
        try:
            auth= False
            auth = request.headers['Authorization']

            if auth:
                data['Authorization'] = auth 
            user_db = user_model.UserModel()
            reply_info = user_db.create_user(data)

            if reply_info == "CREATED":
                pack = {"Status":reply_info}
                answ = make_response(jsonify(pack),201)
                answ.content_type='application/json;charset=utf-8'
                return answ
            else:
                pack = {"Status":reply_info}
                answ = make_response(jsonify(pack),401)
                answ.content_type='application/json;charset=utf-8'
                return answ
        except:
            reply_info = "This is a protected View!! Provide you login token!!"
            answ = make_response(jsonify(reply_info),401)
            answ.content_type='application/json;charset=utf-8'
            return answ       


user_api.add_resource(UserRegister, "/register")

class UserLogin(Resource):
    def post(self):
        data = request.get_json(force =True) or {}
        user_db = user_model.UserModel()
        reply_info = user_db.login_user(data)
        if reply_info == "Incomplete data!!" or reply_info == "Wrong Credentials!!":
            resp = {"Status": reply_info}
            answ = make_response(jsonify(resp),401)
            answ.content_type='application/json;charset=utf-8'
            return answ
        else:
            resp = {"Status":"LoggedIn","Token": reply_info}
            answ = make_response(jsonify(resp),200)
            answ.content_type='application/json;charset=utf-8'
            return answ

user_api.add_resource(UserLogin, "/login")


        