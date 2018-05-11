"""Utility file to seed Givr database from seed_recipients and seed_recipient_orgs data in seed_data/"""

from sqlalchemy import func
from model import Givr
from model import Recipient
from model import Recipient_org
from model import Alt_choice

from model import connect_to_db, db
from server import app
from dateutil import parser


def load_alt_choice():
    """Load alt_choice from seed_alt_choices into database."""

    print "Alternative Choices"

    Alt_choice.query.delete()

    for row in open("seed_alt_choices"):

        row = row.rstrip()
        alt_choice_id, description = row.split("|")

        recipient_org = Recipient_org(alt_choice_id=alt_choice_id,
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
    for row in open("seed_givrs"):
        row = row.rstrip()
        givr_id, email, password, fname, lname, creditcard_name, creditcard_num,
        creditcard_exp, creditcard_ccv, alt_choice, small_giv_amount, big_giv_amount = row.split("|")

        givr = Givr(givr_id=givr_id,
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname,
                    creditcard_name=creditcard_name,
                    creditcard_num=creditcard_num,
                    creditcard_exp=creditcard_exp,
                    creditcard_ccv=creditcard_ccv,
                    alt_choice=alt_choice,
                    small_giv_amount=small_giv_amount,
                    big_giv_amount=big_giv_amount)

        # We need to add to the session or it won't ever be stored
        db.session.add(givr)

    # Once we're done, we should commit our work
    db.session.commit()


def load_recipients():
    """Load recipients from seed_recipients into database."""

    print "Recipients"

    Recipient.query.delete()

    for row in open("seed_recipients"):

        row = row.rstrip()
        recipient_id, address, latitude, longitude, recipient_type = row.split("|")

        recipient = Recipient(recipient_id=recipient_id,
                              address=address,
                              latitude=latitude,
                              longitude=longitude,
                              recipient_type=recipient_type)

        db.session.add(recipient)

    db.session.commit()


def load_recipient_orgs():
    """Load recipient_orgs from seed_recipient_orgs into database."""

    print "Recipient_orgs"

    Recipient_org.query.delete()

    for row in open("seed_recipient_orgs"):

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
    load_recipients()
    load_recipient_orgs
    set_val_user_id()