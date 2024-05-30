from flask import Blueprint,request,jsonify
from Auth.Services import Services
from flask_jwt_extended import jwt_required

AuthBp=Blueprint("Auth",__name__,url_prefix="/auth")
userServices=Services()

@AuthBp.route("/register",methods=["POST"])
def Register():
    data=request.get_json()
    userServices.CreateUser(data["Name"],data["Surname"],data["Username"],data["Email"],data["Password"])
    return jsonify({"success":True,"message":f"User created successfully."}),201

@AuthBp.route("/login",methods=["POST"])
def Login():
    data=request.get_json()
    token=userServices.AuthenticateUser(data["Username"],data["Password"])
    if(token):
        return jsonify({"success":True,"token":token}),200
    return jsonify({"success":False,"message":"Invalid credentials"}),401