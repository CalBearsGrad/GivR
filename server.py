"""Givr."""

from jinja2 import StrictUndefined
from datetime import datetime

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from model import connect_to_db, db, Givr, Alt_choice, Giv, Recipient, Recipient_org, Restaurant, Item
from flask_debugtoolbar import DebugToolbarExtension
import requests
import random
from requests.auth import HTTPBasicAuth
from pprint import pprint



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.

app.jinja_env.undefined = StrictUndefined
# app.jinja_env.undefined = jinja2.StrictUndefined


@app.route('/')
def homepage():
    """Homepage, registration form and log-in."""

    return render_template("homepage.html")

@app.route('/terms_of_service')
def terms_of_use():
    """ Renders the terms of service"""

    return render_template("terms_of_service.html")

@app.route('/privacy_policy')
def privacy_policy():
    """ Renders the privacy policy"""

    return render_template("privacy_policy.html")

@app.route('/preferences-basic-info', methods=["POST", "GET"])
def preferences_basic_info():
    """allow GivR to register preference for Small Givs."""

    print "I'm in /preferences-basic-info"
    session.clear()
    print "session is clean."

    email = request.form.get("email")
    session["email"] = email
    print "email:", email

    password = request.form.get("password")
    session["password"] = password
    print "pw:", password

    fname = request.form.get("fname")
    session["fname"] = fname
    print "fname:", fname

    lname = request.form.get("lname")
    session["lname"] = lname
    print "lname:", lname


    if request.method == "POST":

        print "in request.method == POST"

        """defining the user input that we are getting """

        if ("email" in session) == None:
            print "didn't get email"

        elif (("email" in session) and ("password" in session) and
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

    email = request.form.get("email")
    password = request.form.get("password")

    print email
    print password

    reference_email = Givr.query.filter_by(email=email).first()

    # user_email = reference_email.email

    if reference_email:
        print
        print "Email address matches GivrR in database"
        print
        session.clear()
        session['email'] = email
        session['password'] = password

        return redirect("/log_in")
    else:
        return redirect("/preferences-small-giv")

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

        if ("smallgiv" in session) and ("biggiv" in session):

            return redirect("/alt_choice")
        else:
            return render_template("homepage.html")

    return render_template("preferences-big-giv.html")


@app.route('/alt_choice', methods=["POST", "GET"])
def register_alt_choice():
    """Obtain user's preference in case requested visibly homeless is not at location\
    upon delivery."""


    if request.method == "POST":

        print "This is request.form", request.form

        alternate_choice = int(request.form.get("choice"))
        print "I am alt_choice", alternate_choice

        """defining the user input that we are getting """

        print "I am in alternate-choice POST"

        session['alternate_choice'] = alternate_choice

        if ("alternate_choice" in session):

            return redirect("/payment-info")

        else:
            return redirect("alt_choice")

    return render_template("alt_choice.html")

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

        creditcardexp = datetime.strptime(creditcardexp, "%m/%y").strftime("%Y-%m-%d")
        print "I am new creditcardexp", creditcardexp

        session['creditcardname'] = creditcardname
        session['creditcardnum'] = creditcardnum
        session['creditcardexp'] = creditcardexp
        session['creditcardccv'] = creditcardccv

        print "all credit card info is in session"

        if ("creditcardname" in session) and ("creditcardnum" in session) and ("creditcardexp" in session) and ("creditcardccv" in session):

            return render_template("review_preferences.html")
        else:
            return render_template("payment_info.html")

    return render_template("payment_info.html")


@app.route('/review_preferences', methods=["POST", "GET"])
def review_preferences():
    """Review GivR responses before instantiating user."""
    email = session["email"]
    password = session["password"]
    fname = session["fname"]
    lname = session["lname"]
    creditcardname = session["creditcardname"]
    creditcardnum = session["creditcardnum"]
    creditcardexp = session["creditcardexp"]
    creditcardccv = session["creditcardccv"]
    smallgiv = session["smallgiv"]
    biggiv = session["biggiv"]
    alternate_choice = session["alternate_choice"]


    """defining the user input that we are getting """

    print "This is session", session

    print "This is request.method", request.method



    if request.method == "GET":
        print "in GET and about to make a GivR!"

        if (("email" in session) and ("password" in session) and ("fname" in session)
        and ("lname" in session) and ("creditcardname" in session) and ("creditcardnum" in session)
        and ("creditcardexp" in session) and ("creditcardccv" in session) and
        ("smallgiv" in session) and ("biggiv" in session) and ("alternate_choice" in session)):

            """Instantiating a new user """
            print "Getting ready to instantiate a new user"
            givr=Givr(email=email, password=password, fname=fname, lname=lname,
                creditcardname=creditcardname, creditcardnum=creditcardnum, creditcardexp=creditcardexp,
                creditcardccv=creditcardccv, smallgiv=smallgiv, biggiv=biggiv, alt_choice_id=alternate_choice)

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
            print "I am alternate_choice", alternate_choice

            db.session.add(givr)
            db.session.commit()

            print "We created a new GivR!"

            flash("You have registered successfully")

            return redirect("/welcome-givr")


    return render_template("review_preferences.html", smallgiv=smallgiv,
                                                      biggiv=biggiv,
                                                      cardsuffix=creditcardnum[-4:],
                                                      alternate_choice=alternate_choice)


@app.route('/welcome-givr', methods=["POST", "GET"])
def welcome_givr():
    """Welcome the Givr and invite him/her to use Rapid Giv."""

    email = session["email"]
    user = Givr.query.filter_by(email=email).first()
    fname = user.fname

    return render_template("welcome-givr.html", fname=fname)


@app.route("/log_in", methods=["POST", "GET"])
def log_in():
    """allow user to log_in"""

    email = session["email"]
    password = session["password"]

    return render_template("log_in.html", email=email, password=password)


@app.route("/about_givr")
def about_givr():
    """allow user to learn about Givr."""

    return render_template("/about_givr.html")


@app.route("/contact_givr")
def contact_givr():
    """allow user to contact Givr."""

    return render_template("/contact_givr.html")


@app.route("/log_out")
def log_out():
    """allow user to log out of Givr."""
    session.clear()

    return redirect("/")


@app.route("/rapid_small_giv", methods=['POST', 'GET'])
def rapid_giv():
    """allow user to complete a giv."""

    email = session["email"]
    user = Givr.query.filter_by(email=email).first()
    fname = user.fname
    giv_amount = user.smallgiv
    session["giv_amount"] = giv_amount
    # giv_size = request.args.get("smallgiv")

    restaurant = {"name": "Lers Ros Thai",
              "address": "307 Hayes St, San Francisco, CA 94102",
              "long_lat": "37.776997, -122.421683",
              "items": [["Jasmine Steamed Rice", 2.00],
                        ["Sticky Rice", 2.50],
                        ["Brown Rice", 2.50],
                        ["Steamed Rice Noodle", 3.00],
                        ["Cucumber Salad", 3.95],
                        ["Sweet Sticky Rice", 4.95],
                        ["Brown Rice & Peanut Sauce", 6.45],
                        ["Jasmine Steamed Rice & Peanut Sauce", 5.95],
                        ["Steamed Rice Noodle & Peanut Sauce", 6.95],
                        ["Pad Kee Moo", 11.95],
                        ["Pad See Ew", 11.95],
                        ["Pad Thai", 11.95]],
               "delivery_fee": 3.99}

    restaurant_one = Restaurant.query.all().first()
    print restaurant_one

    famous_inventors_of_color = ["Madam C.J. Walker", "George Washington Carver", "Thomas L. Jennings"]

    if request.method == "POST":
        # Get Form Data (giv_size and address)

        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")

        full_address = "{}, {}, {} {}".format(address, city, state, zipcode)
        print "full_address: ", full_address
        pickup_notes = "Please make sure that the order includes eating utensils and napkins."
        dropoff_notes = "Please deliver to visibly homeless individual in front of addresss or very close to address. "
        # Get giv amount from user object's attributes



        ################################# Create postmates request
        #Delivery Quotes
        payload = {"dropoff_address": full_address,
                    "pickup_address": "307 Hayes St, San Francisco, CA 94102"}

        print "payload: ", payload

        response_from_postmates = requests.post("https://api.postmates.com/v1/customers/cus_Lk1phJYn_uU88V/delivery_quotes", data=payload, auth=("a03e8608-cf6b-4441-ade2-696e2c437d6c", ''))
        response_from_postmates_dictionary = response_from_postmates.json()
        print
        pprint(response_from_postmates_dictionary)
        print
        print response_from_postmates_dictionary['currency']
        # print quote_id = response_from_postmates_dictionary['id']

        ################################# Create postmates request
        #Create a Delivery
        payload_delivery = {"quote_id": quote_id,
                            "manifest": restaurant["items"][4],
                            "manifest_reference": random.choice(famous_inventors_of_color),
                            "pickup_name": restaurant["name"],
                            "pickup_address": restaurant["name"],
                            "pickup_latitude": restaurant["long_lat"][1],
                            "pickup_longitude": restaurant["long_lat"][0],
                            "pickup_phone_number": restaurant["phone"],
                            "pickup_business_name": restaurant["name"],
                            "pickup_notes": pickup_notes,
                            "dropoff_name": "unknown",
                            "dropoff_address": full_address,
                            "dropoff_latitude": "N/A",
                            "dropoff_longitude": "N/A",
                            "dropoff_phone_number": "N/A",
                            "dropoff_business_name": "N/A",
                            "dropoff_notes": dropoff_notes,
                            "requires_id": "false",
                            }
        print "payload_delivery: ", payload_delivery

        response_from_postmates_delivery = requests.post("https://api.postmates.com/v1/customers/cus_Lk1phJYn_uU88V/delivery_quotes", data=payload, auth=("a03e8608-cf6b-4441-ade2-696e2c437d6c", ''))
        response_from_postmates_dictionary = response_from_postmates.json()
        print
        pprint(response_from_postmates_dictionary)
        print
        print response_from_postmates_dictionary['currency']

        # Flash success message or redirct user
    return render_template("/rapid_small_giv.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5001, host='0.0.0.0')