from . import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from .models import User, Workspace, Link
from .forms import LoginForm, RegistrationForm, NewWorkspaceForm, NewLinkForm


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    workspaces = Workspace.query.filter_by(user_id=current_user.id)
    workspace_names = [workspace.name for workspace in workspaces]
    links_urls = [workspace.links for workspace in workspaces]
    ws_form = NewWorkspaceForm()
    link_form = NewLinkForm()
    link_form.workspace.choices = workspace_names
    if ws_form.validate_on_submit():
        workspace = Workspace(name=ws_form.name.data, user_id=current_user.id)
        db.session.add(workspace)
        db.session.commit()
        flash('Workspace created successfully!')
        return redirect(url_for('index'))

    if ws_form.validate_on_submit():
        link = Link(name=link_form.name.data, url=link_form.url.data, workspace_id=link_form.workspace.data)
        db.session.add(link)
        db.session.commit()
        flash('Link added successfully!')
        return redirect(url_for('index'))

    return render_template('index.html', title='Index', workspaces=workspaces, ws_form=ws_form, link_form=link_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)