from Core.Database import db
from Posts.Models import Post,Comment

class Services(object):
    def GetPosts(self):
        return Post.query.filter_by(IsActive=True).all()
    
    def GetPostById(self,postId):
        return Post.query.filter_by(PostId=postId,IsActive=True).first()

    def CreatePost(self,title,body,userId):
        newPost=Post(Title=title,Body=body,UserId=userId)
        db.session.add(newPost)
        db.session.commit()

    def GetCommentsByPostId(self,postId):
        return Comment.query.filter_by(PostId=postId,IsActive=True).all()

    def GetCommentsByParentCommentId(self,parentCommentId):
        return Comment.query.filter_by(ParentCommentId=parentCommentId,IsActive=True).all()

    def CreateComment(self,body,postId,userId=None,parentCommentId=None):
        newComment=Comment(Body=body,PostId=postId,UserId=userId,ParentCommentId=parentCommentId)
        db.session.add(newComment)
        db.session.commit()