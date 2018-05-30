"""Utility file to seed Givr database from seed_recipients and seed_recipient_orgs data in seed_data/"""

from sqlalchemy import func
from model import Givr, Recipient, Recipient_org, Alt_choice, Restaurant, Item
from datetime import datetime

from model import connect_to_db, db
from server import app
from dateutil import parser


def load_alt_choice():
    """Load alt_choice from seed_alt_choices into database."""

    print "Alternative Choices"

    Alt_choice.query.delete()

    for row in open("seed/seed_alt_choices.txt"):

        row = row.rstrip()
        alt_choice_id, description = row.split("|")

        recipient_org = Alt_choice(alt_choice_id=alt_choice_id,
                                   description=description)

        db.session.add(recipient_org)

    db.session.commit()


def load_givrs():
    """Load users from u.user into database."""

    print "Givrs"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Givr.query.delete()

    # Read u.user file and insert data
    for row in open("seed/seed_givrs"):
        row = row.rstrip()
        (givr_id, email, password, fname, lname, creditcardname, creditcardnum,
         creditcardexp, creditcardccv, smallgiv, biggiv, alt_choice_id) = row.split("|")

        # creditcardexp = datetime.strptime(creditcardexp, "%m/%y")
        creditcardexp = datetime.strptime(creditcardexp, "%m/%y").strftime("%Y-%m-%d")

        givr = Givr(
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname,
                    creditcardname=creditcardname,
                    creditcardnum=creditcardnum,
                    creditcardexp=creditcardexp,
                    creditcardccv=creditcardccv,
                    smallgiv=smallgiv,
                    biggiv=biggiv,
                    alt_choice_id=alt_choice_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(givr)

    # Once we're done, we should commit our work
    db.session.commit()


def load_recipients():
    """Load recipients from seed_recipients into database."""

    print "Recipients"

    Recipient.query.delete()

    for row in open("seed/seed_recipients.txt"):

        row = row.rstrip()
        recipient_id, address, city, state, zipcode, latitude, longitude, recipient_type = row.split("|")

        recipient = Recipient(recipient_id=recipient_id,
                              address=address,
                              city=city,
                              state=state,
                              zipcode=zipcode,
                              latitude=latitude,
                              longitude=longitude,
                              recipient_type=recipient_type)

        db.session.add(recipient)

    db.session.commit()


def load_restaurants():
    """Load restaurants from seed_restaurants into database."""

    print "Restaurants"

    Restaurant.query.delete()

    for row in open("seed/seed_restaurants.txt"):

        row = row.rstrip()
        restaurant_id, name, address, delivery_fee = row.split("|")

        restaurant = Restaurant(restaurant_id=restaurant_id,
                              name=name,
                              address=address,
                              delivery_fee=delivery_fee)

        db.session.add(restaurant)

    db.session.commit()


def load_items():
    """ Load Items from seed_items into database"""

    print "Items"

    Item.query.delete()

    for row in open("seed/seed_items.txt"):

        row = row.rstrip()
        item_id, restaurant_id, name, price = row.split("|")

        item = Item(item_id=item_id, restaurant_id=restaurant_id, name=name, price=price)

        db.session.add(item)

    db.session.commit()

def load_recipient_orgs():
    """Load recipient_orgs from seed_recipient_orgs into database."""

    print "Recipient_orgs"

    Recipient_org.query.delete()

    for row in open("seed/seed_recipient_orgs.txt"):

        row = row.rstrip()
        org_id, recipient_id, name, phone, url = row.split("|")

        recipient_org = Recipient_org(org_id=org_id,
                                      recipient_id=recipient_id,
                                      name=name,
                                      phone=phone,
                                      url=url)

        db.session.add(recipient_org)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_alt_choice()
    load_givrs()
    load_restaurants()
    load_items()
    load_recipients()
    load_recipient_orgs()
