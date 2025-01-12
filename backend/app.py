from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from datetime import datetime
from config import ApplicationConfig
from models import db, User, Therapist, Reservation

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

db.init_app(app)

app.config["SESSION_SQLALCHEMY"] = db  
server_session = Session()
server_session.init_app(app)  

with app.app_context():
    db.create_all()

# Endpoint to get the currently logged-in user's information
@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
     
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 

# Endpoint to register a new user with provided details
@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)

    new_user = User(
        email=email,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name
    )
    db.session.add(new_user)
    db.session.commit()
    
    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name
    })

# Endpoint to log in a user by verifying their email and password
@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })

# Endpoint to log out the currently logged-in user
@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id", None)
    return "200"

# Endpoint to get detailed information about the logged-in user and their visits
@app.route("/user_info", methods=["GET"])
def user_info():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    reservations = Reservation.query.filter_by(user_id=user_id).all()

    sorted_reservations = sorted(
        reservations,
        key=lambda res: (
            res.date,
            datetime.strptime(res.time_slot.split(" - ")[0], "%H:%M")
        )
    )

    visits = [
        {
            "id": reservation.id,
            "date": reservation.date.strftime("%Y-%m-%d"),
            "time_slot": reservation.time_slot,
            "therapist": {
                "id": reservation.therapist.id,
                "first_name": reservation.therapist.first_name,
                "last_name": reservation.therapist.last_name,
                "specialization": reservation.therapist.specialization,
            },
        }
        for reservation in sorted_reservations
    ]

    return jsonify({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "visits": visits,
    })

# Endpoint to get a list of all therapists and their details
@app.route("/therapists", methods=["GET"])
def get_therapists():
    therapists = Therapist.query.all()
    result = [
        {
            "id": therapist.id,
            "first_name": therapist.first_name,
            "last_name": therapist.last_name,
            "specialization": therapist.specialization,
            "rating": therapist.rating,
        }
        for therapist in therapists
    ]
    return jsonify(result), 200

# Endpoint to get detailed information about a specific therapist by ID
@app.route("/therapist/<int:id>", methods=["GET"])
def get_therapist(id):

    therapist = Therapist.query.get(id)
    if not therapist:
        return jsonify({"error": "Therapist not found"}), 404

    result = {
        "id": therapist.id,
        "first_name": therapist.first_name,
        "last_name": therapist.last_name,
        "specialization": therapist.specialization,
        "rating": therapist.rating,
        "biography": therapist.biography,
        "contact_email": therapist.contact_email,
        "time_slots": therapist.time_slots,
    }
    return jsonify(result), 200

# Endpoint to get available time slots for a specific therapist on a given date
@app.route("/therapist/<int:id>/available-times", methods=["GET"])
def get_available_times(id):
    from datetime import datetime

    date_str = request.args.get("date")

    if not date_str:
        return jsonify({"error": "Missing required 'date' parameter"}), 400
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    therapist = Therapist.query.get(id)
    if not therapist:
        return jsonify({"error": "Therapist not found"}), 404

    reserved_times = [
        reservation.time_slot for reservation in Reservation.query.filter_by(
            therapist_id=id, date=date
        ).all()
    ]

    available_times = [
        time for time in therapist.time_slots if time not in reserved_times
    ]

    today = datetime.today().date()
    if date == today:
        current_hour = datetime.now().hour
        available_times = [
            time for time in available_times if int(time.split(":")[0]) > current_hour
        ]

    return jsonify({"available_times": available_times}), 200

# Endpoint to create a new booking for a therapist on a specific date and time
@app.route("/booking", methods=["POST"])
def create_booking():

    data = request.get_json()
    user_id = data.get("user_id")
    therapist_id = data.get("therapist_id")
    date = data.get("date")
    time_slot = data.get("time_slot")

    if not user_id or not therapist_id or not date or not time_slot:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    existing_reservation = Reservation.query.filter_by(
        therapist_id=therapist_id,
        date=date,
        time_slot=time_slot
    ).first()

    if existing_reservation:
        return jsonify({"error": "This time slot is already booked."}), 409

    new_reservation = Reservation(
        user_id=user_id,
        therapist_id=therapist_id,
        date=date,
        time_slot=time_slot,
    )
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({"message": "Reservation created successfully"}), 201

# Endpoint to delete a reservation for the logged-in user by reservation ID
@app.route("/delete_reservation/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    reservation = Reservation.query.filter_by(id=reservation_id, user_id=user_id).first()

    if not reservation:
        return jsonify({"error": "Reservation not found or not authorized"}), 404

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({"message": "Reservation deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
