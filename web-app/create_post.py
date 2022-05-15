""" create_post.py """
import datetime
import uuid
import os
from flask import  render_template, request, redirect, session, jsonify
import bson
from google.cloud import storage
from global_app import database, datastore_client, CLOUD_STORAGE_BUCKET

# This will be used to prevent users from posting duplicate posts in a row
uuid_current_form = None

def create_post(stand_id):
    """
    Create post for the current stand.

    Parameters:
       - stand_id_1, stand_id_2 = The current stand.
    """

    # wait because session key won't be ready yet
    count = 1000
    while count:
        count -= 1

    # get current user 
    try:
        if not session["usr"]:
            return redirect("/")
    except KeyError:
        return redirect("/")

    stand_obj_id = bson.objectid.ObjectId(stand_id)
    
    # get the current stand from the stand ID
    stand = database.retrieve_single_document("stand", query={"_id": stand_obj_id})
    stand_name = stand["stand_name"]
    return render_template("create_post.html", stand_name = stand_name, stand_id = stand_id,
        uuid_form = str(uuid.uuid1()))

def add_post():
    """
    Add the post to the database.  This gets called from submit of the form

    Parameters:
       - None
    """
    global uuid_current_form

    # wait because session key won't be ready yet
    count = 1000
    while count:
        count -= 1

    # get current user
    # get the current user's email
    try:
        if not session["usr"]:
            return redirect("/")
    except KeyError:
        return redirect("/")

    email = ""

    # get the current user
    ancestor = datastore_client.key("UserId", session["usr"])
    query = datastore_client.query(kind = "visit", ancestor = ancestor)
    user = query.fetch(limit = 1)
    for tempuser in user:
        # if user is not currently in the database, add them - since there is
        # not a sign-up method
        if not database.retrieve_single_document("user", {"email": tempuser["Email"]}):
            database.add_user("user", tempuser["Name"], tempuser["Email"], [])
        email = tempuser["Email"]

    current_user = database.retrieve_single_document("user", {"email": email})

    new_post_filename = ""
    post_file_name_list = []
    if request.files["post_images"].filename:
        for post_image in request.files.getlist("post_images"):
            # Create a Cloud Storage client
            gcs = storage.Client()
            
            # Get the bucket that the file will be uploaded to
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
            
            #Create a new blob and upload the file's content
            blob = bucket.blob(post_image.filename)
            
            blob.upload_from_string(
                post_image.read(),
                content_type = post_image.content_type
            )
            post_file_name_list.append(blob.public_url)

    post_title = request.form.get("PostTitle")
    post_description = request.form.get("post_description")
    stand_id = request.form.get("stand_id")
    post_tags = request.form.get("PostTags")
    current_uuid = request.form.get("uuid_form")

    # if we've seen this uuid before, do not post
    if current_uuid == uuid_current_form:
        return redirect("/view/stand/"+stand_id)
    else:
        # if we haven't, continue, but save it off to prevent duplicate posts
        uuid_current_form = current_uuid

    if post_tags:
        #split on, and trim whitespaces
        post_tags = post_tags.lower()
        post_tag_list = [x.strip() for x in post_tags.lower().split(",")]
    else:
        post_tag_list = []

    stand_obj_id = bson.objectid.ObjectId(stand_id)

    # add a post for the user about
    database.add_post("post", current_user["_id"], stand_obj_id, datetime.datetime.now(),
                      post_title, post_description, post_file_name_list,
                      post_tag_list)

    return redirect("/view/stand/"+stand_id+"/0/5")

def add_post_api():
    """
    Add the post to the database.  This gets called from submit of the form

    Parameters:
       - None
    """

    json_data = request.get_json(force=True)
    email = json_data['Email']

    current_user = database.retrieve_single_document("user", {"email": email})

    post_title = json_data['PostTitle']
    post_description = json_data['post_description']
    stand_id = json_data['stand_id']
    post_tags = json_data['PostTags']

    new_post_filename = ""
    post_file_name_list = []
    '''
    if request.files["post_images"].filename:
        for post_image in request.files.getlist("post_images"):
            # Create a Cloud Storage client
            gcs = storage.Client()
            
            # Get the bucket that the file will be uploaded to
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
            
            #Create a new blob and upload the file's content
            blob = bucket.blob(post_image.filename)
            
            blob.upload_from_string(
                post_image.read(),
                content_type = post_image.content_type
            )
            post_file_name_list.append(blob.public_url)
    '''

    
    if post_tags:
        #split on, and trim whitespaces
        post_tags = post_tags.lower()
        post_tag_list = [x.strip() for x in post_tags.lower().split(",")]
    else:
        post_tag_list = []

    stand_obj_id = bson.objectid.ObjectId(stand_id)

    # add a post for the user about
    database.add_post("post", current_user["_id"], stand_obj_id, datetime.datetime.now(),
                      post_title, post_description, post_file_name_list,
                      post_tag_list)

    return jsonify({'status':"SUCCESS"})
