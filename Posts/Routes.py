from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity,verify_jwt_in_request
from Posts.Services import Services

PostsBp=Blueprint("Posts",__name__,url_prefix="/post")
postServices=Services()

@PostsBp.route("/postlist",methods=["GET"])
def ListPosts():
        return postServices.GetPosts(),200

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
    return jsonify({"success":True,"msg":f"Posted: {data['Title']}"}),201

@PostsBp.route("/<string:postId>/comments/newcomment",methods=["POST"])
def AddComment(postId):
    data=request.get_json()
    userId="g_guest_-_gue-_st_-0gst-g_0_guest_0_"
    try:
        verify_jwt_in_request(optional=True)
        userId=get_jwt_identity()
    except:
        pass
    postServices.CreateComment(data["Body"],postId,userId,data.get("ParentCommentId"))
    return jsonify({"success":True,"msg":f"Comment added successfully. Post Id: {postId}"}),201