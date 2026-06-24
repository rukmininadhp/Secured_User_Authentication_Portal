from flask import Flask, render_template,request,redirect,session
import mysql.connector, bcrypt, secrets
app=Flask(__name__)

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="p1_ecom"
)
cursor=conn.cursor()

app.secret_key = "your-long-random-secret-key"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        mail=request.form["email"]
        passw=request.form["passw"]
        cursor.execute("select * from p1_ecom where email=%s",(mail,))
        user=cursor.fetchone()
        if not user:
            return "User not registered.....Please register first"
        
        cursor.execute("select password from p1_ecom where email=%s",(mail,))
        result=cursor.fetchone()
        stored_pass=result[0]
        v_pass=bcrypt.checkpw(passw.encode("utf-8"),stored_pass.encode("utf-8"))
        if v_pass:
            session["email"]=mail
            return redirect("/dashboard")
        else:
            return "Incorrect Password.....Please enter correct password"
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        mail=request.form["email_id"]
        pass1=request.form["password1"]
        pass2=request.form["password2"]
        
        cursor.execute("select * from p1_ecom where email=%s",(mail,))
        user=cursor.fetchone()
        if user:
            return "already registered"
        if pass1!=pass2:
            return "Please enter same passwords....."
        else:
            x="~!@#$%^&*()_+=-`<>?:,./;[]"
            if len(pass1)<8:
                return "password should be >= 8 charachers"
            for i in x:
                if i in pass1:
                    break
            else:
                return "Password should contain atleast 1 special character....."
            for i in pass1:
                if i>='A' and i<='Z':
                    break
            else:
                return "Password should contain Upper Case Letters"
            for i in pass1:
                if i>='a' and i<='z':
                    break
            else:
                return "Password should contain Lower Case Letters"
        
        hashed_pass=bcrypt.hashpw(pass1.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

        cursor.execute("insert into p1_ecom(email,password) values(%s,%s)", (mail,hashed_pass))
        conn.commit()

        return "Register successfull......Please Login"
        return redirect("/login")
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect("/login")
    return render_template("dashboard.html",email=session["email"])


@app.route("/profile")
def profile():
    if "email" not in session:
        redirect("/login")
    return render_template("profile.html", email=session["email"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
if "__main__"==__name__:
    app.run(debug=True)