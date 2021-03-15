from datetime import date
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from application.auth import login_required
from application.db import get_db, get_user, get_user_tours_count, get_top_users, get_tours_latest, insert_tour

bp = Blueprint("index", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    tour_count = 0
    if g.user:
        user = get_user(g.user['id'])
        tour_count = get_user_tours_count(g.user['id'],date.today().year)['count_tours']

    if request.method == "POST":
        tour_date = request.form["tour_date"] # Henter ut verdien
        insert_tour(g.user['id'], tour_date)
        
        flash('Tur registrert!')
    
        # TODO: Så må en lagre dette i tabellen, med innlogget bruker
        # TODO: Mulig ta en til egen side når en har registrert turen?

    # TODO: Må vise antall turer i år mm. 
    date_from = date.today().replace(day=1, month=1)
    date_to = date.today()
    # TODO: Fortsett for måned og uke    
    top_users = get_top_users(date_from, date_to)
    latest_tours = get_tours_latest()
    today=date.today()

    return render_template("index.html", **locals())


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
