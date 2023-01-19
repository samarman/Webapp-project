from flask import Flask, render_template, request, redirect
#from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

#setup the app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ellie&Otis2023'
app.config['MYSQL_DB'] = 'resources'
mysql = MySQL(app)


@app.route('/')
def index():
    # Render the home page with a form for the user to submit a link and comment
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve the link and comment from the form
    link = request.form['link']
    comment = request.form['comment']
    
    # Save the link and comment to the MySQL database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO resources (link, comment) VALUES (%s, %s)", (link, comment))
    mysql.connection.commit()
    cur.close()
    
    return redirect('/resources')

@app.route('/resources')
def resources():
    # Retrieve the link and comment from the MySQL database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM resources")
    resources = cur.fetchall()
    print(resources)
    cur.close()
    
    # Render the resources page with the link and comment
    return render_template('resources.html', resources=resources)

if __name__ == "__main__":
    app.run(debug=True)