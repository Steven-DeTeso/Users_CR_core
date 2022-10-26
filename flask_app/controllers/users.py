from flask import render_template, request, redirect, session, url_for # type: ignore
from flask_app.models.user import User
from flask_app import app

# immediately redirects to the home page when just '/' is called
@app.route('/')
def read():
    return redirect('/home')

# renders read.html and passes the User classmethod getall() to be displayed in the table
@app.route('/home')
def home():
    return render_template('read.html', users = User.get_all())

# renders the create form html page
@app.route('/create')
def create():
    return render_template('/create.html')

# listens on the /process which is both forms action on the create.html and edit.html pages, because its a form it also listens for the method=['POST] AND accepts it here under methods=['POST'], note the extra s on methods here in the listener. It takes in the info as data in the form of 'request.form' and  performs an 'if check' if handle_type is 'create' form data is injected into User class method save(); that triggers the query to add it to the database (see users.py). If handle_type is 'edit', user_id data is injected into class method .update_user (see users.py)
# - we NEVER render on a 'POST' so we redirect home which again calls the get_all(). 
@app.route('/process', methods=['POST'])
def r_show():
    print(request.form)
    data = {
    'first_name': request.form['first_name'],
    'last_name': request.form['last_name'],
    'email': request.form['email'],
    }
    if request.form['handle_type'] == 'create':
        User.save(data)
        return redirect('/home')
    elif request.form['handle_type'] == 'edit':
        # line below appends 'user_id' key into data variable and assings the session value of user_id to it. 
        data['user_id'] = session['user_id']
        User.update_user(data)
        return redirect(url_for('r_user_show', id = int(session['user_id'])))

@app.route('/user/<int:id>')
def r_user_show(id):
    user_id = id # this is assiging the value of id into a variable called user_id
    session['user_id'] = user_id
    data = {
        'user_id': user_id
    }
    user = User.get_one(data)
    # setting variables here allows us to Jinja their values into the html page
    return render_template('read_one.html', user_id = user_id, user = user)

@app.route('/edit/<int:id>')
def r_edit_user(id):
    user_id = id
    session['user_id'] = user_id
    data = {
        'user_id': user_id
    }
    user = User.get_one(data)
    return render_template('edit.html', user_id = user_id, user = user)

@app.route('/user/delete/<int:id>')
def rd_delete(id):
    session['user_id'] = id
    data = {
        'user_id':session['user_id']
    }
    User.delete_user(data)
    return redirect('/home')