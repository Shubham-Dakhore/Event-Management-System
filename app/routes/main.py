from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Booking

main = Blueprint('main', __name__)


# =========================
# HOME PAGE
# =========================
@main.route('/')
def home():

    bookings = []

    if current_user.is_authenticated:
        bookings = Booking.query.filter_by(
            user_id=current_user.id
        ).all()

    return render_template("index.html", bookings=bookings)


# =========================
# BOOK EVENT PAGE
# =========================
@main.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():

    if request.method == "POST":

        name = request.form.get("name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        event_type = request.form.get("event_type")
        event_date = request.form.get("event_date")
        plan = request.form.get("plan")
        amount = request.form.get("amount")

        new_booking = Booking(
            name=name,
            address=address,
            phone=phone,
            event_type=event_type,
            event_date=event_date,
            plan=plan,
            amount=amount,
            user_id=current_user.id
        )

        db.session.add(new_booking)
        db.session.commit()

        flash("✅ Event Booked Successfully!", "success")

        return redirect(url_for("main.dashboard"))

    return render_template("booking.html")

@main.route('/delete-booking/<int:id>')
@login_required
def delete_booking(id):

    booking = Booking.query.get_or_404(id)

    # security check
    if booking.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("main.dashboard"))

    db.session.delete(booking)
    db.session.commit()

    flash("Booking deleted successfully!", "success")

    return redirect(url_for("main.dashboard"))



@main.route('/edit-booking/<int:id>', methods=['GET','POST'])
@login_required
def edit_booking(id):

    booking = Booking.query.get_or_404(id)

    if booking.user_id != current_user.id:
        flash("Unauthorized!", "danger")
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":

        booking.name = request.form.get("name")
        booking.address = request.form.get("address")
        booking.phone = request.form.get("phone")
        booking.event_type = request.form.get("event_type")
        booking.event_date = request.form.get("event_date")
        booking.plan = request.form.get("plan")
        booking.amount = request.form.get("amount")

        db.session.commit()

        flash("Booking updated!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("edit_booking.html", booking=booking)



# =========================
# USER DASHBOARD
# =========================
@main.route('/dashboard')
@login_required
def dashboard():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template("dashboard.html", bookings=bookings)


# =========================
# SERVICE PAGES
# =========================
@main.route('/servicecard')
def servicecard():
    return render_template("servicecard.html")


@main.route('/servicepav')
def servicepav():
    return render_template("servicepav.html")