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
from application.db import get_db, get_top_users

bp = Blueprint("top", __name__)

@bp.route("/top")
@bp.route("/top/<interval>")

def top_index(interval='year'):
    if interval == 'year':
        date_from = date.today().replace(day=1, month=1)
        date_to = date.today()
    elif interval == 'month':
        date_from = date.today().replace(day=1)
        date_to = date.today()
  
    # TODO: Fortsett for måned og uke    
    top_users = get_top_users(date_from, date_to)

    return render_template('top/top_index.html', top_users=top_users, interval=interval)
