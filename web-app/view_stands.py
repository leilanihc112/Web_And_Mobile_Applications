""" view_stands.py """
from ast import Str
from datetime import datetime
from typing import Tuple, List
import codecs
import bson
from flask import render_template, redirect, session, jsonify, request
from global_app import database, datastore_client, DEFAULT_IMAGE_NAME

STANDS_PER_PAGE = 3
POSTS_PER_PAGE = 5


def fetch_all_stands() -> List[dict]:
    """
    Get all stands

    Parameters:
        - None

    Return Value:
        - [pymongo.cursor.Cursor] The query result as a list of the posts on a given stand.
    """
    stands = None
    stands = list(database.retrieve_documents("stand"))

    return stands


def fetch_posts_from_stand(stand: bson.objectid.ObjectId) -> List[dict]:
    """
    Get all posts associated with a stand.

    Parameters:
        - stand [bson.objectid.ObjectId] = ID of the stand to fetch posts from

    Return Value:
        - [pymongo.cursor.Cursor] = The query result as a list of the posts on a given stand.
    """
    posts = None
    posts = list(database.retrieve_documents("post", query={"stand": stand}))

    return posts


def fetch_inventory_from_stand(stand: dict) -> List[str]:
    """
    Get inventory items of a given stand.

    Parameters:
        - stand [bson.objectid.ObjectId] = ID of the stand to fetch inventory from

    Return Value:
        - List[str] = A list of inventory item strings for the given stand
    """
    items = []
    inventory = stand["inventory_list"]

    for inventory_item in inventory:
        item = database.retrieve_single_document("item", query={"_id": inventory_item})
        items.append(item["item_name"])

    return items


def get_all_stand_names(stands: List[dict]) -> List[str]:
    """
    Returns a list of stand names from a list of stands

    Parameters:
        - stands [List[dict]] = List of stands

    Return Value:
        - List[str] = The list of stand names
    """
    stand_names = []

    for stand in stands:
        stand_names.append(stand["stand_name"])

    return stand_names


def get_multi_stand_images(stands: List[dict]) -> List[str]:
    """
    Returns a list of stand images from a list of stands

    Parameters:
        - stands [List[dict]] = List of stands

    Return Value:
        - List[str] = The list of stand image strings
    """
    stand_images = []
    for stand in stands:
        stand_images.append(stand["photo"])

    return stand_images


def get_all_stand_ids(stands: List[dict]) -> List[bson.objectid.ObjectId]:
    """
    Returns a list of values from a list of stands

    Parameters:
        - stands [List[dict]] = List of stands

    Return Value:
        - List[bson.objectid.ObjectId] = The list of stand IDs
    """
    stand_ids = []

    for stand in stands:
        stand_ids.append(stand["_id"])

    return stand_ids


def format_date_time(date_time: datetime) -> str:
    """
    Formats a date and time as DD/MM/YY, HH:MM

    Parameters:
        - date_time [datetime] = Date and time stored in MongDB

    Returns:
        - str = Date and time formatted as a string
    """
    return date_time.strftime("%m/%d/%Y, %H:%M")


def get_all_stand_times(stands: List[dict]) -> List[str]:
    """
    Returns a list of stand open and close time strings from a list of stands

    Parameters:
        - stands [List[dict]] = List of stands

    Return Value:
        - List[str] = The list of strings of times each stand opens and closes
    """
    stand_times = []

    for stand in stands:
        # A time can be properly formatted if there is both open and close date times
        if stand["date_time_open"] is not None and stand["date_time_closed"] is not None:
            open_date_time = format_date_time(stand["date_time_open"])
            close_date_time = format_date_time(stand["date_time_closed"])
            stand_times.append(open_date_time + " - " + close_date_time)
        else:
            stand_times.append("N/A")

    return stand_times


