from . import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from .models import user, workspace, link
from .forms.user import LoginForm, RegistrationForm
from .forms.link import NewLinkForm
from .forms.workspace import NewWorkspaceForm, DeleteWorkspaceForm


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    workspaces = workspace.get_all_workspaces(current_user)
    links_urls = [workspace.links for workspace in workspaces]
    ws_form = NewWorkspaceForm()
    link_form = NewLinkForm()
    del_ws_form = DeleteWorkspaceForm()
    workspace_names = [workspace.name for workspace in workspaces]
    if request.method == 'POST':
        if ws_form.ws_name.data and ws_form.validate():
            workspace.create_workspace(name=ws_form.ws_name.data, user=current_user)
            flash('Workspace created successfully!')
            return redirect(url_for('index'))

        elif link_form.validate():
            link.create_link(workspace_name=link_form.workspace.data, user=current_user, link_url=link_form.url.data, link_name=link_form.name.data)
            flash('Link added successfully!')
            return redirect(url_for('index'))

        elif request.form.get("delete_ws"):
            workspace.delete_workspace(name=request.form['delete_ws'],user=current_user)
            flash('Workspace deleted successfully!')
            return redirect(url_for('index'))

        elif request.form.get("delete_link"):
            def get_linkname_and_workspacename_from_form(form_value):
                form_values = form_value.split('::')
                return form_values[0], form_values[1]
            link_name, workspace_name = get_linkname_and_workspacename_from_form(request.form['delete_link'])
            link.delete_link(link_name=link_name, parent_workspace_name=workspace_name, user=current_user)
            flash('Link deleted successfully!')
            return redirect(url_for('index'))

    return render_template('index.html', title='Index', workspaces=workspaces, ws_form=ws_form, link_form=link_form, del_ws_form=del_ws_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_obj = user.User.query.filter_by(username=form.username.data).first()
        if user_obj is None or not user_obj.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user_obj, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_obj = user.User(username=form.username.data, email=form.email.data)
        user_obj.set_password(form.password.data)
        db.session.add(user_obj)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/workspace/<workspace_name>/detail', methods=['GET', 'POST'])
def workspace_detail(workspace_name):
    workspaces = workspace.get_all_workspaces(current_user)
    links_urls = [workspace.links for workspace in workspaces]
    ws_form = NewWorkspaceForm()
    link_form = NewLinkForm()
    del_ws_form = DeleteWorkspaceForm()
    workspace_names = [workspace.name for workspace in workspaces]

    detailed_workspace = [workspace for workspace in workspaces if workspace.name == workspace_name][0]
    if request.method == 'POST':
        if ws_form.ws_name.data and ws_form.validate():
            workspace.create_workspace(name=ws_form.ws_name.data, user=current_user)
            flash('Workspace created successfully!')
            return redirect(url_for('index'))

        elif link_form.validate():
            link.create_link(workspace_name=detailed_workspace.name, user=current_user, link_url=link_form.url.data, link_name=link_form.name.data)
            flash('Link added successfully!')
            return redirect(url_for('index'))

        elif request.form.get("delete_ws"):
            workspace.delete_workspace(name=request.form['delete_ws'],user=current_user)
            flash('Workspace deleted successfully!')
            return redirect(url_for('index'))

        elif request.form.get("delete_link"):
            def get_linkname_and_workspacename_from_form(form_value):
                form_values = form_value.split('::')
                return form_values[0], form_values[1]
            link_name, workspace_name = get_linkname_and_workspacename_from_form(request.form['delete_link'])
            link.delete_link(link_name=link_name, parent_workspace_name=workspace_name, user=current_user)
            flash('Link deleted successfully!')
            return redirect(url_for('index'))

    return render_template('ws_detail.html', workspaces=workspaces, ws_form=ws_form, link_form=link_form, del_ws_form=del_ws_form, detailed_workspace=detailed_workspace)