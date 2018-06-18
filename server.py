"""Givr."""

from jinja2 import StrictUndefined
from datetime import datetime

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from model import connect_to_db, db, Givr, Alt_choice, Giv, Recipient,Recipient_org, Restaurant, Item
from flask_debugtoolbar import DebugToolbarExtension
import requests
import random
from requests.auth import HTTPBasicAuth
from pprint import pprint
from sqlalchemy import extract



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

def correct_tax_deductible_givs():
    """Will find tax deductible givs and will
    change the value for "tax_exempt" to True"""

    email = session["email"]

    user = Givr.query.filter_by(email=email).first()

    givs = Giv.query.filter_by(givr_id=user.givr_id).all()
    print "We are here!"
    if givs:
        for giv in givs:
            if giv.recipient_id == 1 or giv.recipient_id == 2:
                giv.tax_exempt = True
                print giv

            db.session.add(giv)
        db.session.commit()


    # total_tax_deductible_givs_for_givr = givs.query.filter_by(givs.tax_exempt=True).count()

    # sum_tax_deductible_givs_for_givr = sum(givs.query.filter_by(givs.tax_exempt=True)).all()

    # average_of_tax_deductible_givs_for_givr = sum_tax_deductible_givs_for_givr / total_tax_deductible_givs_for_givr

    # return total_tax_deductible_givs_for_givr, sum_tax_deductible_givs_for_givr, average_of_tax_deductible_givs_for_givr


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
            return redirect("/check-user", email=email, password=password, fname=fname, lname=lname)

    else:
        print "This is a new entry"
        return render_template("preferences_basic_info.html")


@app.route('/check-user', methods=["POST", "GET"])
def check_user():
    """allow a new user to register email address and password
    """

    print "I am in check-user route"
    if ("email" in session) == None:
            print "didn't get email"

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
        print "This is smallgiv: ", smallgiv

        if preferences_small_giv:

            session['smallgiv'] = smallgiv
            print "This is smallgiv in session", smallgiv

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

        email = session["email"]
        password = session["password"]
        fname = session["fname"]
        lname = session["lname"]
        session["creditcardname"] = creditcardname
        session["creditcardnum"] = creditcardnum
        print "This is the type creditcardnum is", type(creditcardnum)
        cardsuffix = (str(creditcardnum)[-4:])
        session["creditcardexp"] = creditcardexp
        session["creditcardccv"] = creditcardccv
        smallgiv = session["smallgiv"]
        biggiv = session["biggiv"]
        alternate_choice = session["alternate_choice"]

        def describe_alt_choice():
            if alternate_choice == 1:
                choice = "deliver to nearest visibly homeless individual"
            elif alternate_choice == 2:
                choice = "deliver to nearest 24hr homeless shelter"
            elif alternate_choice == 3:
                choice = "process a refund"

            return choice

        choice = describe_alt_choice()

        print "all credit card info is in session"

        if ("creditcardname" in session) and ("creditcardnum" in session) and ("creditcardexp" in session) and ("creditcardccv" in session):

            return render_template("review_preferences.html", email=email,
                                                   password=password,
                                                   fname=fname,
                                                   lname=lname,
                                                   creditcardname=creditcardname,
                                                   creditcardnum=creditcardnum,
                                                   creditcardexp=creditcardexp,
                                                   creditcardccv=creditcardccv,
                                                   smallgiv=smallgiv,
                                                   biggiv=biggiv,
                                                   alternate_choice=alternate_choice,
                                                   choice=choice,
                                                   cardsuffix=cardsuffix)
        else:
            return render_template("payment_info.html")

    return render_template("payment_info.html")


@app.route('/review_preferences', methods=["POST", "GET"])
def review_preferences():
    """Review GivR responses before instantiating user."""
    print "In review preferences"

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
        else:
            print
            print "Something is wrong"
            print "***************"
            print "See what is missing"
            print "*******************"

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


    return render_template("review_preferences.html", smallgiv=smallgiv,
                                                      biggiv=biggiv,
                                                      cardsuffix=creditcardnum[-4:],
                                                      alternate_choice=alternate_choice)


