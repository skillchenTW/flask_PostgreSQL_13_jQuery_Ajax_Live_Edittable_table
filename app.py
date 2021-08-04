from flask import Flask, render_template,request,jsonify
import psycopg2 
import psycopg2.extras

app = Flask(__name__)

app.secret_key = "SkillChen_Secret_Key"

DB_HOST = 'localhost'
DB_PORT = '5433'
DB_USER = 'postgres'
DB_PASS = 'dba'
DB_NAME = 'sampledb'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)

@app.route("/")
def home():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("Select * from users order by id")
        userslist = cursor.fetchall()
        return render_template('index.html', userslist=userslist)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    
@app.route("/update", methods=["POST", "GET"])
def update():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == 'POST':
            field = request.form['field']
            value = request.form['value']
            editid = request.form['id']

            if field == 'username':
                sql = "UPDATE users set username=%s where id=%s"
            if field == 'name':
                sql = "UPDATE users set fullname=%s where id=%s"
            data = (value, editid)
            cursor.execute(sql, data)
            conn.commit()
            success = 1
        return jsonify(success)
    except Exception as e:
        print(e)
    finally:
        cursor.close()





if __name__ == '__main__':
    app.run(debug=True)