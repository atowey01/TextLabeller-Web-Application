from text_labeller import create_app, db
from text_labeller.models import User, Project, Text, Class_Labels

app = create_app()
app.app_context().push()
db.create_all()


if __name__ == '__main__':
    app.run()
