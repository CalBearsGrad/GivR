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

        if ("creditcardname" in session) and ("creditcardnum" in session) and (
            "creditcardexp" in session) and ("creditcardccv" in session):

            return redirect("/alternate-choice")
        else:
            return render_template("payment_info.html")

    return render_template("payment_info.html")



@app.route('/alternate-choice')
def register_alt_choice():
    """Obtain user's preference in case requested visibly homeless is not at location\
    upon delivery."""
    alternate_choice1 = request.form.get("Deliver to another visibly homeless individual")
    alternate_choice2 = request.form.get("Deliver to the nearest 24-hour Homeless Shelter")
    alternate_choice3 = request.form.get("Receive a Refund")

    if request.method == "POST":
        """defining the user input that we are getting """

        print "I am in alternate-choice POST"

    if alternate_choice1:
        session['alternate_choice1'] = alternate_choice
        print "user choose choice 1"
    elif alternate_choice2:
        session['alternate_choice2'] = alternate_choice
        print "user choose choice 2"
    else:
        session['alternate_choice3'] = alternate_choice
        print "user choose choice 3"

    print "alternate choice was made by GivR"

    if ("alternate_choice" in session):

        return redirect("/review-preferences")

    else:
        return render_template("payment_info.html")

    return render_template("payment_info.html")

@app.route('/review-preferences')
def review_preferences():
    """Review GivR responses before instantiating user."""

    return render_template("review-preferences.html")

    """defining the user input that we are getting """
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    email = session["email"]
    password = session["password"]

    """Instantiating a new user """
    givr = User(email=email, password=password, age=age, zipcode=zipcode)
    print "I am email", email
    print "I am password", password
    print "I am age", age
    print "I am zipcode", zipcode
    db.session.add(user)
    db.session.commit()
    print "We created a new user!"

    flash("You have registered successfully")

    return render_template("log_in.html")


# @app.route('/welcome-givr')
# def index():
#     """Welcome the Givr and invite him/her to log-in."""

#     return render_template("homepage.html")

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