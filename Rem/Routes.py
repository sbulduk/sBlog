from flask import Blueprint,request,jsonify
from Auth.Models import User
from Auth.Services import Services as UserServices
from Rem.Services import Services as RemServices
from Core.Database import db
import uuid

RemBp=Blueprint("RemBp",__name__,url_prefix="/mail")

userServices=UserServices()
remServices=RemServices()

@RemBp.route("/forgotpassword",methods=["POST"])
def ForgotPassword():
    data=request.get_json()
    email=data.get("email")
    user=userServices.GetUserByEmail(email)
    if(user):
        resetToken=str(uuid.uuid4())
        userServices.UpdateUser(user.Id,ResetToken=resetToken)
        remServices.SendResetEmail(email,resetToken)
        return jsonify({"success":True,"message":f"Reset token sent to your email: {email}"}),200
    return jsonify({"success":False,"message":f"E-mail not found"}),404

@RemBp.route("/resetpassword",methods=["POST"])
def ResetPassword():
    data=request.get_json()
    token=data.get("token")
    newPassword=data.get("newPassword")
    user=remServices.VerifyResetToken(token)
    if(user):
        userServices.UpdateUser(user.Id,Password=newPassword,ResetToken=None)
        # userServices.UpdateUser(user.Id,ResetToken=None)
        return jsonify({"success":True,"message":f"Reset token sent to your email"}),200
    return jsonify({"success":False,"message":f"Invalid or expired password"}),400