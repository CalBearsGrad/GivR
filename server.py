"""Givr."""

from jinja2 import StrictUndefined
from datetime import datetime

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from model import connect_to_db, db, Givr, Alt_choice, Giv, Recipient,Recipient_org, Restaurant, Item
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

#function to choose the closest restaurant in the restaurants table to the drop off address provided
def find_closest_restaurant():
   if Restaurant.query.count() > 0:
        closest_restaurant = Restaurant.query.first()
        # restaurants = Restaurant.query.all()
        # restaurant = Restaurant.query.one()

        # for restaurant in restaurants:
        #     #if restaurant distance from full_address is less than closest_restaurant.address
        #     if restaurant.address()
        #         closest_restaurant = restaurant
        print closest_restaurant
        return closest_restaurant

#function to find the item that, when combined with tax and delivery fee, is equal to or less than the small giv amount that the user provided
def find_match_name(closest_restaurant, giv_amount):

    items = Item.query.filter(Item.restaurant_id == closest_restaurant.restaurant_id and (1.085 *(Item.price + delivery_fee)) < giv_amount).all()

    #if there are indeed items in our Items table
    if items:
        item = items[0]
        delivery_fee = closest_restaurant.delivery_fee
        best_price_match = 1.085 * (item.price + delivery_fee)
        best_match_name = item.name
        #if there is a perfect match between giv amount and the best_price_match
        if giv_amount == best_price_match:
            return best_match_name

        #if the small giv amount that the user chose is more than or less than best_price_match
        elif giv_amount > best_price_match or giv_amount < best_price_match:
            #then, iterate through the rows of item.prices in Items table
            for item in items:
                #if the cost of the item with tax and delivery is closer to the giv_amount than the best_price_match with out going over
                #How can I guard against for negative amounts misleading my compiler?
                if (giv_amount - (1.085 *(item.price + delivery_fee))) < (giv_amount - best_price_match):
                    #then the new best_price_match is the new item price
                    best_price_match = item.price
                    best_match_name = item.name

            return best_match_name


@app.route("/rapid_small_giv", methods=['POST', 'GET'])
def rapid_giv():
    """allow user to complete a giv."""

    email = session["email"]
    user = Givr.query.filter_by(email=email).first()
    fname = user.fname
    giv_amount = user.smallgiv
    session["giv_amount"] = giv_amount
    # giv_size = request.args.get("smallgiv")


    famous_inventors = ["Thomas L. Jennings", "Mark E. Dean", "Madam C.J. Walker", "Dr. Shirely Jackson",
                        "Charles Richard Dew", "Marie Van Brittan Brown", "George Carruthers", "Dr. Patricia Bath",
                        "Jan E. Matzeliger", "Alexander Miles"]

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

        closest_restaurant = find_closest_restaurant()

        best_match_name = find_match_name(closest_restaurant, giv_amount)

        ################################# Create postmates request
        #Delivery Quotes
        payload = {"dropoff_address": full_address,
                    "pickup_address": closest_restaurant.address}

        print "payload: ", payload

        response_from_postmates = requests.post("https://api.postmates.com/v1/customers/cus_Lk1phJYn_uU88V/delivery_quotes", data=payload, auth=("a03e8608-cf6b-4441-ade2-696e2c437d6c", ''))
        response_from_postmates_dictionary = response_from_postmates.json()
        print
        pprint(response_from_postmates_dictionary)
        print
        print response_from_postmates_dictionary['currency']
        quote_id = response_from_postmates_dictionary['id']

        ################################# Create postmates request
        #Create a Delivery
        payload_delivery = {"quote_id": quote_id,
                            "manifest": best_match_name,
                            "manifest_reference": random.choice(famous_inventors) + "1234", #how to auto increment the order number?
                            "pickup_name": closest_restaurant.name,
                            "pickup_address": closest_restaurant.address,
                            "pickup_phone_number": "510-866-4577",
                            "pickup_business_name": closest_restaurant.name,
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

        #all of this needs updating
        response_from_postmates_delivery = requests.post("https://api.postmates.com/v1/customers/cus_Lk1phJYn_uU88V/delivery", data=payload_delivery, auth=("a03e8608-cf6b-4441-ade2-696e2c437d6c", ''))
        response_from_postmates_dictionary = response_from_postmates.json()
        print
        pprint(response_from_postmates_dictionary)
        print

        giv =


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