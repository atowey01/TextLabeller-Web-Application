from text_labeller.models import User, Project, Class_Labels, Text


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password are defined correctly
    """
    user = User(email='test@gmail.com', password='password')
    assert user.email == 'test@gmail.com'
    assert user.password == 'password'

def test_new_project():
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check the title is defined correctly
    """
    project = Project(title='New Project')
    assert project.title == 'New Project'

def test_new_text():
    """
    GIVEN a Text model
    WHEN a new Text object is created
    THEN check the text is defined correctly
    """
    text = Text(text = "I am happy")
    assert text.text == "I am happy"

