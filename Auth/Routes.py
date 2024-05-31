from flask import Blueprint,request,jsonify
from Auth.Services import Services
from flask_jwt_extended import jwt_required,get_jwt_identity

AuthBp=Blueprint("Auth",__name__,url_prefix="/user")
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

AuthBp.route("/users",method=["GET"])
@jwt_required()
def GetUsers():
    userList=userServices.GetAllUsers()
    return jsonify({"success":True,"data":userList}),200

AuthBp.route("/userdetails/<userId:string>")
@jwt_required()
def GetUser(id:str):
    userId=get_jwt_identity()
    if(id==userId):
        user=userServices.GetUserById(id)
        return jsonify({"success":True,"data":user})
    return jsonify({"success":False,"message":"You are not authorized for this"})

AuthBp.route("/addrole",method=["POST"])
@jwt_required()
def AddRole():
    
    pass