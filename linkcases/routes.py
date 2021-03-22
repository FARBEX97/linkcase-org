from . import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from .models import user, linkcase, link
from .forms.user import LoginForm, RegistrationForm
from .forms.link import NewLinkForm
from .forms.linkcase import NewLinkcaseForm, DeleteLinkcaseForm
from datetime import datetime

@app.context_processor
def inject_now():
    now = datetime.utcnow()
    linkcases = linkcase.get_all_linkcases(current_user)
    return {'now': now, 'linkcases': linkcases}


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    linkcases = linkcase.get_all_linkcases(current_user)
    linkcase_form = NewLinkcaseForm()
    del_linkcase_form = DeleteLinkcaseForm()
    linkcases_list = []
    for lc in linkcases:
        linkcase_dict = {'name': lc.name.replace(' ', '_'), 'links': [link for link in lc.links]}
        linkcases_list.append(linkcase_dict)

    if request.method == 'POST':
        if linkcase_form.linkcase_name.data and linkcase_form.validate():
            linkcase.create_linkcase(name=linkcase_form.linkcase_name.data, user=current_user)
            flash('Linkcase created successfully!')
            return redirect(url_for('index'))

        elif request.form.get("delete_linkcase"):
            linkcase.delete_linkcase(name=request.form['delete_linkcase'],user=current_user)
            flash('Linkcase deleted successfully!')
            return redirect(url_for('index'))

        elif request.form.get("delete_link"):
            def get_linkname_and_linkcasename_from_form(form_value):
                form_values = form_value.split('::')
                return form_values[0], form_values[1]
            link_name, linkcase_name = get_linkname_and_linkcasename_from_form(request.form['delete_link'])
            link.delete_link(link_name=link_name, parent_linkcase_name=linkcase_name, user=current_user)
            flash('Link deleted successfully!')
            return redirect(url_for('index'))

    return render_template('index.html', title='Dashboard', linkcase_form=linkcase_form, del_linkcase_form=del_linkcase_form, linkcases_list=linkcases_list)


@app.route('/linkcase/<linkcase_name>/detail', methods=['GET', 'POST'])
def linkcase_detail(linkcase_name):
    linkcases = linkcase.get_all_linkcases(current_user)
    linkcase_form = NewLinkcaseForm()
    link_form = NewLinkForm()
    del_linkcase_form = DeleteLinkcaseForm()

    detailed_linkcase = [lc for lc in linkcases if lc.name == linkcase_name][0]
    if request.method == 'POST':
        if linkcase_form.linkcase_name.data and linkcase_form.validate():
            linkcase.create_linkcase(name=linkcase_form.linkcase_name.data, user=current_user)
            flash('Linkcase created successfully!')
            return redirect(url_for('index'))

        elif link_form.validate():
            link.create_link(linkcase_name=detailed_linkcase.name, user=current_user, link_url=link_form.url.data, link_name=link_form.name.data)
            flash('Link added successfully!')
            return redirect(url_for('linkcase_detail', linkcase_name=linkcase_name))

        elif request.form.get("delete_linkcase"):
            linkcase.delete_linkcase(name=request.form['delete_linkcase'],user=current_user)
            flash('Linkcase deleted successfully!')
            return redirect(url_for('index'))

        elif request.form.get("delete_link"):
            def get_linkname_and_linkcasename_from_form(form_value):
                form_values = form_value.split('::')
                return form_values[0], form_values[1]
            link_name, linkcase_name = get_linkname_and_linkcasename_from_form(request.form['delete_link'])
            link.delete_link(link_name=link_name, parent_linkcase_name=linkcase_name, user=current_user)
            flash('Link deleted successfully!')
            return redirect(url_for('linkcase_detail', linkcase_name=linkcase_name))

    return render_template('linkcase_detail.html', linkcase_form=linkcase_form, link_form=link_form, del_linkcase_form=del_linkcase_form, detailed_linkcase=detailed_linkcase)


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
    return render_template('auth/login.html', title='Sign In', form=form)


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
    return render_template('auth/register.html', title='Register', form=form)
