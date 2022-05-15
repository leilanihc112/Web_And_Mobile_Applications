""" search_posts.py """
from datetime import datetime
import codecs
from flask import render_template, session, redirect, jsonify
import bson
from global_app import database, DEFAULT_IMAGE_NAME

def format_date_time(date_time: datetime) -> str:
    """
    Formats a date and time as DD/MM/YY, HH:MM.

    Parameters:
        - date_time [datetime] = Date and time stored in MongoDB.

    Returns:
        - [str] = Date and time formatted as a string.
    """
    return date_time.strftime("%m/%d/%Y, %H:%M")

def search_posts():
    """
    Show search edit box and start the process of search.

    Parameters:
       - None
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

    # if we get here, there has been no tag searched
    post_count = 0

    return render_template("search.html",
                           post_count=post_count,
                           current_value="",
                           max_per_page=10)

def search_posts_tags(search_string: str):
    """
    Show search box and start the process of search.

    Parameters:
       - search_string [str] = The tag to search for.
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

    current_value = search_string

    # get each of the tags and save to a list, strip whitespace
    search_string_list = [x.strip() for x in search_string.split(",")]
    # grab the posts that contain these tags
    posts = list(database.retrieve_documents("post", query={"tags" : {"$in":search_string_list}}))
    post_count = len(posts)
    post_users = []
    post_hours = []
    post_stands_names = []
    post_image_names = []
    post_image_count = []
    stand_ids = []
    prev_button_link = False

    # for each post, grab the stand information associated with it
    for post in posts:
        post_users.append(database.retrieve_single_document("user",
        query={"_id": post["user"]})["username"])
        stand_obj_id = bson.objectid.ObjectId(post["stand"])
        stand = database.retrieve_single_document("stand", query={"_id": stand_obj_id})
        # if there is no stand, show that it could not be found
        if stand is None:
            stand_name = "Unknown?"
            stand_ids.append(stand_obj_id)
        else:
            stand_name = stand["stand_name"]
            stand_ids.append(stand["_id"])

        # grab all of the post information
        post_stands_names.append(stand_name)

        post_hours.append(format_date_time(post["timestamp"]))
        post_images = []
        # grab the photos in the post, if there are any
        for photo in post["photos"]:
            post_images.append(photo)
        post_image_names.append(post_images)
        post_image_count.append(len(post_images))

    next_button_link = False
    search_second_index = post_count
    if post_count >= 10:
        search_second_index = 10
        next_button_link = True

    return render_template("search.html",
                           post_count=post_count, posts=posts, post_users=post_users,
                           post_hours=post_hours, post_image_names=post_image_names,
                           post_image_count=post_image_count,
                           post_stands_names = post_stands_names, stand_ids = stand_ids,
                           current_value = current_value,
                           search_first_index = 0,
                           search_second_index = search_second_index,
                           max_per_page=10, prev_button_link=prev_button_link,
                           next_button_link=next_button_link,
                           search_first_index_plus = 1)


