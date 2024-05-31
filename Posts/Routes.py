from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from Posts.Services import Services

PostsBp=Blueprint("Posts",__name__,url_prefix="/posts")
postServices=Services()

@PostsBp.route("",methods=["GET"])
def ListPosts():
    postList=postServices.GetPosts()
    return jsonify([post.to_dict() for post in postList]),200

@PostsBp.route("/<postId>",methods=["POST"])
def GetPostById(postId):
    postData=postServices.GetPostwithComments(postId)
    if postData:
        return jsonify({"success":True,"data":postData}),200
    return jsonify({"success":False,"data":"No posts found"}),404

    # selectedPost=postServices.GetPostById(postId)
    # postwithComments={"Post":selectedPost}
    # commentList=postServices.GetCommentsByPostId(postId)
    # if(commentList):
    #     for comment in commentList:
    #         commentData={"Comment":comment}
    #         subCommentList=postServices.GetCommentsByCommentId(comment.commentId)
    #         if(subCommentList):
    #             commentData["Subcomment"]=subCommentList
    # postwithComments["Comments"]=commentData
    # return postwithComments


@PostsBp.route("/newpost",methods=["POST"])
@jwt_required()
def AddPost():
    data=request.get_json()
    userId=get_jwt_identity()
    postServices.CreatePost(data["Title"],data["Body"],userId)
    return jsonify({"success":True,"message":f"Posted: {data['Title']}"}),201

@PostsBp.route("/<postId>/comments/newcomment",methods=["POST"])
def AddComment(postId):
    data=request.get_json()
    userId=None
    if("Authorization" in request.headers):
        userId=get_jwt_identity()
    postServices.CreateComment(data["Body"],postId,userId,data.get("ParentCommentId"))
    return jsonify({"success":True,"message":f"Comment added successfully. Post Id: {postId}"}),201