"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Giver(db.Model):
    """User of ratings website."""

    __tablename__ = "givers"

    givr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    creditcard_name = db.Column(db.String(50), nullable=False)
    creditcard_exp = db.Column(db.DateTime, nullable=False)
    creditcard_ccv = db.Column(db.Integer, nullable=False)
    alt_choice = db.Column(db.Integer, nullable=False, ForeignKey("alt_choice.alt_choice_id"))
    small_giv_amount = db.Column(db.Integer, nullable=False)
    big_giv_amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<GivR givr_id={} email={} password={} fname={}\
        lname={} creditcard_name={} creditcard_exp={}\
        creditcard_ccv={} alt_choice={} small_giv_amount={}\
        big_giv_amount={}>".format(self.givr_id, self.email,
                                   self.password, self.fname,
                                   self.lname, self.creditcard_name,
                                   self.creditcard_exp, self.creditcard_ccv,
                                   self.alt_choice, self.small_giv_amount,
                                   self.big_giv_amount)

    #Define relationship to alt_choice
    preference = db.relationship("Alt_choice", uselist=False, backref=db.backref("giver"))

    #Define relationship to Givs
    gives = db.relationship("Giv", backref=db.backref("givers", order_by=givr_id))


# Givs Table Class

class Giv(db.Model):
    """User of GivR."""

    __tablename__ = "givs"

    giv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    givr_id = db.Column(db.Integer, ForeignKey("Giv.givr_id"))
    date_of_order = db.Column(db.DateTime, nullable=False)
    time_of_order = db.Colum(db.DateTime, nullable=False)
    date_of_delivery = db.Column(db.DateTime, nullable=False)
    time_of_delivery = db.Column(db.DateTime, nullable=False)
    requested_destination = db.Column(db.String(100), nullable=False)
    actual_destination = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    restaurant = db.Column(db.String(50), nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    tip = db.Column(db.Float, nullable=False)
    successful_delivery = db.Column(db.Boolean, nullable=False)
    recipient_id = db.Column(db.Integer, ForeignKey("Recipient.recipient_id"))
    size = db.Column(db.String(10), nullable=False)
    tax_exempt = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<Giv giv_id={} givr_id={} date_of_order={} time_of_order={}\
        date_of_delivery={} time_of_order={} requested_destination={}\
        actual_destination={} total_amount={} restaurant_used={} subtotal={}\
        tax={} tip={} successful_delivery={} recipient_id={} size={} tax_exempt={}\
        big_giv_amount={}>".format(self.giv_id, self.givr_id, self.date_of_order,
                              self.time_of_order, self.requested_destination)


class Alt_choice(db.Model):
    """A rating of a movie; stored in a database."""

    __tablename__ = "alt_choices"

    alt_choice_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.String(300), nullable=False)

    # @classmethod
    # def get_by_rating_id(cls, rating_id):
    #     """Get a rating from database by ID and return instance."""

    #     QUERY = """SELECT rating_id, movie_id, user_id, score
    #                FROM rating WHERE rating_id = :rating_id"""
    #     cursor = db.session.execute(QUERY, {'rating_id': rating_id})
    #     rating_id, movie_id, user_id, score = cursor.fetchone()
    #     return cls(rating_id, movie_id, user_id, score)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        alternatives = "<Alternate choices alt_choice_id={} description={}>".format(self.alt_choice_id, self.description)


class Recipient(db.Model):
    """User of GivR."""

    __tablename__ = "recipients"

    recipient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(9), nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    recipient_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<Recipient recipient_id={} address={} city={} state={}\
        zipcode={} latitude={} longitude={} recipient_type={}={}".format(self.recipient_id, self.address, self.city,
                                                                  self.zipcode, self.latitude. self.longitude, self.recipient_type)

    #Define relationship to recipients
    give = db.relationship("Giv", backref=db.backref("recipients"), uselist=False)

    #Define relationship to users
    recipient_org = db.relationship("Recipient_org", uselist=False, backref=db.backref("recipient_orgs"))


class Recipient_org(db.Model):
    """User of GivR."""

    __tablename__ = "recipient_orgs"

    org_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipient_id = db.Column(db.Integer, ForeignKey("Recipient.recipient_id"))
    name = db.Column(db.String(200), nullable=False)
    Phone = db.Colum(db.String(14), nullable=False)
    url = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<Recipient Org org_id={} recipient_id={} name={} phone={}\
        url={}".format(self.org_id, self.recipient_id, self.name,
                self.phone, self.url)

    #Define relationship to recipients
    recipient = db.relationship("Recipient", backref=db.backref("recipients", order_by=recipient_id))

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