@app.route('/welcome-givr', methods=["POST", "GET"])
def welcome_givr():
    """Welcome the Givr and invite him/her to use Rapid Giv."""

    email = session["email"]
    user = Givr.query.filter_by(email=email).first()
    print "This is user", user
    fname = user.fname

    return render_template("welcome-givr.html", fname=fname)


@app.route("/log_in", methods=["POST", "GET"])
def log_in():
    """allow user to log_in"""

    if "email" in session:
        email = session["email"]
        password = session["password"]

    else:
        email = ""
        password = ""
        

    if request.method == "POST":
        email = request.form.get("email")
        session["email"] = email
        password = request.form.get("password")
        session["password"] = password


        return redirect("/welcome-givr")

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

            return best_match_name, best_price_match

def make_recipient():
    """Instantiating a new Recipient """
    print "Getting ready to instantiate a new recipient"


    address = actual_destination.rstrip()

    address, city, N = row.split(",")
    state, zipcode = N.split(" ")

    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=address,+city+state,+zipcode')

    resp_json_payload = response.json()

    print(resp_json_payload['results'][0]['geometry']['location'])


    recipient = Recipient(recipient_id=recipient_id,
                          address=address,
                          city=city,
                          state=state,
                          zipcode=zipcode,
                          latitude=latitude,
                          longitude=longitude,
                          recipient_type=recipient_type)


    # Flash success message or redirct user
    db.session.add(giv)
    db.session.commit()


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
        print "*****************************closest_restaurant: \n"
        print type(closest_restaurant)
        print closest_restaurant

        best_match_name, best_price_match = find_match_name(closest_restaurant, giv_amount)

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
                            "manifest_reference": random.choice(famous_inventors) + " " + quote_id, #how to auto increment the order number?
                            "pickup_name": closest_restaurant.name,
                            "pickup_address": closest_restaurant.address,
                            "pickup_phone_number": "510-866-4577",
                            "pickup_business_name": closest_restaurant.name,
                            "pickup_notes": pickup_notes,
                            "dropoff_name": "unknown",
                            "dropoff_address": full_address,
                            "dropoff_phone_number": "888-712-9985",
                            "dropoff_business_name": "N/A",
                            "dropoff_notes": dropoff_notes,
                            "requires_id": "false",
                            }
        print "payload_delivery: ", payload_delivery

        #all of this needs updating
        response_from_postmates_delivery = requests.post("https://api.postmates.com/v1/customers/cus_Lk1phJYn_uU88V/deliveries", data=payload_delivery, auth=("a03e8608-cf6b-4441-ade2-696e2c437d6c", ''))
        response_from_postmates_dictionary = response_from_postmates_delivery.json()
        print
        pprint(response_from_postmates_dictionary)
        print

        """Instantiating a new giv """
        print "Getting ready to instantiate a new giv"

        manifest_reference = payload_delivery["manifest_reference"]
        tracking_url = response_from_postmates_dictionary["tracking_url"]
        date_of_order = response_from_postmates_dictionary["created"]
        date_of_delivery = response_from_postmates_dictionary["dropoff_eta"]
        requested_destination = payload_delivery["dropoff_address"]
        actual_destination = payload_delivery["dropoff_address"]
        total_amount = best_price_match
        successful_delivery = True
        # recipient_id =
        size = "small"
        tax_exempt = False
        restaurant = Restaurant.query.filter_by(name=closest_restaurant.name).first()
        print restaurant.restaurant_id

        giv = Giv(givr_id=user.givr_id,
                  restaurant_id=restaurant.restaurant_id,
                  date_of_order=date_of_order,
                  date_of_delivery=date_of_delivery,
                  requested_destination=requested_destination,
                  actual_destination=actual_destination,
                  total_amount=total_amount,
                  successful_delivery=successful_delivery,
                  size=size,
                  tax_exempt=tax_exempt)

        print "I am date_of_order", date_of_order
        print "I am date_of_delivery", date_of_delivery
        print "I am requested_destination", requested_destination
        print "I am actual_destination", actual_destination
        print "I am total_amount", total_amount
        print "I am successful_delivery", successful_delivery,
        print "I am size", size
        print "I am tax_exempt", tax_exempt

        db.session.add(giv)
        db.session.commit()

        print "We created a new Giv!"

        flash("You have successfully created a delivery.")

        """Instantiating a new Recipient """
        print "Getting ready to instantiate a new recipient"

        recipient = Recipient.query.order_by('-recipient_id').first()


        print "in recipient for loop"
        address = actual_destination
        print "assigned address to actual_destination"
        address, city, state_zip = address.split(",")
        print "successfully split address, city, state_zip"
        print "This is state_zip", state_zip

        state = state_zip[:-6]
        zipcode = state_zip[-5:]

        print "separated state and zip"

        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=address,+city+state,+zipcode')

        resp_json_payload = response.json()

        print(resp_json_payload['results'][0]['geometry']['location'])

        google_location_dictionary = (resp_json_payload['results'][0]['geometry']['location'])

        latitude = google_location_dictionary["lat"]
        print "I am latitude", latitude

        longitude = google_location_dictionary["lng"]
        print "I am longitude", longitude

        if tax_exempt == True:
            recipient_type = "organization"
        else:
            recipient_type = "individual"

        print "This is recipient_type", recipient_type

        recipient_id = recipient.recipient_id + 1

        recipient = Recipient(recipient_id=recipient_id,
                              address=address,
                              city=city,
                              state=state,
                              zipcode=zipcode,
                              latitude=latitude,
                              longitude=longitude,
                              recipient_type=recipient_type)

        print "This is address, city, state, zipcode", address, city, state, zipcode


        # Flash success message or redirct user
        db.session.add(recipient)
        db.session.commit()

        return render_template("track_order.html", manifest_reference=manifest_reference,
                               fname=fname, tracking_url=tracking_url)

    return render_template("rapid_small_giv.html")

