from flask import Flask, render_template, request, redirect # type: ignore
from users import User
app = Flask(__name__)

# immediately redirects to the home page when just '/' is called
@app.route('/')
def read():
    return redirect('/home')

# renders read.html and passes the User classmethod getall() to be displayed in the table
@app.route('/home')
def home():
    return render_template('read.html', users = User.get_all())

# renders the create form html page
@app.route('/home/create')
def create():
    return render_template('/create.html')

# listens on the /home/show which is the forms action on the create.html page, because its a form it also listens for the method=['POST] AND accepts it here under methods=['POST'], note the extra s on methods here in the listener. It takes in the info as data in the form of 'request.form' and that is injected into User class method save(); that triggers the query to add it to the database (see users.py)
# - we NEVER render on a 'POST' so we redirect home which again calls the get_all(). 
@app.route('/home/show', methods=['POST'])
def r_show():
    print(request.form)
    User.save(request.form)
    return redirect('/home')

if __name__ == "__main__":
    app.run(debug=True)