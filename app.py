from flask import Flask, render_template, request       
from flask_mysqldb import MySQL
import mysql.connector # pip install mysql-connector-python
from flask_sqlalchemy import SQLAlchemy
import pickle
import joblib

app = Flask(__name__)

#-----------------------------------------Connection Database-----------------------------------------
def get_user_by_username(username):
    mydb = mysql.connector.connect(
        host="localhost",
        user=username,
        passwd="root",
        database="movie_5"
        )
    mycursor = mydb.cursor()
    #mycursor.execute("SELECT * FROM actor")
    return mydb, mycursor

mydb, mycursor = get_user_by_username("root")

#for x in mycursor:
#    print(x)

try:
    mydb, mycursor = get_user_by_username("root") 
    #mydb = mysql.connector.connect(
                                        #host = "localhost",
                                        #user="root",
                                        #passwd="root",
                                        #database = "movie_5",
                                        #auth_plugin='mysql_native_password',
                                        #)
except:
    print ("I am unable to connect to the database")



# 'mysql://username:password@localhost/dv_name'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@localhost/movie_5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/movie_5'


#-----------------------------------------Take data from Database-----------------------------------------
#mysql = MySQL(app)

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE DATABASE movie_metadata") #remove hashtag 
#my_cursor.execute("SHOW DATABASES")
#my_cursor.execute("USE movie_5")
my_cursor.execute("SELECT movie_title FROM movie_1")
#title=[item[0] for item in my_cursor.fetchall()]
movie_title=[item[0] for item in my_cursor.fetchall()]
movie_title_enumerated = list(enumerate(movie_title))
#print(movie_title[0])
my_cursor.execute("SELECT movie_imdb_link FROM movie_1")
movie_link=[item[0] for item in my_cursor.fetchall()]
movie_link_enumerated = list(enumerate(movie_link))
#print(movie_link[0])
#print(movie_title_enumerated)
#for row in my_cursor:
    #print(row)
my_cursor.close()

#----------------------------------------- creat model -----------------------------------------



#-----------------------------------------import model-----------------------------------------
#model = pickle.load(open('cosine_sim.pkl', 'rb'))
model = joblib.load(open('cosine_sim_notitle.joblib', 'rb'))
#model = joblib.load(open('clf_nn.joblib', 'rb'))

def recommendation(title, kernel):
    recomm = []
    for i in range(len(movie_title)):
        if movie_title_enumerated[i][1] == title:
            idx = movie_title_enumerated[i][0]
    global sim_scores
    sim_scores = list(enumerate(kernel[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    for y in movie_indices:
        recomm.append(movie_title[y])
        recomm.append(movie_link[y])
    return movie_indices, recomm

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/movie_5'
db = SQLAlchemy(app)
global name
veri = None
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    
    my_cursor = mydb.cursor(buffered=True)
    if request.method == 'POST':
        """name = request.values.get('Name')
        my_cursor.execute("USE movie_5;")
        my_cursor.execute("SELECT * FROM genres")
        veri = my_cursor.fetchall()
       
        my_cursor.close()"""
        
        movie = request.values.get('Name')
        not_found = 'not_found'
        if movie in movie_title:
            
            movies = recommendation(movie, model)
            print(movies[1])
            #imgs = scrapper(movies[0])
            return  render_template('index.html', movie=movies[1])
        
    return  render_template('index.html')

"""@app.route("/", methods=['GET', 'POST'])
def index():
    ## maths, pred, variable
    phrase = ""
    if request.method == "POST":
        phrase = "hello Eva, et Tolga et Jules ! Enjoy your april fool"
    return render_template("index.html",movie_title=movie_title)"""

if __name__ == "__main__":
    app.run(debug=True)


# https://www.codementor.io/@adityamalviya/python-flask-mysql-connection-rxblpje73