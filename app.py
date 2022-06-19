from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate    import Migrate
from src.connectors import (connect_mariadb,
                            connect_mysql,
                            connect_postgres,
                            connect_sqlserver,
                            get_connection_method)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProjectDB.db'
app.config['TESTING'] = True
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = 'GDtfDCFYjD'

db = SQLAlchemy(app)



@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('dashboard/welcome.html')
    else:
        return render_template('index.html', message="Hello!")



@app.route('/check-connection/', methods=['GET','POST'])
def check_connection():

    if session.get('logged_in'):

        if request.method == 'POST':
            data_source = request.form['ds-name']
            connection_name = request.form['connectionName']
            host_name = request.form['hostName']
            port = int(request.form['port'])
            database = request.form['dbname']
            user = request.form['user']
            password = request.form['password']

            print(data_source,connection_name,host_name ,port ,database, user, password)
            print(type(data_source),type(connection_name), type(host_name) , type(port) , type(database), type(user), type(password))

            connection_status = get_connection_method(data_source,
                                            host_name, 
                                            port,
                                            database,
                                            user,
                                            password)
            
            
            return render_template('dashboard/connection_status.html', status= connection_status)

        return render_template('dashboard/welcome.html')
    else:
        return render_template('index.html', message="Hello!")




@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')



@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))




if __name__ == "__main__":
    from models.access import User
    db.create_all()
    app.run()