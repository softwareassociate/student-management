from flask import Flask, render_template, request,redirect
app=Flask(__name__)
import mysql.connector


db= mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="student_db"
    )

@app.route("/")
def home():
    search=request.args.get("search","")

    cursor = db.cursor()
    if search:
        query = """
        SELECT * FROM students
        WHERE name LIKE %s
        OR email LIKE %s
        OR course LIKE %s
        OR phone LIKE %s
        """

        search_value = "%" + search + "%"

        cursor.execute(
            query,
            (search_value, search_value, search_value, search_value)
        )
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    cursor.close()
    return render_template("index.html", students=students,search =search)

@app.route("/add", methods=["GET","POST"])
def add_student():
    if request.method=="POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        phone = request.form["phone"]

        cursor=db.cursor()

        query="""
        INSERT INTO students (name, email, course, phone)
        VALUES (%s, %s, %s, %s)
        """
        values=(name,email,course,phone)
        cursor.execute(query,values)

        db.commit()

        cursor.close()

        return redirect("/")

    return render_template("add_student.html")

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit_student(id):
    cursor=db.cursor()
    if request.method=="POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        phone = request.form["phone"]

        query = """
        UPDATE students
        SET name = %s, email = %s, course = %s, phone = %s
        WHERE student_id = %s
        """
        values=(name,email,course,phone,id)

        cursor.execute(query,values)

        db.commit()

        cursor.close()
        return redirect("/")
    cursor.execute("SELECT * FROM students WHERE student_id=%s",(id,))
    student=cursor.fetchone()
    cursor.close()
    return render_template("edit_student.html",student = student)

@app.route("/delete/<int:id>")
def delete_student(id):
    cursor=db.cursor()
    query="DELETE FROM students WHERE student_id=%s"

    cursor.execute(query,(id,))
    db.commit()
    cursor.close()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

