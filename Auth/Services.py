from Core.Database import db
from Core.Utils import HashPassword
from Auth.Models import User,Role,UserRole
from flask_jwt_extended import create_access_token
import datetime

class Services(object):
    def GetAllUsers(self):  #------------------
        return User.query.filter_by(IsActive=True).all()

    def GetUserById(self,userId:str)->User:
        return User.query.filter_by(Id=userId,IsActive=True).first()
    
    def GetUserByEmail(self,email:str)->User:
        return User.query.filter_by(Email=email,IsActive=True).first()

    def CreateUser(self,name:str,surname:str,username:str,email:str,password:str)->None:
        hashedPassword=HashPassword(password)
        newUser=User(Name=name,Surname=surname,Username=username,Email=email,Password=hashedPassword)
        db.session.add(newUser)
        db.session.commit()

    def AuthenticateUser(self,username:str,password:str):   #------------------
        user=User.query.filter_by(Username=username).first()
        if(user and user.Password==HashPassword(password) and user.IsActive):
            expires=datetime.timedelta(hours=1)
            return create_access_token(identity=user.Id,expires_delta=expires)
        return None

    def UpdateUser(self,userId:str,**kwargs):   #------------------
        user=self.GetUserById(userId)
        for key,value in kwargs.items():
            if(key=="Password"):
                value=HashPassword(value)
            setattr(user,key,value)
        db.session.commit()

    def ActivateUser(self,userId:str)->None:
        user=self.GetUserById(userId)
        user.IsActive=True
        db.session.commit()

    def DeactivateUser(self,userId:str)->None:
        user=self.GetUserById(userId)
        user.IsActive=False
        db.session.commit()

    def GetRoleById(self,roleId:str)->Role:
        return Role.query.filter_by(Id=roleId,IsActive=True).first()

    def GetRoleByRoleName(self,roleName:str)->Role:
        return Role.query.filter_by(Name=roleName,IsActive=True).first()

    def CreateRole(self,roleName:str,description:str="")->None:
        newRole=Role(Name=roleName,Description=description)
        db.session.add(newRole)
        db.session.commit()

    def UpdateRole(self,roleId:str,**kwargs)->None: #------------------
        role=self.GetRoleById(roleId)
        for key,value in kwargs.items():
            setattr(role,key,value)
        db.session.commit()

    def ActivateRole(self,roleId:str)->None:
        role=self.GetRoleById(roleId)
        role.IsActive=True
        db.session.commit()

    def DeactivateRole(self,roleId:str)->None:
        role=self.GetRoleById(roleId)
        role.IsActive=False
        userRoles=UserRole.query.filter_by(RoleId=roleId).all()
        for userRole in userRoles:
            userRole.IsActive=False
        db.session.commit()

    def GetUserRoles(self,userId:str):  #------------------
        user=self.GetUserById(userId)
        if(user):
            return [Role.Name for role in user.Roles]
        return []
    
    def GetUserswithRole(self,roleName:str):    #------------------
        role=self.GetRoleByName(roleName)
        if(role):
            return [User.Username for user in role.Users]
        return []
    
    def UserHasRole(self,userId:str,roleName:str):  #------------------
        user=self.GetUserById(userId)
        if(user):
            return any(Role.Name==roleName for role in user.Roles)
        return []