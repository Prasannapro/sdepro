from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from .import db
from flask_login import login_user,login_required,logout_user,current_user
#login_manager



auth=Blueprint('auth',__name__)

@auth.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('pass')
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged sucessfully!',category='success')
                # login_user(user,remember=True)
                return redirect(url_for("auth.tenent"),user=user)
                # return redirect(url_for("tenent.html"),user=user)
                # tenent(user)
               # return redirect(url_for("views.home"))
            else:
                flash("incorrect password, try again",category='error')
        else:
            flash("email does not exist ",category='error')
    return render_template("login.html")


@auth.route("/tenent",methods=["POST","GET"])
def tenent():
    userobj=User.query.filter_by(email=email).first()
    return render_template("tenent.html",user=userobj)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))



@auth.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
       username=request.form.get("username")
       name=request.form.get("name")
       apno=request.form.get("apno")
       email=request.form.get("email")
       password=request.form.get("password")
       password1=request.form.get("password1")
    #    li=[username,name,apno,email,password,password1]
    #    print(li)
       user=User.query.filter_by(email=email).first()
       if user:
        flash("email already exists",category='error')
       elif len(email) <4:
        flash("email should be greater than 3 characters",category="error")
       elif len(name) and len(username) <2:
        flash("name and username should be greater than 3 characters",category="error")
        
       elif password1!=password:
        flash("password do not match",category="error")
        
       elif len(password1) <7:
        flash("password should be greater than 6 characters",category="error")
        
       else:
        new_user=User(email=email,password=generate_password_hash(password,method='sha256'),name=name,apno=apno,username=username)
        db.session.add(new_user)
        db.session.commit()
        # login_user(user,remember=True)


        flash("Account Created!!",category="success")
        #return redirect(url_for('views.home'))
        return redirect(url_for('auth.login'))

       
    return render_template("signup.html")