""" create_stand.py """
import datetime
import uuid
from flask import render_template, request, redirect, session, jsonify
from google.cloud import storage
from global_app import database, datastore_client, app, os, DEFAULT_IMAGE_NAME, CLOUD_STORAGE_BUCKET

app.secret_key = os.urandom(24)

def create_stand():
    """
    Generate HTML for the Create Stand page.

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

    return render_template("createStand.html", hidden_value1 = "none", hidden_value2 = "none",
    hidden_value3 = "none", hidden_value4 = "none", hidden_value5 = "none", hidden_value6 = "none",
    hidden_value7 = "none", alert = False, show_val = False)

def add_stand():
    """
    Add New Stand to the Database.

    Parameters:
        - None
    """
    if request.method == "POST":
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

        # Get information from createStand.html
        stand_name = request.form["StandName"]
        latitude = request.form["Latitude"]
        longitude = request.form["Longitude"]
        inventory = request.form["Inventory"]
        open_date = request.form["OpenDate"]
        close_date = request.form["CloseDate"]

        if not stand_name:
            return render_template("createStand.html", hidden_value1 = "none",
            hidden_value2 = "none", hidden_value3 = "none", hidden_value4 = "none",
            hidden_value5 = "inline", hidden_value6 = "none",
            hidden_value7 = "none", alert = False, show_val = True)

        # Check if latitude and longitude are valid
        try:
            latitude = float(latitude)

            if latitude > 90 or latitude < -90:
                raise ValueError

        except ValueError:
            return render_template("createStand.html", hidden_value1 = "inline",
            hidden_value2 = "none", hidden_value3 = "none", hidden_value4 = "none",
            hidden_value5 = "none", hidden_value6 = "none",
            hidden_value7 = "none", alert = False, show_val = True)

        try:
            longitude = float(longitude)

            if longitude > 180 or longitude < -180:
                raise ValueError

        except ValueError:
            return render_template("createStand.html", hidden_value1 = "none",
            hidden_value2 = "inline", hidden_value3 = "none", hidden_value4 = "none",
            hidden_value5 = "none", hidden_value6 = "none",
            hidden_value7 = "none", alert = False, show_val = True)

        # Parse date
        opened = ""
        close = ""

        try:
            opened = datetime.datetime.strptime(open_date, "%Y-%m-%dT%H:%M")
        except ValueError:
            return render_template("createStand.html", hidden_value1 = "none",
            hidden_value2 = "none", hidden_value3 = "inline", hidden_value4 = "none",
            hidden_value5 = "none", hidden_value6 = "none",
            hidden_value7 = "none", alert = False, show_val = True)

        try:
            close = datetime.datetime.strptime(close_date, "%Y-%m-%dT%H:%M")
        except ValueError:
            return render_template("createStand.html", hidden_value1 = "none",
            hidden_value2 = "none", hidden_value3 = "none", hidden_value4 = "inline",
            hidden_value5 = "none", hidden_value6 = "none",
            hidden_value7 = "none", alert = False, show_val = True)

        if opened >= close:
            return render_template("createStand.html", hidden_value1 = "none",
            hidden_value2 = "none", hidden_value3 = "none", hidden_value4 = "none",
            hidden_value5 = "none", hidden_value6 = "inline",
            hidden_value7 = "none", alert = False, show_val = True)

        # Parse inventory
        inventory_list = [x.strip() for x in inventory.split(",")]
        items_list = []

        for i in inventory_list:
            # Check if item exist before adding
            item = database.retrieve_single_document("item", query={"item_name": i})

            if item is None:
                database.add_item("item", i, False)
                item = database.retrieve_single_document("item", query={"item_name": i})
                items_list.append(item["_id"])
            else:
                items_list.append(item["_id"])

        # get the current user's email
        email = ""
        # get the current user
        ancestor = datastore_client.key("UserId", session["usr"])
        query = datastore_client.query(kind = "visit", ancestor = ancestor)
        user = query.fetch(limit = 1)
        for us_i in user:
            email = us_i["Email"]

        current_user = database.retrieve_single_document("user", {"email": email})

        # Get image
        stand_image_name = ""

        if request.files["img"].filename:
            # give the file a unique name since this is what we will be using to find it
            stand_image = request.files["img"]
            
            # Create a Cloud Storage client
            gcs = storage.Client()
            
            # Get the bucket that the file will be uploaded to
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
            
            #Create a new blob and upload the file's content
            blob = bucket.blob(stand_image.filename)
            
            blob.upload_from_string(
                stand_image.read(),
                content_type = stand_image.content_type
            )
            
        else:
            stand_image_name = DEFAULT_IMAGE_NAME

        tuple_location = (latitude, longitude)

        # check if theres a duplicate
        duplicate = list(database.retrieve_documents("stand", query = {"stand_name" : stand_name,
        "location": tuple_location, "date_time_open": opened, "date_time_closed": close}))
        if duplicate:
            # There is a duplicate - show error
            return render_template("createStand.html", hidden_value1 = "none",
            hidden_value2 = "none", hidden_value3 = "none", hidden_value4 = "none",
            hidden_value5 = "none", hidden_value6 = "none",
            hidden_value7 = "inline", alert = False, show_val = True)

        database.add_stand("stand", stand_name, items_list, current_user["_id"],
                           blob.public_url, tuple_location, opened, close)

        return render_template("createStand.html", hidden_value1 = "none",
        hidden_value2 = "none", hidden_value3 = "none", hidden_value4 = "none",
        hidden_value5 = "none", hidden_value6 = "none",
        hidden_value7 = "none", alert = True, show_val = False)

    return render_template("createStand.html", hidden_value1 = "none",
    hidden_value2 = "none", hidden_value3 = "none", hidden_value4 = "none",
    hidden_value5 = "none", hidden_value6 = "none",
    hidden_value7 = "none", alert = False, show_val = False)

def add_stand_api():
    """
    Add New Stand to the Database.

    Parameters:
        - None
    """
    if request.method == "POST":
        # Get information from createStand.html
        json_data = request.get_json(force=True)
        stand_name = json_data['StandName']
        latitude = json_data['Latitude']
        longitude = json_data['Longitude']
        inventory = json_data['Inventory']
        open_date = json_data['OpenDate']
        close_date = json_data['CloseDate']
        #stand_image = json_data['img']

        if not stand_name:
            return jsonify({'status':"ERROR"})

        # Check if latitude and longitude are valid
        try:
            latitude = float(latitude)

            if latitude > 90 or latitude < -90:
                raise ValueError

        except ValueError:
            return jsonify({'status':"ERROR"})

        try:
            longitude = float(longitude)

            if longitude > 180 or longitude < -180:
                raise ValueError

        except ValueError:
            return jsonify({'status':"ERROR"})

        # Parse date
        opened = ""
        close = ""

        try:
            opened = datetime.datetime.strptime(open_date, "%Y-%m-%dT%H:%M")
        except ValueError:
            return jsonify({'status':"ERROR"})

        try:
            close = datetime.datetime.strptime(close_date, "%Y-%m-%dT%H:%M")
        except ValueError:
            return jsonify({'status':"ERROR"})

        if opened >= close:
            return jsonify({'status':"ERROR"})

        # Parse inventory
        inventory_list = [x.strip() for x in inventory.split(",")]
        items_list = []

        for i in inventory_list:
            # Check if item exist before adding
            item = database.retrieve_single_document("item", query={"item_name": i})

            if item is None:
                database.add_item("item", i, False)
                item = database.retrieve_single_document("item", query={"item_name": i})
                items_list.append(item["_id"])
            else:
                items_list.append(item["_id"])

        # get the current user's email
        email = json_data['Email']

        current_user = database.retrieve_single_document("user", {"email": email})

        # Get image
        stand_image_name = ""

        '''
        if stand_image:
            # Create a Cloud Storage client
            gcs = storage.Client()
            
            # Get the bucket that the file will be uploaded to
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
            
            #Create a new blob and upload the file's content
            blob = bucket.blob(stand_image.filename)
            
            blob.upload_from_string(
                stand_image.read(),
                content_type = stand_image.content_type
            )

        else:
            stand_image_name = DEFAULT_IMAGE_NAME
        '''

        stand_image_name = DEFAULT_IMAGE_NAME

        #stand_image_name = DEFAULT_IMAGE_NAME

        tuple_location = (latitude, longitude)

        # check if theres a duplicate
        duplicate = list(database.retrieve_documents("stand", query = {"stand_name" : stand_name,
        "location": tuple_location, "date_time_open": opened, "date_time_closed": close}))
        if duplicate:
            # There is a duplicate - show error
            return jsonify({'status':"ERROR"})

        database.add_stand("stand", stand_name, items_list, current_user["_id"],
                           stand_image_name, tuple_location, opened, close)

        return jsonify({'status':"SUCCESS"})

    return jsonify({'status':"ERROR"})