############################################################ NEED TO MAKE THIS A ROUTE ###########################################################

@app.route("/rapid_big_giv", methods=['POST', 'GET'])
def rapid_biggiv():
    """allow user to complete a giv."""

    email = session["email"]
    user = Givr.query.filter_by(email=email).first()
    fname = user.fname
    giv_amount = user.biggiv
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
        print "*****************************closest_restaurant: \n"
        print type(closest_restaurant)
        print closest_restaurant

        best_match_name, best_price_match = find_match_name(closest_restaurant, giv_amount)

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
                            "manifest_reference": random.choice(famous_inventors) + " " + quote_id, #how to auto increment the order number?
                            "pickup_name": closest_restaurant.name,
                            "pickup_address": closest_restaurant.address,
                            "pickup_phone_number": "510-866-4577",
                            "pickup_business_name": closest_restaurant.name,
                            "pickup_notes": pickup_notes,
                            "dropoff_name": "unknown",
                            "dropoff_address": full_address,
                            "dropoff_phone_number": "888-712-9985",
                            "dropoff_business_name": "N/A",
                            "dropoff_notes": dropoff_notes,
                            "requires_id": "false",
                            }
        print "payload_delivery: ", payload_delivery

        #all of this needs updating
        response_from_postmates_delivery = requests.post("https://api.postmates.com/v1/customers/cus_Lk1phJYn_uU88V/deliveries", data=payload_delivery, auth=("a03e8608-cf6b-4441-ade2-696e2c437d6c", ''))
        response_from_postmates_dictionary = response_from_postmates_delivery.json()
        print
        pprint(response_from_postmates_dictionary)
        print

        """Instantiating a new giv """
        print "Getting ready to instantiate a new giv"

        manifest_reference = payload_delivery["manifest_reference"]
        tracking_url = response_from_postmates_dictionary["tracking_url"]
        date_of_order = response_from_postmates_dictionary["created"]
        date_of_delivery = response_from_postmates_dictionary["dropoff_eta"]
        requested_destination = payload_delivery["dropoff_address"]
        actual_destination = payload_delivery["dropoff_address"]
        total_amount = best_price_match
        successful_delivery = True
        # recipient_id =
        size = "big"
        tax_exempt = False
        restaurant = Restaurant.query.filter_by(name=closest_restaurant.name).first()
        print restaurant.restaurant_id

        giv = Giv(givr_id=user.givr_id,
                  restaurant_id=restaurant.restaurant_id,
                  date_of_order=date_of_order,
                  date_of_delivery=date_of_delivery,
                  requested_destination=requested_destination,
                  actual_destination=actual_destination,
                  total_amount=total_amount,
                  successful_delivery=successful_delivery,
                  size=size,
                  tax_exempt=tax_exempt)

        print "I am date_of_order", date_of_order
        print "I am date_of_delivery", date_of_delivery
        print "I am requested_destination", requested_destination
        print "I am actual_destination", actual_destination
        print "I am total_amount", total_amount
        print "I am successful_delivery", successful_delivery,
        print "I am size", size
        print "I am tax_exempt", tax_exempt

        db.session.add(giv)
        db.session.commit()

        print "We created a new Giv!"

        flash("You have successfully created a delivery.")

        """Instantiating a new Recipient """
        print "Getting ready to instantiate a new recipient"

        recipient = Recipient.query.order_by('-recipient_id').first()


        print "in recipient for loop"
        address = actual_destination
        print "assigned address to actual_destination"
        address, city, state_zip = address.split(",")
        print "successfully split address, city, state_zip"
        print "This is state_zip", state_zip

        state = state_zip[:-6]
        zipcode = state_zip[-5:]

        print "separated state and zip"

        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=address,+city+state,+zipcode')

        resp_json_payload = response.json()

        print(resp_json_payload['results'][0]['geometry']['location'])

        google_location_dictionary = (resp_json_payload['results'][0]['geometry']['location'])

        latitude = google_location_dictionary["lat"]
        print "I am latitude", latitude

        longitude = google_location_dictionary["lng"]
        print "I am longitude", longitude

        if tax_exempt == True:
            recipient_type = "organization"
        else:
            recipient_type = "individual"

        print "This is recipient_type", recipient_type

        recipient_id = recipient.recipient_id + 1

        recipient = Recipient(recipient_id=recipient_id,
                              address=address,
                              city=city,
                              state=state,
                              zipcode=zipcode,
                              latitude=latitude,
                              longitude=longitude,
                              recipient_type=recipient_type)

        print "This is address, city, state, zipcode", address, city, state, zipcode

        # Flash success message or redirct user
        db.session.add(recipient)
        db.session.commit()

        return render_template("track_order.html", manifest_reference=manifest_reference,
                               fname=fname, tracking_url=tracking_url)

    return render_template("rapid_biggiv.html")


