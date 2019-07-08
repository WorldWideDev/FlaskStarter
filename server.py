from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route("/")
def index():
    query = "SELECT * FROM users ORDER BY created_at DESC;"
    result = connectToMySQL("mydb").query_db(query)
    return render_template("index.html", users=result)

@app.route("/show/<user_id>")
def show(user_id):
    query = "SELECT * FROM users WHERE id = %(uid)s"
    data = { "uid": user_id }
    result = connectToMySQL("mydb").query_db(query, data)
    if result:
        return render_template("show.html", user=result[0])
    return redirect("/")

@app.route("/delete/<user_id>")
def delete(user_id):
    query = "DELETE users WHERE id = %(uid)s"
    data = { "uid": user_id }
    connectToMySQL("mydb").query_db(query, data)
    return redirect("/")


@app.route("/update/<user_id>", methods=["POST"])
def update(user_id):
    data = {
        "nm": request.form["name"],
        "loc": request.form["location"],
        "id": user_id
    }
    query = "UPDATE users SET name = %(nm)s, location = %(loc)s WHERE id = %(id)s"
    connectToMySQL("mydb").query_db(query, data)
    return redirect(f"/show/{user_id}")

@app.route("/create", methods=["POST"])
def create():
    data = {
        "nm": request.form['name'],
        "loc": request.form['location']
    }
    connectToMySQL("mydb").query_db("INSERT INTO users (name, location) VALUES (%(nm)s, %(loc)s)", data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