def search_posts_tags_index(search_string: str, search_first_index: str, search_second_index: str):
    """
    Limit html page rendering to a range of index.

    Parameters:
       search_string [str] = The tag to search for.
       search_first_index [str] = First post index to display.
       search_second_index [str] = Last post index to display.
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

    current_value = search_string

    # get each of the tags and save to a list, strip whitespace
    search_string_list = [x.strip() for x in search_string.split(",")]
    # grab the posts that contain these tags
    posts = list(database.retrieve_documents("post", query={"tags" : {"$in":search_string_list}}))
    post_count = len(posts)

    # grab the current index from the passed in variables
    search_first_index_int = int(search_first_index)
    search_second_index_int = int(search_second_index)

    # if the indexes are out of the acceptable bounds
    if search_first_index_int < 0 or search_first_index_int > post_count:
        search_first_index_int = 0
    if search_second_index_int < search_first_index_int:
        search_second_index_int = search_first_index_int + 10

    search_second_index_int = min(search_second_index_int, post_count)
    search_first_index = search_first_index_int
    search_second_index = search_second_index_int

    post_users = []
    post_hours = []
    post_stands_names = []
    post_image_names = []
    post_image_count = []
    stand_ids = []

    # only show previous and next button when appropriate
    prev_button_link = True
    if search_first_index_int == 0:
        prev_button_link = False

    next_button_link = True
    if search_second_index_int >= post_count:
        next_button_link = False

    # for each post, grab the stand information associated with it
    for post in posts:
        post_users.append(database.retrieve_single_document("user",
        query={"_id": post["user"]})["username"])
        stand_obj_id = bson.objectid.ObjectId(post["stand"])
        stand = database.retrieve_single_document("stand", query={"_id": stand_obj_id})
        # if there is no stand, show that it could not be found
        if stand is None:
            stand_name = "Unknown?"
            stand_ids.append(stand_obj_id)
        else:
            stand_name = stand["stand_name"]
            stand_ids.append(stand["_id"])

        # grab all of the post information
        post_stands_names.append(stand_name)

        post_hours.append(format_date_time(post["timestamp"]))\
        # grab the photos in the post, if there are any
        post_images = []
        for photo in post["photos"]:
            post_images.append(photo)
        post_image_names.append(post_images)
        post_image_count.append(len(post_images))

    return render_template("search.html",
                           post_count=post_count, posts=posts, post_users=post_users,
                           post_hours=post_hours, post_image_names=post_image_names,
                           post_image_count=post_image_count,
                           post_stands_names = post_stands_names, stand_ids = stand_ids,
                           current_value = current_value,
                           search_first_index = search_first_index_int,
                           search_second_index = search_second_index_int,
                           max_per_page=10, prev_button_link=prev_button_link,
                           next_button_link=next_button_link,
                           search_first_index_plus = search_first_index_int+1)

def search_posts_tags_api(search_string: str):
    """
    Show search box and start the process of search.

    Parameters:
       - search_string [str] = The tag to search for.
    """

    current_value = search_string

    # get each of the tags and save to a list, strip whitespace
    search_string_list = [x.strip() for x in search_string.split(",")]
    # grab the posts that contain these tags
    posts = list(database.retrieve_documents("post", query={"tags" : {"$in":search_string_list}}))
    post_count = len(posts)
    post_users = []
    post_hours = []
    post_stands_names = []
    post_image_names = []
    post_image_count = []
    stand_ids = []
    prev_button_link = False

     # for each post, grab the stand information associated with it
    for post in posts:
        post_users.append(database.retrieve_single_document("user",
        query={"_id": post["user"]})["username"])
        stand_obj_id = bson.objectid.ObjectId(post["stand"])
        stand = database.retrieve_single_document("stand", query={"_id": stand_obj_id})
        # if there is no stand, show that it could not be found
        if stand is None:
            stand_name = "Unknown?"
            stand_ids.append(stand_obj_id)
        else:
            stand_name = stand["stand_name"]
            stand_ids.append(stand["_id"])

        # grab all of the post information
        post_stands_names.append(stand_name)

        post_hours.append(format_date_time(post["timestamp"]))
        post_images = []
        # grab the photos in the post, if there are any
        for photo in post["photos"]:
            post_images.append(photo)
        post_image_names.append(post_images)
        post_image_count.append(len(post_images))

    next_button_link = False
    search_second_index = post_count
    if post_count >= 10:
        search_second_index = 10
        next_button_link = True

    return jsonify({'post_count':post_count, 'posts':posts, 'post_users':post_users,
                           'post_hours':post_hours, 'post_image_names':post_image_names,
                           'post_image_count':post_image_count,
                           'post_stands_names':post_stands_names, 'stand_ids':stand_ids,
                           'current_value':current_value,
                           'search_first_index':0,
                           'search_second_index':search_second_index,
                           'max_per_page':10, 'prev_button_link':prev_button_link,
                           'next_button_link':next_button_link,
                           'search_first_index_plus':1})


def search_posts_tags_index_api(search_string: str, search_first_index: str, search_second_index: str):
    """
    Limit html page rendering to a range of index.

    Parameters:
       search_string [str] = The tag to search for.
       search_first_index [str] = First post index to display.
       search_second_index [str] = Last post index to display.
    """
    # wait because session key won't be ready yet
    count = 1000
    while count:
        count -= 1

    current_value = search_string

    # get each of the tags and save to a list, strip whitespace
    search_string_list = [x.strip() for x in search_string.split(",")]
    # grab the posts that contain these tags
    posts = list(database.retrieve_documents("post", query={"tags" : {"$in":search_string_list}}))
    post_count = len(posts)

    # grab the current index from the passed in variables
    search_first_index_int = int(search_first_index)
    search_second_index_int = int(search_second_index)

    # if the indexes are out of the acceptable bounds
    if search_first_index_int < 0 or search_first_index_int > post_count:
        search_first_index_int = 0
    if search_second_index_int < search_first_index_int:
        search_second_index_int = search_first_index_int + 10

    search_second_index_int = min(search_second_index_int, post_count)
    search_first_index = search_first_index_int
    search_second_index = search_second_index_int

    post_users = []
    post_hours = []
    post_stands_names = []
    post_image_names = []
    post_image_count = []
    stand_ids = []

    # only show previous and next button when appropriate
    prev_button_link = True
    if search_first_index_int == 0:
        prev_button_link = False

    next_button_link = True
    if search_second_index_int >= post_count:
        next_button_link = False

    # for each post, grab the stand information associated with it
    for post in posts:
        post_users.append(database.retrieve_single_document("user",
        query={"_id": post["user"]})["username"])
        stand_obj_id = bson.objectid.ObjectId(post["stand"])
        stand = database.retrieve_single_document("stand", query={"_id": stand_obj_id})
        # if there is no stand, show that it could not be found
        if stand is None:
            stand_name = "Unknown?"
            stand_ids.append(stand_obj_id)
        else:
            stand_name = stand["stand_name"]
            stand_ids.append(stand["_id"])

        # grab all of the post information
        post_stands_names.append(stand_name)

        post_hours.append(format_date_time(post["timestamp"]))\
        # grab the photos in the post, if there are any
        post_images = []
        for photo in post["photos"]:
            post_images.append(photo)
        post_image_names.append(post_images)
        post_image_count.append(len(post_images))

    
    return jsonify({'post_count':post_count, 'posts':posts, 'post_users':post_users,
                           'post_hours':post_hours, 'post_image_names':post_image_names,
                           'post_image_count':post_image_count,
                           'post_stands_names':post_stands_names, 'stand_ids':stand_ids,
                           'current_value':current_value,
                           'search_first_index':search_first_index_int,
                           'search_second_index':search_second_index_int,
                           'max_per_page':10, 'prev_button_link':prev_button_link,
                           'next_button_link':next_button_link,
                           'search_first_index_plus':search_first_index_int+1})