def get_all_stand_locations(stands: List[dict]) -> List[str]:
    """
    Returns a list of stand location strings from a list of stands

    Parameters:
        - stands [List[dict]] = List of stands

    Return Value:
        - [List[str]] = The list of strings of locations of each stand
    """
    stand_locations = []

    for stand in stands:
        location = stand["location"]
        if location is None:
            stand_locations.append("N/A")
        else:
            stand_locations.append("(" + str(location[0]) + ", " + str(location[1]) + ")")

    return stand_locations


def fetch_next_set_of_posts(posts: List[dict], first_index: int, last_index: int) -> \
        Tuple[List[dict], bool, bool]:
    """
    Get the next set of posts to display, limited by POSTS_PER_PAGE.

    Parameters:
        - posts [List] = List of all posts
        - first_index [int] = First index to grab of the posts to display.
        - last_index [int] = Last index to grab of the posts to display.

    Return Value:
        - [tuple of list of dicts, bool, bool]
            - The query result containing <= POSTS_PER_PAGE posts at the indexes given
            - Whether there are previous posts in the query.
            - Whether there are more posts in the query.
    """
    prev_post_link = False
    next_post_link = False
    posts_list = []
    first_index_adj = first_index
    last_index_adj = last_index

    # if first index is less than 0, fix it to be 0
    first_index_adj = max(first_index_adj, 0)

    # make the first index to be the last post if it is past the end
    if first_index_adj >= len(posts):
        first_index_adj = (len(posts) - 1) - ((len(posts) - 1) % POSTS_PER_PAGE)

    if last_index_adj > len(posts):
        last_index_adj = len(posts)

    # if more than POSTS_PER_PAGE, force last index to be POSTS_PER_PAGE more from first index
    if last_index_adj - first_index_adj > POSTS_PER_PAGE:
        last_index_adj = first_index_adj + POSTS_PER_PAGE

    # if at least one post returned
    if posts:
        if first_index_adj > (len(posts) - 1):
            first_index_adj = len(posts) - 1
            last_index_adj = len(posts)
        if last_index_adj > len(posts):
            last_index_adj = len(posts)
        # if at least POSTS_PER_PAGE stands returned
        if len(posts) >= POSTS_PER_PAGE:
            # if we are at the end of the list and less than POSTS_PER_PAGE stands remain
            if first_index_adj > (len(posts) - POSTS_PER_PAGE):
                # make the last index to be the last stand. do not pass the end of the list
                last_index_adj = len(posts)
            # if there are previous stands in the list
            if first_index_adj > 0:
                prev_post_link = True
            # if there are more stands in the list, indicate to show the next
            if last_index_adj < len(posts):
                next_post_link = True
        # if less than POSTS_PER_PAGE stands
        else:
            # make the last index to be the last stand. do not pass the end of the list
            last_index_adj = len(posts)
        if first_index != first_index_adj or last_index != last_index_adj:
            return posts_list, prev_post_link, next_post_link
        # get only the amount of docs we want
        for idx in range(first_index_adj, last_index_adj):
            posts_list.append(posts[idx])
    else:
        first_index_adj = 0
        last_index_adj = 0

    return posts_list, prev_post_link, next_post_link


