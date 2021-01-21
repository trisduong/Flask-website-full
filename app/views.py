from app import app
from flask import render_template
from datetime import datetime
from flask import request, redirect, jsonify, make_response


@app.route("/")
def index():
    return render_template("public/index.html")


@app.route("/about")
def about():
    return render_template("public/about.html")


@app.route("/jinra")
def jinja():
    # Strings
    my_name = "Tri"

    # Integers
    my_age = 23

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description
            self.domain = domain

        def pull(self):
            return "{} Pulling repo".format(self.name)

        def clone(repo):
            return "{} Cloning into".format(repo)

    my_remote = GitRemote(
        name="Learning Flask",
        description="Learn the Flask web framework for python",
        domain="https://github.com"
    )

    def repeat(x, qty=1) -> int:
        return x * qty

    date = datetime.utcnow()
    my_html = "<h1>This is some HTML</h1>"
    suspicious = "<script>alert('NEVER TRUST USER INPUT!')</script>"

    return render_template(
        "public/jinra.html", my_name=my_name, my_age=my_age, langs=langs,
        friends=friends, colors=colors, cool=cool, GitRemote=GitRemote,
        my_remote=my_remote, repeat=repeat, date=date, my_html=my_html,
        suspicious=suspicious
    )


@app.template_filter("clean_date")
def clean_date(date):
    return datetime.strftime(date, "%d %b %Y")


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req = request.form
        missing = list()
        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = "Missing fields for {}".format(*{', '.join(missing)})
            return render_template("public/sign_up.html", feedback=feedback)
        return redirect(request.url)
    return render_template("public/sign_up.html")


@app.route("/profile/<username>")
def profile(username):
    users = {
        "mitsuhiko": {
            "name": "Armin Ronacher",
            "bio": "Creat of of the Flask framework",
            "twitter_handle": "@mitsuhiko"
        },
        "gvanrossum": {
            "name": "Guido Van Rossum",
            "bio": "Creator of the Python programming language",
            "twitter_handle": "@gvanrossum"
        },
        "elonmusk": {
            "name": "Elon Musk",
            "bio": "technology entrepreneur, investor, and engineer",
            "twitter_handle": "@elonmusk"
        }
    }
    if username in users:
        user = users[username]
    return render_template("public/profile.html", username=username, user=user)


@app.route("/multiple/<foo>/<bar>/<baz>")
def multiple(foo, bar, baz):
    print("foo is {}".format(foo))
    print("bar is {}".format(bar))
    print("baz is {}".format(baz))

    return "foo is {}, bar is {}, baz is {}".format(foo, bar, baz)


@app.route("/json", methods=["POST"])
def json_example():
    if request.is_json:
        req = request.get_json()
        response_body = dict(message="JSON received!", sender=req.get("name"))
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():
    req = request.get_json()
    print(req)
    res = make_response(jsonify(req), 200)
    return res
