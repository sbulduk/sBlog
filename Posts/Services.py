from Core.Database import db
from Posts.Models import Post,Comment,Tag

class Services(object):
    def GetPosts(self):
        return Post.query.filter_by(IsActive=True).all()
    
    def GetPostById(self,postId):
        return Post.query.filter_by(PostId=postId,IsActive=True).first()

    def CreatePost(self,title,body,userId):
        newPost=Post(Title=title,Body=body,UserId=userId)
        db.session.add(newPost)
        db.session.commit()

    def UpdatePost(self,postId,**kwargs):
        post=self.GetPostById(postId)
        for key,value in kwargs.items():
            setattr(post,key,value)
        db.session.commit()

    def ActivatePost(self,postId):
        post=self.GetPostById(postId)
        post.IsActive=True
        db.session.commit()

    def DeactivatePost(self,postId):
        post=self.GetPostById(postId)
        post.IsActive=False
        db.session.commit()

    def GetCommentsByPostId(self,postId):
        return Comment.query.filter_by(PostId=postId,IsActive=True).all()

    def GetCommentsByParentCommentId(self,parentCommentId):
        return Comment.query.filter_by(ParentCommentId=parentCommentId,IsActive=True).all()

    def CreateComment(self,body,postId,userId=None,parentCommentId=None):
        newComment=Comment(Body=body,PostId=postId,UserId=userId,ParentCommentId=parentCommentId)
        db.session.add(newComment)
        db.session.commit()

    def GetPostwithComments(self,postId):
        post=self.GetPostById(postId)
        if post:
            comments=self.GetCommentsByPostId(postId)
            return{"post":post,"comments":comments}
        return None

    def GetTags(self):
        return Tag.query.filter_by(IsActive=True).all()

    def CreateTag(self,name):
        newTag=Tag(Name=name)
        db.session.add(newTag)
        db.session.commit()