def fetch_next_set_of_stands(stands: List[dict], first_index: int, last_index: int) -> \
        Tuple[List[dict], bool, bool]:
    """
    Get the next set of stands to display, limited by STANDS_PER_PAGE.

    Parameters:
        - stands [List] = List of all stands
        - first_index [int] = First index to grab of the stands to display.
        - last_index [int] = Last index to grab of the stands to display.

    Return Value:
        - [tuple of list of dicts, bool, bool]
            - The query result containing <= STANDS_PER_PAGE stands at the indexes given
            - Whether there are previous stands in the query.
            - Whether there are more stands in the query.
    """
    prev_stand_link = False
    next_stand_link = False
    stands_list = []
    first_index_adj = first_index
    last_index_adj = last_index

    # if first index is less than 0, fix it to be 0
    first_index_adj = max(first_index_adj, 0)

    # make the first index to be the last stand if it is past the end
    if first_index_adj >= len(stands):
        first_index_adj = (len(stands) - 1) - ((len(stands) - 1) % STANDS_PER_PAGE)

    if last_index_adj > len(stands):
        last_index_adj = len(stands)

    # if more than STANDS_PER_PAGE, force last index to be STANDS_PER_PAGE more from first index
    if last_index_adj - first_index_adj > STANDS_PER_PAGE:
        last_index_adj = first_index_adj + STANDS_PER_PAGE

    # if at least one stand returned
    if stands:
        if first_index_adj > (len(stands) - 1):
            first_index_adj = len(stands) - 1
            last_index_adj = len(stands)
        if last_index_adj > len(stands):
            last_index_adj = len(stands)
        # if at least STANDS_PER_PAGE stands returned
        if len(stands) >= STANDS_PER_PAGE:
            # if we are at the end of the list and less than STANDS_PER_PAGE stands remain
            if first_index_adj > (len(stands) - STANDS_PER_PAGE):
                # make the last index to be the last stand. do not pass the end of the list
                last_index_adj = len(stands)
            # if there are previous stands in the list
            if first_index_adj > 0:
                prev_stand_link = True
            # if there are more stands in the list, indicate to show the next
            if last_index_adj < len(stands):
                next_stand_link = True
        # if less than STANDS_PER_PAGE stands
        else:
            # make the last index to be the last stand. do not pass the end of the list
            last_index_adj = len(stands)
        if first_index != first_index_adj or last_index != last_index_adj:
            return stands_list, prev_stand_link, next_stand_link
        # get only the amount of docs we want
        for idx in range(first_index_adj, last_index_adj):
            stands_list.append(stands[idx])
    else:
        first_index_adj = 0
        last_index_adj = 0

    return stands_list, prev_stand_link, next_stand_link


