from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, session, send_file, make_response)
from flask_login import current_user, login_required
from text_labeller import db
from text_labeller.view_data.forms import SelectProjectForm
from text_labeller.models import Project, Text, Class_Labels, User
import pandas as pd

view_data_blueprint = Blueprint('view_data', __name__)


@view_data_blueprint.route('/select_project_to_view', methods=['GET', 'POST'])
@login_required
def select_project_to_view():
    available_projects=db.session.query(Project).filter(Project.user_id == current_user.user_id).all()
    #get the list of tuples for SelectField
    projects_list=[(i.project_id, i.title) for i in available_projects]
    select_form=SelectProjectForm()
    #passing projects_list to the form
    select_form.project.choices = projects_list

    if select_form.validate_on_submit():
        if request.method == 'POST':
            # not working showing an id
            selected_project_name = dict(select_form.project.choices).get(select_form.project.data)
            selected_project_id =  select_form.project.data
            session['selected_project_name'] = selected_project_name
            session['selected_project_id'] = selected_project_id

            flash(f'Project Selected', 'success')
            return redirect(url_for('view_data.view_data'))

    return render_template('select_project_to_show.html', title='Select Project', form=select_form)


@view_data_blueprint.route('/view_data', methods=['GET'])
@login_required
def view_data():
    # we need to get the project id the user selected that they want to label so we cant filter to that data
    # we will use a session to do this
    selected_id_by_user = session['selected_project_id']
    selected_project_name_by_user = session['selected_project_name']
    text_to_show_query=db.session.query(Text, Class_Labels).join(Class_Labels, Text.class_label_id == Class_Labels.class_label_id).filter(Class_Labels.project_id == selected_id_by_user).statement
    text_to_show=pd.read_sql(text_to_show_query, db.session.bind)
    text_to_show = text_to_show[['text', 'class_label']]
    text_to_show.columns = ['Text', 'Label']

    return render_template('view_data.html',  tables=[text_to_show.to_html()], titles=text_to_show.columns.values, project_name=selected_project_name_by_user)

@view_data_blueprint.route('/download_data', methods=['GET'])
@login_required
def download_data():
    # we need to get the project id the user selected that they want to label so we cant filter to that data
    # we will use a session to do this
    selected_id_by_user = session['selected_project_id']
    selected_project_name_by_user = session['selected_project_name']
    text_to_show_query=db.session.query(Text, Class_Labels).join(Class_Labels, Text.class_label_id == Class_Labels.class_label_id).filter(Class_Labels.project_id == selected_id_by_user).statement
    text_to_show=pd.read_sql(text_to_show_query, db.session.bind)
    text_to_show = text_to_show[['text', 'class_label']]
    text_to_show.columns = ['Text', 'Label']

    response = make_response(text_to_show.to_csv())
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    response.headers["Content-Type"] = "text/csv"
    return response