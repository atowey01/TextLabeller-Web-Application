from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from text_labeller import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}')"

    def get_id(self):
        return (self.user_id)

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f"Project('{self.title}')"


class Class_Labels(db.Model):
    class_label_id = db.Column(db.Integer, primary_key=True)
    class_label = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)

    def __repr__(self):
        return f"Class Label('{self.class_label}')"

class Text(db.Model):
    text_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    class_label_id = db.Column(db.Integer, db.ForeignKey('class__labels.class_label_id'), nullable=True)

    def __repr__(self):
        return f"Text('{self.text_id}', '{self.text}', '{self.class_label_id}')"