def view_all_stands(stand_first_index: str, stand_second_index: str):
    """
    Gets information about the stands to display on the view all stands page
    from a stand at stand_first_index to stand_second_index and renders a template

    Parameters:
        - stand_first_index [str] = Index of the first stand to display
        - stand_first_index [str] = Index of the last stand to display

    Returns:
        - A rendered template
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

    stand_first_index_int = int(stand_first_index)
    stand_second_index_int = int(stand_second_index)
    all_stands = fetch_all_stands()
    all_stand_count = len(all_stands)
    stand_second_index_int = min(stand_second_index_int, all_stand_count)
    all_stand_names = get_all_stand_names(all_stands)
    all_stand_ids = get_all_stand_ids(all_stands)
    all_stand_times = get_all_stand_times(all_stands)
    all_stand_locations = get_all_stand_locations(all_stands)
    stands_to_display, prev_stands_link, next_stands_link = \
        fetch_next_set_of_stands(all_stands, stand_first_index_int, stand_second_index_int)
    stand_list_count = len(stands_to_display)
    all_stand_names = get_all_stand_names(stands_to_display)
    all_stand_ids = get_all_stand_ids(stands_to_display)
    all_stand_images = get_multi_stand_images(stands_to_display)
    all_stand_times = get_all_stand_times(stands_to_display)
    all_stand_locations = get_all_stand_locations(stands_to_display)

    return render_template("view-all-stands.html",
                           all_stand_count=all_stand_count,
                           all_stand_names=all_stand_names,
                           all_stand_ids=all_stand_ids,
                           all_stand_times=all_stand_times,
                           all_stand_locations=all_stand_locations,
                           all_stand_images=all_stand_images,
                           first_stand_index=stand_first_index_int,
                           last_stand_index=stand_second_index_int,
                           prev_stands_link=prev_stands_link, next_stands_link=next_stands_link,
                           stand_list_count=stand_list_count, max_stands_per_page=STANDS_PER_PAGE,
                           max_posts_per_page=POSTS_PER_PAGE)

def view_all_stands_api():
    """
    Gets information about the stands to display on the view all stands page
    from a stand at stand_first_index to stand_second_index and renders a template

    Parameters:
        - stand_first_index [str] = Index of the first stand to display
        - stand_first_index [str] = Index of the last stand to display

    Returns:
        - A rendered template
    """

    all_stands = fetch_all_stands()
    all_stand_count = len(all_stands)
    all_stand_names = get_all_stand_names(all_stands)
    all_stand_ids = get_all_stand_ids(all_stands)
    all_stand_times = get_all_stand_times(all_stands)
    all_stand_locations = get_all_stand_locations(all_stands)
    stand_list_count = len(all_stands)
    all_stand_names = get_all_stand_names(all_stands)
    all_stand_ids = get_all_stand_ids(all_stands)
    all_stand_images = get_multi_stand_images(all_stands)
    all_stand_times = get_all_stand_times(all_stands)
    all_stand_locations = get_all_stand_locations(all_stands)

    return jsonify({'all_stand_count':all_stand_count,
                           'all_stand_names':all_stand_names,
                           'all_stand_ids':all_stand_ids,
                           'all_stand_times':all_stand_times,
                           'all_stand_locations':all_stand_locations,
                           'all_stand_images':all_stand_images,
                           'stand_list_count':stand_list_count, 'max_stands_per_page':STANDS_PER_PAGE,
                           'max_posts_per_page':POSTS_PER_PAGE})
    


def view_stand(stand_id: str, post_first_index: str, post_second_index: str):
    """
    Gets information about a stand to display on the view stand page from a stand id
    and renders a template

    Parameters:
        - stand_id [str] = ID of the stand to get information from
        - post_first_index [str] = Index of first post to display
        - post_second_index [str] = Index of last post to display

    Returns:
        - A rendered template
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
    stand = database.retrieve_single_document("stand", query={"_id": stand_obj_id})
    stand_name = stand["stand_name"]
    location = stand["location"]

    # Retrieve a photo for the stand
    image_name = stand["photo"]

    # Retrieve information about the stand
    time = format_date_time(stand["date_time_open"]) + " - " \
                            + format_date_time(stand["date_time_closed"])
    creator = database.retrieve_single_document("user", query={"_id": stand["user"]})["username"]
    inventory_list = fetch_inventory_from_stand(stand)
    posts = list(database.retrieve_documents("post", query={"stand": stand_obj_id}))
    post_count = len(posts)
    post_first_index_int = int(post_first_index)
    post_second_index_int = int(post_second_index)
    post_second_index_int = min(post_second_index_int, post_count)
    posts_to_display, prev_post_link, next_post_link = \
        fetch_next_set_of_posts(posts, post_first_index_int, post_second_index_int)
    posts_display_count = len(posts_to_display)
    post_users = []
    post_hours = []
    post_image_names = []
    post_image_count = []
    user_is_subscribed = is_user_subscribed(stand_id, get_user_email())

    # Retrieve information about all the posts on a stand
    for post in posts_to_display:
        post_users.append(database.retrieve_single_document
                          ("user", query={"_id": post["user"]})["username"])
        post_hours.append(format_date_time(post["timestamp"]))
        post_images = []
        for photo in post["photos"]:
            post_images.append(photo)
        post_image_names.append(post_images)
        post_image_count.append(len(post_images))

    return render_template("view-stand.html", stand_name=stand_name, stand_id=stand_id,
                           location=location, time=time, creator=creator, \
                           inventory_list=inventory_list, post_count=post_count, posts=posts, \
                           posts_to_display=posts_to_display, \
                           posts_display_count=posts_display_count, \
                           post_users=post_users, post_hours=post_hours, \
                           post_image_names=post_image_names, post_image_count=post_image_count, \
                           first_post_index=post_first_index_int,
                           last_post_index=post_second_index_int,
                           image_name=image_name, user_is_subscribed=user_is_subscribed, \
                           prev_post_link=prev_post_link, next_post_link=next_post_link, \
                           max_per_page=POSTS_PER_PAGE)

