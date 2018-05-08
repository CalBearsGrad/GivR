"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

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
                                   self.password, self.fname
                                   self.lname, self.creditcard_name,
                                   self.creditcard_exp, self.creditcard_ccv,
                                   self.alt_choice, self.small_giv_amount,
                                   self.big_giv_amount)

    #Define relationship to alt_choice
    preference = db.relationship("Alt_choice", backref=db.backref("alt_choice", order_by=alt_choice_id))


# Givs Table Class

class Giv(db.Model):
    """User of GivR."""

    __tablename__ = "givs"

    giv_id = db.Column(db.Integer, autoincrement=True primary_key=True)
    givr_id = db.Column(db.Integer, ForeignKey("Giv.givr_id"))
    date_of_order = db.Column(db.DateTime, nullable=False)
    time_of_order = db.Colum(db.DateTime, nullable=False)
    date_of_delivery= db.Column(db.DateTime, nullable=False)
    time_of_delivery = db.Column(db.DateTime nullable=False)
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
                            self.time_of_order, self.requested_destination
                            )

    #Define relationship to alt_choice
    preference = db.relationship("Alt_choice", backref=db.backref("alt_choice", order_by=alt_choice_id))


class Rating(db.Model):
    """A rating of a movie; stored in a database."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    #Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings", order_by=rating_id))

    #Define relationship to movie
    movie = db.relationship("Movie", backref=db.backref("ratings", order_by=rating_id))

    @classmethod
    def get_by_rating_id(cls, rating_id):
        """Get a rating from database by ID and return instance."""

        QUERY = """SELECT rating_id, movie_id, user_id, score
                   FROM rating WHERE rating_id = :rating_id"""
        cursor = db.session.execute(QUERY, {'rating_id': rating_id})
        rating_id, movie_id, user_id, score = cursor.fetchone()
        return cls(rating_id, movie_id, user_id, score)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        s = "<rating_id={} movie_id={} user_id={} score={}>".format(self.rating_id, self.movie_id, self.user_id, self.score)

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
