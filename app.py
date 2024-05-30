import os
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
from flask import  Flask
from Core.Config import Config
from Core.Database import InitDB
from flask_jwt_extended import JWTManager
from Auth.Routes import AuthBp
from Posts.Routes import PostsBp

def CreateApp():
    app=Flask(__name__)
    app.config.from_object(Config)
    InitDB(app)
    JWTManager(app)

    app.register_blueprint(AuthBp)
    app.register_blueprint(PostsBp)
    return app

if(__name__=="__main__"):
    app=CreateApp()
    app.run()