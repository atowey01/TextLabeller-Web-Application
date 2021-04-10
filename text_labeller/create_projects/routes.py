from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from text_labeller import db
from text_labeller.create_projects.forms import PrepareDataForm
from io import TextIOWrapper
import csv
from text_labeller.models import Project, Text, Class_Labels
from werkzeug.utils import secure_filename
import os
import pandas as pd

create_projects = Blueprint('create_projects', __name__)


@create_projects.route("/prepare_data", methods=['GET', 'POST'])
@login_required
def create_project():
    form = PrepareDataForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            project = Project(title=form.title.data, user_id=current_user.user_id)
            db.session.add(project)
            db.session.commit()
    
            form_text_data = form.content.data
            uploaded_filename= secure_filename(form_text_data.filename)
            form_text_data.save(uploaded_filename)
            df = pd.read_csv(uploaded_filename)

            for index, row in df.iterrows():
                text = Text(text = row[0], project_id = project.project_id)
                db.session.add(text)
                db.session.commit()

            class_labels = form.class_labels.data.split(',')
            for label in class_labels:
                label = label.strip()
                class_label = Class_Labels(class_label = label, project_id = project.project_id)
                db.session.add(class_label)
                db.session.commit()

            flash('Your project has been created, you can now start labelling!', 'success')
            return redirect(url_for('label_data.select_project'))
            
    return render_template('create_project.html', title='Create Project', form=form)