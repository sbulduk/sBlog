from Core.Database import db
from Core.Utils import HashPassword
from Auth.Models import User,Role
from flask_jwt_extended import create_access_token
import datetime

class Services(object):
    def CreateUser(self,name,surname,username,email,password):
        hashedPassword=HashPassword(password)
        newUser=User(Name=name,Surname=surname,Username=username,Email=email,Password=hashedPassword)
        db.session.add(newUser)
        db.session.commit()
    
    def AuthenticateUser(self,username,password):
        user=User.query.filter_by(Username=username).first()
        if(user and user.Password==HashPassword(password) and user.IsActive):
            expires=datetime.timedelta(hours=1)
            return create_access_token(identity=user.Id,expires_delta=expires)
        return None