from flask import Blueprint, render_template

services = Blueprint("services", __name__)

@services.route("/servicepav")
def servicepav():
    return render_template("servicepav.html")

@services.route("/servicecard")
def servicecard():
    return render_template("servicecard.html")