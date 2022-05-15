""" management.py """
from typing import Tuple, List
import codecs
from flask import render_template, request, redirect, session, jsonify
from bson import ObjectId
from global_app import database, datastore_client, DEFAULT_IMAGE_NAME
import view_stands

POSTS_PER_PAGE = 5


def fetch_subscribed_stands(email: str, first_index: int, last_index: int) -> \
Tuple[List[dict], bool, bool, List[dict]]:
    """
    Get 3 stands the current user is subscribed to.

    Parameters:
        - email [str] = Email of the user to search for.
        - first_index [int] = First index to grab of the stands the user is subscribed to. If
            a negative number is passed in, then this will be changed to 0.
        - last_index [int] = Last index to grab of the stands the user is subscribed to. Must be
            3 more than the first_index (or less). If it is more, it will be changed to be 3 more
            than the first index.

    Return Value:
        - [tuple of list of dicts, bool, bool, list of dicts]
            - The query result containing 3 (or less) stands at the indexes given that the user is
              subscribed to.
            - Whether there are previous stands in the query.
            - Whether there are more stands in the query.
            - The images associated with each of the 3 (or less) stands.
    """
    prev_stand_link = False
    next_stand_link = False
    stands_list = []
    stand_images = []
    first_index_adj = first_index
    last_index_adj = last_index

    # get document of user that was passed in
    user = database.retrieve_single_document("user", query={ "email": email })

    if user:
        # get the stands associated with the user
        stands = list(database.retrieve_documents("stand", query={ "_id": { "$in":
            user["subscribed_stands"] } }))

        # if first index is less than 0, fix it to be 0
        first_index_adj = max(first_index_adj, 0)

        # if at least one stand returned
        if stands:
            # make the first index to be the last stand if it is past the end
            if first_index_adj >= len(stands):
                first_index_adj = (len(stands) - 1) - ((len(stands) - 1) % 3)
            else:
                # since we show in 3s, this will fix if the last stand was unsubscribed to
                # but it was the only one on that page, for example
                first_index_adj = first_index_adj - (first_index_adj % 3)

            # if more than 3, force last index to be 3 more from first index
            if (last_index_adj - first_index_adj) > 3:
                last_index_adj = first_index_adj + 3

            if first_index_adj > (len(stands) - 1):
                first_index_adj = len(stands) - 1
                last_index_adj = len(stands)
            if last_index_adj > len(stands):
                last_index_adj = len(stands)
            # if at least 3 stands returned
            if len(stands) >= 3:
                # if we are at the end of the list and less than 3 stands remain
                if first_index_adj > (len(stands) - 3):
                    # make the last index to be the last stand. do not pass the end of the list
                    last_index_adj = len(stands)
                # if there are previous stands in the list
                if first_index_adj > 0:
                    prev_stand_link = True
                # if there are more stands in the list, indicate to show the next
                if last_index_adj < len(stands):
                    next_stand_link = True
            # if less than 3 stands
            else:
                # make the last index to be the last stand. do not pass the end of the list
                last_index_adj = len(stands)

            # get only the amount of docs we want
            stands_list = stands[first_index_adj:last_index_adj]

            # get the images
            for doc in stands_list:
                stand_images.append(doc["photo"])
        else:
            first_index_adj = 0
            last_index_adj = 0

    return stands_list, prev_stand_link, next_stand_link, stand_images


def fetch_post(email: str, first_index: int) -> Tuple[dict, bool, str, bool, bool, str]:
    """
    Get 1 post created by the current user and the image of the stand associated with it.

    Parameters:
        - email [str] = Email of the user to search for.
        - first_index [int] = The index of the posts the user has made to grab.

    Return Value:
        - [tuple of dict, bool, str, bool, bool, str]
            - The query result of 1 post created by the user at the index given.
            - Whether the stand associated with the post exists.
            - The name of the stand the post was made on.
            - Whether there are previous posts in the query.
            - Whether there are more posts in the query.
            - The image that is associated with the stand the post was made on.
    """
    prev_post_link = False
    next_post_link = False
    post = None
    stand_name = ""
    stand_image = None
    stand_exist = False

    # get the user passed in
    user = database.retrieve_single_document("user", query={ "email": email })

    if user:
        # get all posts this user has made
        post = list(database.retrieve_documents("post", query={ "user": user["_id"] }))

        # if there is at least 1 post made by the current user
        if post:
            # if there are previous posts, indicate to show the prev button
            if first_index > 0:
                prev_post_link = True
            # if there are more posts, indicate to show the next button
            if first_index < (len(post) - 1):
                next_post_link = True
            # the requested post doesn't exist, redirect
            if first_index != 0 and first_index > (len(post) - 1):
                first_index = len(post) - 1
                return post, stand_exist, stand_name, prev_post_link, next_post_link, \
                stand_image
            # get post at index indicated
            post = database.retrieve_documents("post", query={ "user": user["_id"] },
                first_index=first_index)
            # get stand associated with the post so that we can get the name and image
            stand = database.retrieve_single_document("stand", query={ "_id": post["stand"] })
            # stand must exist
            if stand:
                stand_exist = True
                # get the name of the stand
                stand_name = stand["stand_name"]
                # get the image of the stand
                stand_image = stand["photo"]
            else:
                stand_exist = False
                prev_post_link = False
                next_post_link = False
                stand_name = ""
                stand_image = None

    return post, stand_exist, stand_name, prev_post_link, next_post_link, stand_image


