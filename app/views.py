"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from flask import render_template, request, redirect, url_for, flash,session, abort, send_from_directory
from werkzeug.utils import secure_filename
import os
from app import app, db, login_manager
from app.forms import PropertyForm
from app.models import Property
from app.forms import UploadForm
from app.forms import LoginForm
from app.models import UserProfile
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.utils import get_uploaded_images



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Jhanell Edwards")


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/properties/create', methods= ['GET', 'POST'])
def create():
    #function to display the form to add a new property
    form = PropertyForm()
    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        property = Property(
            title = form.title.data, 
            description = form.description.data,  
            bedrooms = form.bedrooms.data, 
            bathrooms = form.bathrooms.data,
            price = form.price.data,
            type = form.property_type.data,
            location = form.location.data,
            photo = filename
        )
        db.session.add(property)
        db.session.commit()
        flash("Property created.")
        return redirect(url_for('properties'))
    else:
        flash_errors(form)
    return  render_template('create_property.html', form=form)
    
    
    
@app.route('/properties')
def properties():
    #function to display list of all properties
    properties = Property.query.all()
    return render_template('property_listing.html', properties = properties)
    
    
@app.route('/properties/<int:property_id>')
def view(property_id):
    #for viewng specific property
    property = Property.query.get_or_404(property_id)
    return render_template('view.html', property = property, property_id = property_id)

@app.route('/uploads/<filename>')
def photo(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)
  

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    # change this to actually validate the entire form submission
    # and not just one field
    if form.username.data:
        # Get the username and password values from the form.
        
        username = form.username.data
        password = form.password.data
        
        # Using your model, query database for a user based on the username
        user = UserProfile.query.filter_by(username=username).first()
         
        # and password submitted. Remember you need to compare the password hash.
        if user and check_password_hash(user.password, password):
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.

            # Gets user id, load into session
            login_user(user)

        # Remember to flash a message to the user
        flash('Login successful!', 'success')
        
        return redirect(url_for("create"))  # The user should be redirected to the property form instead
    
    return render_template("login.html", form=form)


@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()


###
# The functions below should be applicable to all Flask apps.
###
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
