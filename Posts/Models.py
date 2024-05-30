from Core.Database import db
import uuid
from datetime import datetime

class Post(db.Model):
    __tablename__="Posts"

    Id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    Title=db.Column(db.String(512),nullable=False)
    Body=db.Column(db.Text,nullable=False)
    DatePosted=db.Column(db.DateTime,default=lambda:datetime.now(datetime.utc))
    NumofReads=db.Column(db.Integer,default=0,nullable=0)
    NumofComments=db.Column(db.Integer,default=0,nullable=0)
    NumofLikes=db.Column(db.Integer,default=0,nullable=0)
    NumofDislikes=db.Column(db.Integer,default=0,nullable=0)
    IsActive=db.Column(db.Boolean,default=True,nullable=False)
    UserId=db.Column(db.String(36),db.ForeignKey("Users.Id"),nullable=False)

class Comment(db.Model):
    __tablename__="Comments"

    Id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    Body=db.Column(db.Text,nullable=False)
    DatePosted=db.Column(db.DateTime,default=lambda:datetime.now(datetime.utc))
    IsActive=db.Column(db.Boolean,default=True)
    UserId=db.Column(db.String(36),db.ForeignKey("Users.Id"),nullable=True)
    PostId=db.Column(db.String(36),db.ForeignKey("Posts.Id"),nullable=True)
    ParentCommentId=db.Column(db.String(36),db.ForeignKey("Comments.Id"),nullable=True)