def management_main():
    """
    Generate the HTML for the management page.

    Parameters:
        - None.

    Return value:
        - The return of Flask's render_html method.
    """
    # if there isn't a stand, then redo the first part of the function without
    # redirecting
    redo_loop = True

    while redo_loop:
        if request.method == "GET":
            # wait because session key won't be ready yet
            count = 1000
            while count:
                count -= 1

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
            for us_i in user:
                # if user is not currently in the database, add them - since there is
                # not a sign-up method
                if not database.retrieve_single_document("user", {"email": us_i["Email"]}):
                    database.add_user("user", us_i["Name"], us_i["Email"], [])
                email = us_i["Email"]

            try:
                # get the current indexes to look at
                post_index = int(request.args.get("post_index"))
                stand_first_index = int(request.args.get("stand_first_index"))
                stand_second_index = int(request.args.get("stand_second_index"))
            except ValueError:
                post_index = 0
                stand_first_index = 0
                stand_second_index = 3

            stands_html = []
            stands_id_html = []
            post_link = False
            time_stamp_string = []

            # get a post the user has made, the name of the stand for that post,
            # indicate whether to show the previous and next buttons, and get the image for
            # the stand for this post
            first_post, stand_flag, stand_name, prev_post_link, next_post_link, stand_image = \
            fetch_post(email, post_index)
            if not first_post:
                first_post = [{ "title": "", "text": "" }]
                redo_loop = False
            # if there are posts made by this user
            else:
                # there is no stand - the post is not valid
                if not stand_flag:
                    database.delete_posts("post", {"_id": first_post["_id"]})
                else:
                    # indicate to show the post
                    post_link = True
                    # get the time stamp of the post, and format it to Month Day, Year
                    time_stamp_string = first_post["timestamp"].strftime("%B %d, %Y")
                    redo_loop = False

        # get the stands the user has subscribed to
        stands, prev_stands_link, next_stands_link, stands_images = \
        fetch_subscribed_stands(email, stand_first_index, stand_second_index)

        # if the user has subscribed to at least 1 stand
        if stands:
            # get the name and id of the stands
            for doc in stands:
                stands_html.append(doc["stand_name"])
                stands_id_html.append(str(doc["_id"]))
            num_stands = len(stands)
        # else if there no stands
        else:
            num_stands = 0
            stands_html = [""] * 3
            stands_images = [""] * 3
            stands_id_html = [""] * 3

        # render html
        return render_template("management.html", stand_name = stand_name,
                stand_image = stand_image, post = first_post, post_timestamp = time_stamp_string,
                post_index = post_index, first_stand_index = stand_first_index,
                last_stand_index = stand_second_index,
                stands_name = stands_html, stands_photo = stands_images,
                stands_id = stands_id_html, prev_stands_link = prev_stands_link,
                next_stands_link = next_stands_link,
                prev_post_link = prev_post_link, next_post_link = next_post_link,
                post_link = post_link, num_stands = num_stands, max_posts_per_page = POSTS_PER_PAGE)


def unsubscribe(stand_id: str, post_index: str, stand_first_index: str,
stand_second_index: str):
    """
    Unsubscribe the current user from the associated stand.

    Parameters:
        - stand_id [str] = The ID of the stand to unsubscribe the user from.
        - post_index [str] = Index of the user's posts to grab.
        - stand_first_index [str] = First index of the user's subscribed stands to grab.
        - stand_second_index [str] = Second index of the user's subscribed stands to grab.
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

    email = ""

    # get the current user
    ancestor = datastore_client.key("UserId", session["usr"])
    query = datastore_client.query(kind = "visit", ancestor = ancestor)
    user = query.fetch(limit = 1)
    for us_i in user:
        email = us_i["Email"]

    user = database.retrieve_single_document("user", query = { "email": email })
    # save length of list
    len_before = len(user["subscribed_stands"])
    # remove stand to unsubscribe from the list
    if user["subscribed_stands"]:
        sub_list = user["subscribed_stands"].copy()
    else:
        sub_list = []
    if ObjectId(stand_id) in sub_list:
        sub_list.remove(ObjectId(stand_id))
    # length of list after
    len_after = len(sub_list)

    if len_after == len_before:
        raise Exception
    else:
        database.update_documents("user", { "subscribed_stands": sub_list },
            { "email": email })
    return redirect("/management/?post_index=" + post_index + "/&stand_first_index=" +
        stand_first_index + "/&stand_second_index=" + stand_second_index)

def management_api():
    json_data = request.get_json(force=True)
    email = json_data['Email']

    # get document of user that was passed in
    user = database.retrieve_single_document("user", query={ "email": email })
    # posts = []
    stand_count = 0
    stand_names = []
    stand_ids = []
    stand_times = []
    stand_locations = []
    stand_images = []

    if user:
        # get the stands associated with the user
        stands = list(database.retrieve_documents("stand", query={ "_id": { "$in":
            user["subscribed_stands"] } }))

        stand_count = len(stands)
        stand_names = view_stands.get_all_stand_names(stands)
        stand_ids = view_stands.get_all_stand_ids(stands)
        stand_times = view_stands.get_all_stand_times(stands)
        stand_locations = view_stands.get_all_stand_locations(stands)
        stand_images = view_stands.get_multi_stand_images(stands)
        # get all posts this user has made
        # posts = list(database.retrieve_documents("post", query={ "user": user["_id"] }))
    else:
        return jsonify({'status':"ERROR"})
        
    return jsonify({'stand_count':stand_count,
                           'stand_names':stand_names,
                           'stand_ids':stand_ids,
                           'stand_times':stand_times,
                           'stand_locations':stand_locations,
                           'stand_images':stand_images,
                           'stand_count':stand_count})