@app.route('/bar_chart.json')
def bar_chart():
    """Will display the user's giv history over time"""

    email = session["email"]

    user = Givr.query.filter_by(email=email).first()

    # givs = Giv.query.filter_by(givr_id=user.givr_id).all()

    # givs.query.filter(extract('month', ))
    data = []
    months = [1,2,3,4,5,6]
    for month in months:
        givs_amount = Giv.query.filter_by(givr_id=user.givr_id).filter(extract('month', Giv.date_of_delivery)==month).count()
        data.append(int(givs_amount))

    #print data

    data_dict = { "labels": ["January", "February", "March", "April", "May"],
                                  "datasets": [
                                    {
                                      "label": "Your Givs for 2018",
                                      "backgroundColor": ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                                      "data": data
                                    }
                                  ]
                                }
    return jsonify(data_dict)


def find_tax_deductible_givs(user):
    """Will find the total number of tax deductible givs,
      will return the total amount,
      and will find the average amount spent on Givs"""
    correct_tax_deductible_givs()

    email = session["email"]
    user = Givr.query.filter_by(email=email).first()

    givs = Giv.query.filter_by(givr_id=user.givr_id).all()

    all_giv_count = 0
    tax_exempt_givs = 0

    for giv in givs:
        all_giv_count += 1
        if giv.tax_exempt:
            tax_exempt_givs += 1

    return all_giv_count, tax_exempt_givs


