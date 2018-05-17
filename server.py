"""Givr."""

from jinja2 import StrictUndefined


from flask import (Flask, render_template, redirect, request, flash,
                   session)
from model import connect_to_db, db, Givr, Alt_choice, Giv, Recipient,Recipient_org
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

    email = request.form.get("email")
    email = session["email"]
    print email

    password = request.form.get("password")
    password = session["password"]
    print password

    fname = request.form.get("fname")
    session["fname"]
    print fname

    lname = request.form.get("lname")
    lname = session["lname"]
    print lname

    reference_email = Givr.query.filter_by(email=email).first()


    if request.method == "POST":

        print "in request.method == POST"

        """defining the user input that we are getting """

        if (("email" in session) and ("password" in session) and
            ("fname" in session) and ("lname" in session)):

            print "email, password, fname and lname in session"
            return redirect("/check-user")

    else:
        print "This is a new entry"
        return render_template("preferences_basic_info.html")


@app.route('/check-user', methods=["POST", "GET"])
def check_user():
    """allow a new user to register email address and password
    """

    print "I am in check-user route"

    email = session['email']
    password = session['password']

    print email
    print password

    reference_email = Givr.query.filter_by(email=email).first()

    # user_email = reference_email.email

    if reference_email:

        return render_template("log_in.html",
                               email=email,
                               password=password)
    else:
        return redirect("/preferences-basic-info")

@app.route('/preferences-small-giv', methods=["POST", "GET"])
def preferences_small_giv():
    """allow GivR to register preference for Small Givs."""
    print "I'm in /preferences-small-giv"
    if request.method == "POST":
        print "This is POST"
        """defining the user input that we are getting """

        smallgiv = request.form.get("smallgiv")

        if preferences_small_giv:

            session['smallgiv'] = smallgiv

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
        biggiv = request.form.get("biggiv")

        session['biggiv'] = biggiv

        print "I am the big giv amount the Givr chose", biggiv
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
    """Review GivR responses before instantiating user."""
    creditcardname = session["creditcardname"]
    creditcardnum = session["creditcardnum"]
    creditcardexp = session["creditcardexp"]
    creditcardccv = session["creditcardccv"]
    smallgiv = session["smallgiv"]
    biggiv = session["biggiv"]
    alternate_choice = session["alternate_choice"]

    """defining the user input that we are getting """

    email = request.form.get("email")
    session["email"] = email

    password = request.form.get("password")
    session["password"] = password

    fname = request.form.get("fname")
    session["fname"] = fname

    lname = request.form.get("lname")
    session["lname"] = lname

    if request.method == "POST":

        if (("email" in session) and ("password" in session) and ("fname" in session)
        and ("lname" in session) and ("creditcardname" in session) and ("creditcardnum" in session)
        and ("creditcardexp" in session) and ("creditcardccv" in session) and
        ("smallgiv" in session) and ("biggiv" in session) and ("alternate_choice" in session)):

            """Instantiating a new user """
            givr=Givr(email=email, password=password, fname=fname, lname=lname,
                creditcardname=creditcardname, creditcardnum=creditcardnum, creditcardexp=creditcardexp,
                creditcardccv=creditcardccv, smallgiv=smallgiv, biggiv=biggiv)

          #   sql = """INSERT INTO givrs (email, password, fname, lname, creditcardname, creditcardexp,
          #       creditcardccv, smallgiv, biggiv, alternate_choice)
          #    VALUES (:email, :password, :fname, :lname, :creditcardname, :creditcardexp,
          #       :creditcardccv, :smallgiv, :biggiv, :alternate_choice)
          # """

          #   db.session.execute(sql,
          #              {'email': email,
          #               'password': password,
          #               'fname': fname,
          #               'lname': lname,
          #               'creditcardname': creditcardname,
          #               'creditcardnum': creditcardnum,
          #               'creditcardexp': creditcardexp,
          #               'creditcardccv': creditcardccv,
          #               'smallgiv': smallgiv,
          #               'biggiv': biggiv,
          #               'alternate_choice': alternate_choice})

          #   db.session.commit()

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

            return redirect("/welcome-givr")


    return render_template("review_preferences.html", smallgiv=smallgiv,
                                                      biggiv=biggiv,
                                                      cardsuffix=creditcardnum[-4:],
                                                      alternate_choice=alternate_choice)


@app.route('/welcome-givr')
def welcome_givr():
    """Welcome the Givr and invite him/her to use Rapid Giv."""

    return render_template("welcome-givr.html")

@app.route("/log_in", methods=["POST", "GET"])
def log_in():
    """allow user to log_in
    """

    return render_template("log_in.html")


@app.route("/about_givr")
def about_givr():
    """allow user to learn about Givr."""

    return render_template("/about_givr.html")

@app.route("/contact_givr")
def contact_givr():
    """allow user to contact Givr."""

    return render_template("/contact_givr.html")


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