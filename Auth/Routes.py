from flask import Blueprint,request,jsonify
from Auth.Services import Services
from flask_jwt_extended import jwt_required,get_jwt_identity,unset_jwt_cookies

AuthBp=Blueprint("Auth",__name__,url_prefix="/user")
userServices=Services()

@AuthBp.route("/register",methods=["POST"])
def Register():
    data=request.get_json()
    userServices.CreateUser(data["Name"],data["Surname"],data["Username"],data["Email"],data["Password"])
    return jsonify({"success":True,"msg":f"User created successfully."}),201

@AuthBp.route("/login",methods=["POST"])
def Login():
    data=request.get_json()
    token=userServices.AuthenticateUser(data["Username"],data["Password"])
    if(token):
        return jsonify({"success":True,"token":token}),200
    return jsonify({"success":False,"msg":"Invalid credentials"}),401

@AuthBp.route("/logout",methods=["POST"])
@jwt_required()
def Logout():
    response=jsonify({"success":True,"msg":f"Logged out successfully"})
    unset_jwt_cookies(response)
    return response,200

@AuthBp.route("/users",methods=["GET"])
@jwt_required()
def GetUsers():
    userList=userServices.GetAllUsers()
    # userData=[user.ConvertToDict() for user in userList]
    return jsonify({"success":True,"data":userList}),200

@AuthBp.route("/userdetails/<string:id>",methods=["POST"])
@jwt_required()
def GetUser(id:str):
    userId=get_jwt_identity()
    if(str(id)==str(userId)):
        user=userServices.GetUserById(id)
        return jsonify({"success":True,"data":user}),200
    return jsonify({"success":False,"msg":"You are not authorized for this page"}),404

@AuthBp.route("/addrole",methods=["POST"])
@jwt_required()
def AddRole():
    a="0"
    pass