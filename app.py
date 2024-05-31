import os
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
from flask import  Flask
from Core.Config import Config
from Core.Database import InitDB
from Core.Mail import InitMail
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from Auth.Routes import AuthBp
from Posts.Routes import PostsBp
from Rem.Routes import RemBp

def CreateApp():
    app=Flask(__name__)
    app.config.from_object(Config)
    InitDB(app)
    InitMail(app)
    JWTManager(app)
    CORS(app)

    app.register_blueprint(AuthBp)
    app.register_blueprint(PostsBp)
    app.register_blueprint(RemBp)
    return app

if(__name__=="__main__"):
    app=CreateApp()
    app.run()