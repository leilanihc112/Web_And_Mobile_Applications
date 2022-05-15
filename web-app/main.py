""" main.py """
import sys
from flask import render_template, redirect, request, make_response, session, url_for, jsonify
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
from global_app import app, datastore_client
import management
import create_stand
import view_stands
import create_post
import search_posts
from bson.json_util import ObjectId
import json
from datetime import date

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, date):
                return obj.isoformat()
        return super(MyEncoder, self).default(obj)

app.json_encoder = MyEncoder

# All app routes blueprints
app.add_url_rule("/management/", methods=["GET"], view_func = management.management_main)
app.add_url_rule("/management/unsubscribe/<stand_id>/" +
    "<post_index>/<stand_first_index>/<stand_second_index>/",
    view_func = management.unsubscribe)
app.add_url_rule("/create_stand/", view_func = create_stand.create_stand)
app.add_url_rule("/create_stand/", methods=["POST"], view_func = create_stand.add_stand)
app.add_url_rule("/view/stand/<stand_id>/", view_func = view_stands.view_stand)
app.add_url_rule("/view/stand/<stand_id>/subscribe/<post_first_index>/<post_second_index>/", view_func = view_stands.subscribe)
app.add_url_rule("/view/stand/<stand_id>/unsubscribe/<post_first_index>/<post_second_index>/", view_func = view_stands.stand_unsubscribe)
app.add_url_rule("/view/stand/<stand_id>/<post_first_index>/<post_second_index>/", view_func = view_stands.view_stand)
app.add_url_rule("/view_all_stands/<stand_first_index>/<stand_second_index>/",
    view_func = view_stands.view_all_stands)
app.add_url_rule("/create_post/<stand_id>", view_func = create_post.create_post)
app.add_url_rule("/add_post/", methods=["POST"], view_func = create_post.add_post)
app.add_url_rule("/search/", view_func = search_posts.search_posts)
app.add_url_rule("/search/<search_string>/", view_func = search_posts.search_posts_tags)
app.add_url_rule("/search/<search_string>/<search_first_index>/<search_second_index>/",
    view_func = search_posts.search_posts_tags_index)

# API START #

# Management
app.add_url_rule("/api/management/", methods=["POST"], view_func = management.management_api)

# Create Stand 
app.add_url_rule("/api/create_stand/", methods=["POST"], view_func = create_stand.add_stand_api)

# Create Post
app.add_url_rule("/api/add_post/", methods=["POST"], view_func = create_post.add_post_api)

# View
app.add_url_rule("/api/view/stand/<stand_id>/subscribe/", methods=["POST"], view_func = view_stands.subscribe_api)
app.add_url_rule("/api/view/stand/<stand_id>/unsubscribe/", methods=["POST"], view_func = view_stands.stand_unsubscribe_api)
app.add_url_rule("/api/view/stand/<stand_id>/", methods=["POST"], view_func = view_stands.view_stand_api)
app.add_url_rule("/api/view_all_stands/",
    view_func = view_stands.view_all_stands_api)

# Search
app.add_url_rule("/api/search/<search_string>/", view_func = search_posts.search_posts_tags_api)
app.add_url_rule("/api/search/<search_string>/<search_first_index>/<search_second_index>/",
    view_func = search_posts.search_posts_tags_index_api)

# API END #

# Firebase 
firebase_request_adapter = requests.Request()

@app.route("/")
def login():
    """ Main page """
    id_token = request.cookies.get("token")
    error_message = None
    claims = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token( \
                id_token, firebase_request_adapter)
            entity = datastore.Entity(key = datastore_client.key("UserId", claims["sub"], \
                "visit"))
            entity.update({
                "Name": claims["name"],
                "Email": claims["email"]
            })
            session["usr"] = claims["sub"]
            # add user to datastore
            datastore_client.put(entity)
            # redirect to management if the user is logged in
            return redirect(url_for("management_main", post_index=0, stand_first_index=0, \
                stand_second_index=3))
        except ValueError as exc:
            error_message = str(exc)
            print(error_message, file = sys.stderr)

    return render_template("login.html")

@app.route("/logout/")
def logout():
    """ Logout page """
    id_token = request.cookies.get("token")
    session["usr"] = ""
    resp = make_response(redirect("/"))

    # delete cookies so it doesn't automatically redirect to home page
    if id_token:
        resp.set_cookie("token", id_token, expires = 0)

    return resp

@app.errorhandler(Exception)
def handle_error(error):
    """ Exceptions will be routed here """
    print(error, file = sys.stderr)
    return render_template("error.html")

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
