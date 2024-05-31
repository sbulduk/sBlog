from Core.Database import db
import uuid

class User(db.Model):
    __tablename__="Users"

    Id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    Username=db.Column(db.String(64),unique=True,nullable=False)
    Email=db.Column(db.String(128),unique=True,nullable=False)
    Password=db.Column(db.String(64),nullable=False)
    Name=db.Column(db.String(32),nullable=False)
    Surname=db.Column(db.String(32),nullable=False)
    IsActive=db.Column(db.Boolean,default=True,nullable=False)
    ResetToken=db.Column(db.Text,nullable=True)
    Roles=db.relationship("Role",secondary="UsersRoles",backref=db.backref("Users",lazy="dynamic"))

class Role(db.Model):
    __tablename__="Roles"

    Id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    Name=db.Column(db.String(64),unique=True)
    Description=db.Column(db.String(1024),unique=True)
    IsActive=db.Column(db.Boolean,default=True)
    # Users=db.relationship("User",secondary="UsersRoles",backref=db.backref("Roles",lazy="dynamic"))

class UserRole(db.Model):
    __tablename__="UsersRoles"

    Id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    IsActive=db.Column(db.Boolean,default=True)
    UserId=db.Column(db.String(36),db.ForeignKey("Users.Id",ondelete="CASCADE"))
    RoleId=db.Column(db.String(36),db.ForeignKey("Roles.Id",ondelete="CASCADE"))