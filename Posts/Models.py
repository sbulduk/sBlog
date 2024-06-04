from Core.Database import db
import uuid
from datetime import datetime,timezone

class Post(db.Model):
    __tablename__="Posts"
    Id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    Title=db.Column(db.String(512),nullable=False)
    Body=db.Column(db.Text,nullable=False)
    DatePosted=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    NumofReads=db.Column(db.Integer,default=0,nullable=False)
    NumofComments=db.Column(db.Integer,default=0,nullable=False)
    NumofLikes=db.Column(db.Integer,default=0,nullable=False)
    NumofDislikes=db.Column(db.Integer,default=0,nullable=False)
    IsActive=db.Column(db.Boolean,default=True,nullable=False)
    UserId=db.Column(db.String(36),db.ForeignKey("Users.Id"),nullable=False)
    Comments=db.relationship("Comment",backref="Posts",lazy=True)
    Tags=db.relationship("Tag",secondary="PostsTags",backref=db.backref("Posts",lazy="dynamic"))

    def ConvertToDict(self):
        return {
            "Id":self.Id,
            "Title":self.Title,
            "Body":self.Body,
            "DatePosted":self.DatePosted,
            "NumofReads":self.NumofReads,
            "NumofComments":self.NumofComments,
            "NumofLikes":self.NumofLikes,
            "NumofDislikes":self.NumofDislikes,
            "IsActive":self.IsActive,
            "User":self.Users.Username,
            "Comments":[comment.ConvertToDict() for comment in self.Comments],
            "Tags":[tag.ConvertToDict() for tag in self.Tags]
            }

class Comment(db.Model):
    __tablename__="Comments"
    Id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    Body=db.Column(db.Text,nullable=False)
    DatePosted=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    IsActive=db.Column(db.Boolean,default=True,nullable=False)
    UserId=db.Column(db.String(36),db.ForeignKey("Users.Id"),nullable=True)
    PostId=db.Column(db.String(36),db.ForeignKey("Posts.Id"),nullable=False)
    ParentCommentId=db.Column(db.String(36),db.ForeignKey("Comments.Id"),nullable=True)
    ParentCommentReplies=db.relationship("Comment",backref=db.backref("ParentComment",remote_side=[Id]),lazy=True)

    def ConvertToDict(self):
        return {
            "Id":self.Id,
            "Body":self.Body,
            "DatePosted":self.DatePosted,
            "IsActive":self.IsActive,
            "UserId":self.UserId,
            "PostId":self.Posts.Title,
            "ParentCommentReplies":[reply.ConvertToDict() for reply in self.ParentCommentReplies]
            }

class Tag(db.Model):
    __tablename__="Tags"
    Id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    Name=db.Column(db.String(64),nullable=False)
    IsActive=db.Column(db.Boolean,default=True,nullable=False)

    def ConvertToDict(self):
        return {
            "Id":self.Id,
            "Name":self.Name,
            "IsActive":self.IsActive
            }

class PostTag(db.Model):
    __tablename__="PostsTags"
    Id=db.Column(db.String(36),primary_key=True,default=lambda:str(uuid.uuid4()))
    IsActive=db.Column(db.Boolean,default=True)
    PostId=db.Column(db.String(36),db.ForeignKey("Posts.Id",ondelete="CASCADE"))
    TagId=db.Column(db.String(36),db.ForeignKey("Tags.Id",ondelete="CASCADE"))