@app.route('/giv_donut.json')
def giv_donut():
    """Return data about Melon Sales."""
    correct_tax_deductible_givs()
    email = session["email"]
    user = Givr.query.filter_by(email=email).first()
    all_giv_count, tax_exempt_givs = find_tax_deductible_givs(user)
    # print all_giv_count, tax_exempt_givs
    data_dict = {
                "labels": [
                    "Non Tax Exempt",
                    "Tax Exempt",
                ],
                "datasets": [
                    {
                        "data": [all_giv_count-tax_exempt_givs, tax_exempt_givs],
                        "backgroundColor": [
                            "#20993A",
                            "#D2D4D3",
                        ],
                        "hoverBackgroundColor": [
                            "#1B7F31",
                            "#787A79",
                        ]
                    }]
                }

    return jsonify(data_dict)


def giv_map():
    """ Creates data for a map of SF where the givr has made a giv
    """
    email = session["email"]

    givr = Givr.query.filter_by(email=email).first()

    givs = Giv.query.filter_by(givr_id=givr.givr_id).all()

    givs_distinct = Giv.query.filter_by(givr_id=givr.givr_id).distinct(Giv.actual_destination).all()

    giv_count = Giv.query.filter_by(givr_id=givr.givr_id).count()

    """ Create a dictionary of givs. The key will be the address, and the values will be:
     1) The number of total times GivR has given at that address,
     2) the total amount given at that address
     3) the average amount of Giv for that neighborhood"""

    district_dictionary = { "District 6": [["94103", "94109", "94107"], "South of Market/SOMA, Tenderloin, Treasure Island"],
    "District 5": [["94117"], "Haight Ashbury, Panhandle, Western Addition"],
    "District 3": [["94102", "94108", "94104"], "Russian Hill, Nob Hill, Telegraph Hill, North Beach"]
    }
    """total times given, total amount given, average amount given """

    master_list = []
    district_6_list = [0, 0, 0]
    district_5_list = [0, 0, 0]
    district_3_list = [0, 0, 0]

    print "This is giv_count", giv_count

    for giv in givs:
        actual_destination = getattr(giv, "actual_destination")
        actual_destination = str(actual_destination)
        zipcode = actual_destination[-6:]
        total_amount = getattr(giv, "total_amount")
        for key in district_dictionary:
            district_zipcodes = district_dictionary[key][0]
            for district_zipcode in district_zipcodes:

                if zipcode == district_zipcode:

                    print "I am about to enter district_6_list"
                    if  key in district_dictionary == "District 6":
                        print "in district_6_list"
                        district_6_list[0] += 1
                        district_6_list[1] += total_amount

                    elif key == "District 5":
                        district_5_list[0] += 1
                        district_5_list[1] += total_amount

                    elif key == "District 3":
                        district_3_list[0] += 1
                        district_3_list[1] += total_amount

                    else:
                        print "I am in the else loop."
                        pass
        else:
            pass

    if district_6_list[0] != 0:
        district_6_list[2] = district_6_list[1] / district_6_list[0]

    if district_5_list[0] != 0:
        district_5_list[2] = district_5_list[1] / district_5_list[0]

    if district_3_list[0] != 0:
        district_3_list[2] = district_3_list[1] / district_3_list[0]

    district_6_list.append(district_dictionary["District 6"][1])
    district_5_list.append(district_dictionary["District 5"][1])
    district_3_list.append(district_dictionary["District 3"][1])

    master_list.append(district_6_list)
    master_list.append(district_5_list)
    master_list.append(district_3_list)

    print
    print "This is master list", master_list
    print
    

    return district_dictionary, master_list



@app.route('/giv_history')
def giv_history():
    """ Renders the user;s giv history"""
    correct_tax_deductible_givs()

    # district_dictionary,master_list = giv_map()

    district_dictionary = district_dictionary
    master_list = master_list

    email = session["email"]

    user = Givr.query.filter_by(email=email).first()

    find_tax_deductible_givs(user)

    return render_template("giv_history.html")

    # return render_template("giv_history.html", district_dictionary=district_dictionary,
    #                                            master_list=master_list)


@app.route("/track_order")
def track_order():
    """allow user to track delivery."""

    return render_template("track_order.html")

@app.route("/how_givr_works")
def how_givr_works():
    """allow user to learn about GivR."""

    return render_template("how_Givr_works.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')