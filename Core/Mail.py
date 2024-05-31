from flask_mail import Mail

mail=Mail()

def InitMail(app):
    mail.init_app(app)