from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from myproject import db
from myproject.models import User 
from myproject.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from myproject.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)


##################################################
############### REGISTRATION #####################
##################################################

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(fname=form.fname.data,
                    lname=form.lname.data,
                    email=form.email.data,
                    contact = form.contact.data,
                    role = form.role.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


##################################################
############### LOG_IN ###########################
##################################################

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        try:
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                flash('You have been successfully logged in!', "info")
                next = request.args.get('next')
                if next == None or not next[0]=='/':
                    next = url_for('core.index')
                return redirect(next)
            else:
               flash('Invalid username or password!', "error") 
        except:
            flash('Account does not exist')    
    return render_template('login.html', form=form)

##################################################
############### LOG_OUT ##########################
##################################################

@users.route("/logout")
def logout():
    logout_user()
    flash('You have been successfully logged out!', "info")
    return redirect(url_for("core.index"))


##################################################
############# Account_Update_UserForm ############
##################################################

@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.contact = form.contact.data
        current_user.role = form.role.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.contact.data = current_user.contact
        form.role.data = current_user.role
        form.email.data = current_user.email

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)


