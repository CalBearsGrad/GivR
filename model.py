"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Givr(db.Model):
    """User of ratings website."""

    __tablename__ = "givrs"

    givr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    creditcardtype = db.Column(db.String, nullable=False)
    creditcardname = db.Column(db.String(50), nullable=False)
    creditcardnum = db.Column(db.String(16), nullable=False)
    creditcardexp = db.Column(db.DateTime, nullable=False)
    creditcardccv = db.Column(db.Integer, nullable=False)
    smallgiv = db.Column(db.Integer, nullable=False)
    biggiv = db.Column(db.Integer, nullable=False)
    alt_choice_id = db.Column(db.Integer, db.ForeignKey("alt_choices.alt_choice_id"))


    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<GivR givr_id={} email={} password={} fname={}\
        lname={} creditcardtype={} creditcardname={} creditcardnum={} creditcardexp={}\
        creditcardccv={} smallgiv={}\
        biggiv={} alt_choice_id={}>".format(self.givr_id, self.email,
                                   self.password, self.fname,
                                   self.lname, self.creditcardtype, self.creditcardname,
                                   self.creditcardnum,
                                   self.creditcardexp, self.creditcardccv,
                                   self.smallgiv,
                                   self.biggiv, self.alt_choice_id)

    #Define relationship to alt_choice
    preference = db.relationship("Alt_choice", uselist=False, backref=db.backref("givr"))


# Givs Table Class

class Giv(db.Model):
    """User of GivR."""

    __tablename__ = "givs"

    giv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    givr_id = db.Column(db.Integer, db.ForeignKey("givrs.givr_id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"))
    date_of_order = db.Column(db.DateTime, nullable=False)
    date_of_delivery = db.Column(db.DateTime, nullable=True)
    requested_destination = db.Column(db.String(100), nullable=False)
    actual_destination = db.Column(db.String(100), nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    restaurant = db.Column(db.String(50), nullable=False)
    successful_delivery = db.Column(db.Boolean, nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("recipients.recipient_id"))
    size = db.Column(db.String(10), nullable=False)
    tax_exempt = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<Giv giv_id={} givr_id={} restaurant_id={} date_of_order={}\
        date_of_order={} date_of_delivery={} requested_destination={}\
        actual_destination={} total_amount={} restaurant={}\
        successful_delivery={} recipient_id={} size={} tax_exempt={}>".format(self.giv_id,
                                                                              self.givr_id,
                                                                              self.date_of_order,
                                                                              self.date_of_delivery,
                                                                              self.requested_destination,
                                                                              self.actual_destination,
                                                                              self.total_amount,
                                                                              self.restaurant,
                                                                              self.successful_delivery,
                                                                              self.recipient_id,
                                                                              self.size,
                                                                              self.tax_exempt)

    #Define relationship to Givs
    giver = db.relationship("Givr", backref=db.backref("givs", order_by=givr_id))
    restaurant = db.relationship("Restaurant", backref=db.backref("givs", order_by=restaurant_id))


class Restaurant(db.Model):
    """List of Restaurants."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    delivery_fee = db.Column(db.Float, nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<Restaurant restaurant_id={} name={} address={}\
        delivery_fee={}>".format(self.restaurant_id, self.name, self.address, self.delivery_fee)

class Item(db.Model):
    """List of Items."""

    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"))
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<Item item_id={} restaurant_id={} name={} price={}>".format(self.item_id ,self.restaurant_id ,self.name ,self.price)

    #backre relationship to the restaurants table
    restaurants = db.relationship("Restaurant", backref=db.backref("items", order_by=restaurant_id))

class Alt_choice(db.Model):
    """A rating of a movie; stored in a database."""

    __tablename__ = "alt_choices"

    alt_choice_id = db.Column(db.Integer, primary_key=True)
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
    recipient_id = db.Column(db.Integer, db.ForeignKey("recipients.recipient_id"))
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(14), nullable=False)
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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///givr'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
