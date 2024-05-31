from Core.Config import Config
from Auth.Models import User
from Auth.Services import Services as UserServices
from Core.Database import db
from Core.Mail import mail
from flask_mail import Message

class Services(object):
    def __init__(self):
        self.userServices=UserServices()
    
    def SendResetEmail(self,email:str,token:str)->None:
        msg=Message("Password reset request",sender=Config.MAIL_DEFAULT_SENDER,recipients=[email])
        msg.body=f"""
            To reset your password, visit the following link: {Config.ROOT_LINK}/mail/resetpassword?token={token}\n
            Your token is: {token}\n
            You can simply ignore this mail if you did not make this request.
            """
        mail.send(msg)

    def VerifyResetToken(self,token:str)->User:
        return User.query.filter_by(ResetToken=token).first()