def view_stand_api(stand_id: str):
    """
    Gets information about a stand to display on the view stand page from a stand id
    and renders a template
    Parameters:
        - stand_id [str] = ID of the stand to get information from
        - post_first_index [str] = Index of first post to display
        - post_second_index [str] = Index of last post to display
    Returns:
        - A rendered template
    """
    json_data = request.get_json(force=True)
    email = json_data['Email']

    stand_obj_id = bson.objectid.ObjectId(stand_id)
    stand = database.retrieve_single_document("stand", query={"_id": stand_obj_id})
    stand_name = stand["stand_name"]
    location = stand["location"]

    # Retrieve a photo for the stand
    image_name = stand["photo"]

    # Retrieve information about the stand
    time = format_date_time(stand["date_time_open"]) + " - " \
                            + format_date_time(stand["date_time_closed"])
    creator = database.retrieve_single_document("user", query={"_id": stand["user"]})["username"]
    inventory_list = fetch_inventory_from_stand(stand)
    posts = list(database.retrieve_documents("post", query={"stand": stand_obj_id}))
    post_count = len(posts)
    post_users = []
    post_hours = []
    post_image_names = []
    post_image_count = []
    user_is_subscribed = is_user_subscribed(stand_id, email)

    posts_list = []
    for i in range(0, post_count):
        posts_list.append(posts[i])

    # Retrieve information about all the posts on a stand
    for post in posts_list:
        post_users.append(database.retrieve_single_document
                          ("user", query={"_id": post["user"]})["username"])
        post_hours.append(format_date_time(post["timestamp"]))
        post_images = []
        for photo in post["photos"]:
            post_images.append(photo)
        post_image_names.append(post_images)
        post_image_count.append(len(post_images))
    
    return jsonify({'stand_name':stand_name, 'stand_id':stand_id,
                           'location':location, 'time':time, 'creator':creator, \
                           'inventory_list':inventory_list, 'post_count':post_count, 'posts':posts, \
                           'post_users':post_users, 'post_hours':post_hours, \
                           'post_image_names':post_image_names, 'post_image_count':post_image_count, \
                           'image_name':image_name, 'isSub':user_is_subscribed,\
                           'max_per_page':POSTS_PER_PAGE})


def is_user_subscribed(stand_id: str, user_email: str) -> bool:
    """
    Checks if a user is subscribed to a stand.

    Parameters:
        - stand_id [str] = The ID of a stand.
        - user_email [str] = The email of a user to search for.

    Returns:
        - bool = Whether a user is subscribed
    """
    is_subscribed = False
    user = database.retrieve_single_document("user", query = { "email": user_email })
    if user["subscribed_stands"]:
        sub_list = user["subscribed_stands"]
        if sub_list:
            if bson.objectid.ObjectId(stand_id) in sub_list:
                is_subscribed = True

    return is_subscribed

def is_user_subscribed_api(stand_id: str):
    """
    Checks if a user is subscribed to a stand.

    Parameters:
        - stand_id [str] = The ID of a stand.
    """

    is_subscribed = False

    json_data = request.get_json(force=True)
    email = json_data['Email']

    user = database.retrieve_single_document("user", query = { "email": email })
    
    if user["subscribed_stands"]:
        sub_list = user["subscribed_stands"]
        
        if sub_list:
            if bson.objectid.ObjectId(stand_id) in sub_list:
                is_subscribed = True


    return jsonify({'isSub':is_subscribed})


