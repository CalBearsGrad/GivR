"""Givr."""

from jinja2 import StrictUndefined


from flask import (Flask, render_template, redirect, request, flash,
                   session)
from model import connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.

app.jinja_env.undefined = StrictUndefined
# app.jinja_env.undefined = jinja2.StrictUndefined


@app.route('/')
def index():
    """Homepage, registration form and log-in."""

    return render_template("homepage.html")


@app.route('/preferences-basic-info', methods=["POST", "GET"])
def preferences_basic_info():
    """allow GivR to register preference for Small Givs."""

    print "I'm in /preferences-basic-info"

    email = session["email"]
    print email

    password = session["password"]
    print password

    fname = session["fname"]
    print fname

    lname = session["lname"]
    print lname

    reference_email = givr.query.filter_by(email=email).first()

    if reference_email:

        alert("You already have an account. Redirecting to log-in.")
        return render_template("log_in.html")

        if request.method == "GET":

            print "in request.method == GET"

            """defining the user input that we are getting """

            if (("email" in session) and ("password" in session) and
                ("fname" in session) and ("lname" in session)):

                print "email, password, fname and lname in session"
                return redirect("/check-user")

            else:
                print "I AM IN ELSE"
                return render_template("preferences_basic_info.html")
    else:
        print "This is GET"
        return render_template("preferences_basic_info.html")


@app.route('/check-user', methods=["POST", "GET"])
def check_user():
    """allow a new user to register email address and password
    """

    email = session['email']
    password = session['password']

    # print User.query.filter_by(email=email).first()

    print email
    print password

    reference_email = Givr.query.filter_by(email=email).first()

    # user_email = reference_email.email

    if reference_email:

        return render_template("log_in.html",
                               email=email,
                               password=password)
    else:
        return redirect("preferences-small-giv",
                               email=email,
                               password=password)

@app.route('/preferences-small-giv', methods=["POST", "GET"])
def preferences_small_giv():
    """allow GivR to register preference for Small Givs."""
    print "I'm in /preferences-small-giv"
    if request.method == "POST":
        print "This is POST"
        """defining the user input that we are getting """

        preferences_small_giv = request.form.get("smallgiv")

        if preferences_small_giv:

            session['smallgiv'] = preferences_small_giv

            return redirect("/preferences-big-giv")
        else:
            print "I AM IN ELSE"
            return render_template("preferences-small-giv.html")
    else:
        print "This is GET"
        return render_template("preferences-small-giv.html")


@app.route('/preferences-big-giv', methods=["POST", "GET"])
def preferences_big_giv():
    """allow GivR to register preference for Big Givs."""

    if request.method == "POST":
        """defining the user input that we are getting """
        preferences_big_giv = request.form.get("biggiv")

        session['biggiv'] = preferences_big_giv

        print "I am the big giv amount the Givr chose", preferences_big_giv
        print "I am the small giv amount the GivR chose", session['smallgiv']

        if ("smallgiv" in session) and preferences_big_giv:

            return redirect("/payment-info")
        else:
            return render_template("homepage.html")

    return render_template("preferences-big-giv.html")


@app.route('/payment-info', methods=["POST", "GET"])
def payment_info():
    """allow GivR to register credit card."""

    if request.method == "POST":
        """defining the user input that we are getting """

        print "I am in payment_info POST"
        creditcardname = request.form.get("creditcardname")
        creditcardnum = request.form.get("creditcardnum")
        creditcardexp = request.form.get("creditcardexp")
        creditcardccv = request.form.get("creditcardccv")

        session['creditcardname'] = creditcardname
        session['creditcardnum'] = creditcardnum
        session['creditcardexp'] = creditcardexp
        session['creditcardccv'] = creditcardccv

        print "all credit card info is in session"

        if ("creditcardname" in session) and ("creditcardnum" in session) and ("creditcardexp" in session) and ("creditcardccv" in session):

            return redirect("/alt_choice")
        else:
            return render_template("payment_info.html")

    return render_template("payment_info.html")


@app.route('/alt_choice', methods=["POST", "GET"])
def register_alt_choice():
    """Obtain user's preference in case requested visibly homeless is not at location\
    upon delivery."""

    print request.form

    alternate_choice1 = request.form.get("alt_choice1")
    alternate_choice2 = request.form.get("alt_choice2")
    alternate_choice3 = request.form.get("alt_choice3")

    if request.method == "POST":
        """defining the user input that we are getting """

        print "I am in alternate-choice POST"

        if alternate_choice1:
            session['alternate_choice'] = alternate_choice1
        elif alternate_choice2:
            session['alternate_choice'] = alternate_choice2
            print "user choose choice 2"
        elif alternate_choice3:
            session['alternate_choice'] = alternate_choice3
            print "user choose choice 3"

        if ("alternate_choice" in session):

            return redirect("/review_preferences")

        else:
            return redirect("alt_choice")

    return render_template("alt_choice.html")


@app.route('/review_preferences', methods=["POST", "GET"])
def review_preferences():
    """Review GivR responses before instantiating user. Below are placeholders."""
    creditcardname = session["creditcardname"]
    creditcardnum = session["creditcardnum"]
    creditcardexp = session["creditcardexp"]
    creditcardccv = session["creditcardccv"]
    smallgiv = session["smallgiv"]
    biggiv = session["biggiv"]
    alternate_choice = session["alternate_choice"]

    """defining the user input that we are getting """

    if request.method == "POST":
        email = request.form.get("email")
        session["email"] = email

        password = request.form.get("password")
        session["password"] = password

        fname = request.form.get("fname")
        session["fname"] = fname

        lname = request.form.get("lname")
        session["lname"] = lname


        if (("email" in session) and ("password" in session) and ("fname" in session)
        and ("lname" in session) and ("creditcardname" in session) and ("creditcardnum" in session)
        and ("creditcardexp" in session) and ("creditcardccv" in session) and
        ("smallgiv" in session) and ("biggiv" in session)):


            """Instantiating a new user """
            givr=User(email=email, password=password, fname=fname, lname=lname,
                creditcardname=creditcardname, creditcardnum=creditcardnum, creditcardexp=creditcardexp,
                creditcardccv=creditcardccv, smallgiv=smallgiv, biggiv=biggiv)

            print "I am email", email
            print "I am password", password
            print "I am fname", fname
            print "I am lname", lname
            print "I am creditcardname", creditcardname
            print "I am creditcardnum", creditcardnum
            print "I am creditcardexp", creditcardexp
            print "I am creditcardccv", creditcardccv
            print "I am smallgiv", smallgiv
            print "I am biggiv", biggiv

            db.session.add(givr)
            db.session.commit()

            print "We created a new GivR!"

            flash("You have registered successfully")

            return render_template("welcome-givr.html")

    return render_template("review_preferences.html", smallgiv=smallgiv,
                                                      biggiv=biggiv,
                                                      cardsuffix=creditcardnum[-4:],
                                                      alternate_choice=alternate_choice)


@app.route('/welcome-givr')
def welcome_givr():
    """Welcome the Givr and invite him/her to use Rapid Giv."""

    return render_template("welcome-givr.html")

# @app.route('/logged-in-homepage')
# def index():
#     """Homepage and registration form."""

#     return render_template("homepage.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')