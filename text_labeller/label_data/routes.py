from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, session)
from flask_login import current_user, login_required
from text_labeller import db
from text_labeller.label_data.forms import SelectProjectForm, LabelDataForm
from text_labeller.models import Project, Text, Class_Labels, User

label_data = Blueprint('label_data', __name__)


@label_data.route('/select_project', methods=['GET', 'POST'])
@login_required
def select_project():
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
            session['selected_project_id'] = selected_project_id

            flash('Project Selected', 'success')
            return redirect(url_for('label_data.label_data_class'))

    return render_template('select_project.html', title='Select Project', form=select_form)


@label_data.route('/label_data', methods=['GET', 'POST'])
@login_required
def label_data_class():
    # we need to get the project id the user selected that they want to label so we cant filter to that data
    # we will use a session to do this
    selected_id_by_user = session['selected_project_id']
    available_labels=db.session.query(Class_Labels).filter(Class_Labels.project_id == selected_id_by_user).all()
    text_to_label_query=db.session.query(Text).filter(Text.class_label_id == None, Text.project_id == selected_id_by_user).first()


    if text_to_label_query != None:
        text_to_label=text_to_label_query.text
        id_of_text=db.session.query(Text).filter(Text.class_label_id == None, Text.project_id == selected_id_by_user).first().text_id

        labels_list=[(i.class_label_id, i.class_label) for i in available_labels] 
        label_data_form=LabelDataForm()
        #passing projects_list to the form
        label_data_form.class_label.choices = labels_list
        text_row = Text.query.get(id_of_text)

        if label_data_form.validate_on_submit():
            if request.method == 'POST':

                text_row.class_label_id = label_data_form.class_label.data
                db.session.commit()

                flash('Data Labelled', 'success')
                return redirect(url_for('label_data.label_data_class'))

    else:
        return render_template('no_data.html')

    return render_template('label_data.html', title='Label Data', form=label_data_form, text_to_label=text_to_label)