def get_user_email() -> str:
    """
    Gets the email of the current user.

    Parameters:
        - None

    Returns:
        - The email of the user currently logged in
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

    return email


def subscribe(stand_id: str, post_first_index: str, post_second_index: str):
    """
    Subscribe the current user to the associated stand.

    Parameters:
        - stand_id [str] = The ID of the stand to subscribe the user to.
        - post_first_index [str] = Index of first post to display
        - post_second_index [str] = Index of last post to display
    """

    email = get_user_email()
    if email:
        len_before = 0
        user = database.retrieve_single_document("user", query={"email": email})
        # If the user has subscribed to at least one stand
        if user["subscribed_stands"]:
            len_before = len(user["subscribed_stands"])
            len_after = len_before
            sub_list = user["subscribed_stands"].copy()
            if bson.objectid.ObjectId(stand_id) not in sub_list:
                sub_list.append(bson.objectid.ObjectId(stand_id))
                len_after = len_before + 1
        else:
            # Add this stand as the first one in the subscribed list
            sub_list = [bson.objectid.ObjectId(stand_id)]
            len_after = 1
        if len_before < len_after:
            database.update_documents("user", {"subscribed_stands": sub_list}, \
                                      {"email": email})

    return redirect("/view/stand/" + stand_id + '/' + post_first_index + '/' + post_second_index)


def stand_unsubscribe(stand_id: str, post_first_index: str, post_second_index: str):
    """
    Unsubscribe the current user from the associated stand.

    Parameters:
        - stand_id [str] = The ID of the stand to unsubscribe the user from.
        - post_first_index [str] = Index of first post to display
        - post_second_index [str] = Index of last post to display
    """

    email = get_user_email()

    if email:
        user = database.retrieve_single_document("user", query={"email": email})
        if user["subscribed_stands"]:
            # Check the user's subscribed stands list for the stand to unsubscribe from
            sub_list = user["subscribed_stands"].copy()
            len_before = len(sub_list)
            len_after = len_before
            if bson.objectid.ObjectId(stand_id) in sub_list:
                sub_list.remove(bson.objectid.ObjectId(stand_id))
                len_after = len(sub_list)
            if len_before > len_after:
                database.update_documents("user", {"subscribed_stands": sub_list}, \
                                          {"email": email})
        else:
            # The user's subscribed_stands list is empty, cannot unsubscribe
            raise Exception

    return redirect("/view/stand/" + stand_id + '/' + post_first_index + '/' + post_second_index)

def subscribe_api(stand_id: str):
    """
    Subscribe the current user to the associated stand.

    Parameters:
        - stand_id [str] = The ID of the stand to subscribe the user to.
        - post_first_index [str] = Index of first post to display
        - post_second_index [str] = Index of last post to display
    """
    json_data = request.get_json(force=True)
    email = json_data['Email']
    
    if email:
        len_before = 0
        user = database.retrieve_single_document("user", query={"email": email})
        # If the user has subscribed to at least one stand
        if user["subscribed_stands"]:
            len_before = len(user["subscribed_stands"])
            len_after = len_before
            sub_list = user["subscribed_stands"].copy()
            if bson.objectid.ObjectId(stand_id) not in sub_list:
                sub_list.append(bson.objectid.ObjectId(stand_id))
                len_after = len_before + 1
        else:
            # Add this stand as the first one in the subscribed list
            sub_list = [bson.objectid.ObjectId(stand_id)]
            len_after = 1
        if len_before < len_after:
            database.update_documents("user", {"subscribed_stands": sub_list}, \
                                      {"email": email})
    
    return jsonify({'status':"SUCCESS"})


def stand_unsubscribe_api(stand_id: str):
    """
    Unsubscribe the current user from the associated stand.

    Parameters:
        - stand_id [str] = The ID of the stand to unsubscribe the user from.
        - post_first_index [str] = Index of first post to display
        - post_second_index [str] = Index of last post to display
    """

    json_data = request.get_json(force=True)
    email = json_data['Email']

    if email:
        user = database.retrieve_single_document("user", query={"email": email})
        if user["subscribed_stands"]:
            # Check the user's subscribed stands list for the stand to unsubscribe from
            sub_list = user["subscribed_stands"].copy()
            len_before = len(sub_list)
            len_after = len_before
            if bson.objectid.ObjectId(stand_id) in sub_list:
                sub_list.remove(bson.objectid.ObjectId(stand_id))
                len_after = len(sub_list)
            if len_before > len_after:
                database.update_documents("user", {"subscribed_stands": sub_list}, \
                                          {"email": email})
        else:
            # The user's subscribed_stands list is empty, cannot unsubscribe
            raise Exception
            return jsonify({'status':"ERROR"})

    return jsonify({'status':"SUCCESS"})
