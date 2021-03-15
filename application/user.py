from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from datetime import date

from application.auth import login_required
from application.db import get_db, get_user, get_user_tours_count, get_user_tours

bp = Blueprint("user", __name__)

@bp.route("/user/")
@bp.route("/user/<int:user_id>")
#@login_required # Siden skal bare være tilgjengelig for inlogget bruker, i test så kan en se forskjellige
def user_index(user_id=-1):
    #user_id = g.user["id"] # Dette er innlogget bruker
    user = get_user(user_id)
    tour_count = get_user_tours_count(user_id,date.today().year)['count_tours']
    # TODO: Legg også til initial_tours hvis brukeren er opprettet i år.
  
    return render_template('user/user_index.html', user=user, tour_count=tour_count)

@bp.route("/user/<int:user_id>/tours/<int:year>")
def user_tours(user_id, year):
    user = get_user(user_id)
    tours = get_user_tours(user_id, date(year,1,1), date(year,12,31))

    #tour_count = get_user_tours_count(user_id,date.today().year)['count_tours']
    #return render_template('user/user_index.html', user=user, tour_count=tour_count)
    return render_template('user/user_tours.html', user=user, tours=tours)

# users.py
@bp.route("/user/<int:user_id>/tours/<int:tour_id>/delete")
#@login_required # Siden skal bare være tilgjengelig for inlogget bruker, i test så kan en se forskjellige
def user_tours_delete(user_id, tour_id):
    flash('Slettet turen')
    # SQL - Delete 
    db = get_db()
    db.execute('delete from tours where id=?', (tour_id,))
    db.commit()
    return redirect(url_for('user.user_index', user_id=user_id))