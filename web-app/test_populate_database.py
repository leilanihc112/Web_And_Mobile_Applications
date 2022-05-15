""" demo.py """
import datetime
from database import Database

def demo_item(database):
    """ Demonstration of API methods for MongoDB instance for items """

    # ITEM
    # CREATE COLLECTION, ADD ITEM, RETRIEVE, & RETRIEVE/SORT
    # create item collection
    database.create_collection("item")
    # add shirt
    database.add_item("item", "Shirt", True)
    # add poster
    database.add_item("item", "Poster", False)
    # add sticker
    database.add_item("item", "Sticker", True)
    # add hoodie
    database.add_item("item", "Hoodie", True)
    # get all items so far
    all_items = database.retrieve_documents("item")
    print("After Add Item:")
    for doc in all_items:
        print(doc)
    print("\n")
    # get all items so far and sort
    all_items = database.retrieve_sort_query("item", "name", direction=-1)
    print("After Sort:")
    for doc in all_items:
        print(doc)
    print("\n")

    # UPDATE ITEM & RETRIEVE
    # get items that were updated
    print("After Update Item (only get items that were updated):")
    for doc in all_items:
        print(doc)
    print("\n")


def demo_user(database):
    """ Demonstration of API methods for MongoDB instance for users """

    # USER
    # CREATE COLLECTION, ADD USER, & RETRIEVE
    # create user collection
    database.create_collection("user")
    # add vendor
    database.add_user("user", "vendor1", "vendor1@vendor.com", [])
    database.add_user("user", "vendor2", "vendor2@vendor.com", [])
    database.add_user("user", "vendor3", "vendor3@vendor.com", [])
    # get all users so far
    all_users = database.retrieve_documents("user")
    print("After Add User:")
    for doc in all_users:
        print(doc)
    print("\n")

    # UPDATE USER
    print("Update User Email:")
    database.update_documents("user", { "username" : "vendor1" },
                         { "email": "vendor12@vendor.com" })
    vendor_1 = database.retrieve_single_document("user", { "username": "vendor1" })
    print(vendor_1)
    print("\n")


def demo_stand(database):
    """ Demonstration of API methods for MongoDB instance for stands """

    # STAND
    # CREATE COLLECTION, ADD STAND, RETRIEVE, & RETRIEVE SINGLE
    # create stand collection
    database.create_collection("stand")
    # get vendor to link
    vendor_1 = database.retrieve_single_document("user", { "username": "vendor1" })
    # get items
    all_items = database.retrieve_documents("item")
    items_list = []
    for doc in all_items:
        items_list.append(doc["_id"])
    # add a stand created by vendor above
    database.add_stand("stand", "Stand 1", items_list, vendor_1["_id"],
                       "green_image1.png", [30.266657, -98.317321],
                       datetime.datetime.now(),
                       datetime.datetime.fromisoformat('2022-02-19 21:00'))
    # get all stands so far
    all_stands = database.retrieve_documents("stand")
    print("After Add Stand:")
    for doc in all_stands:
        print(doc)
    print("\n")

    # look for all photographs tied to stands
    all_posts = database.retrieve_documents("stand", {}, {"photo": 1, "_id": 0})
    print("All uploaded photos tied to stands:")
    for doc in all_posts:
        print(doc["photo"])
    print("\n")


def demo_post(database):
    """ Demonstration of API methods for MongoDB instance for posts """

    # POST
    # CREATE COLLECTION, ADD USER, ADD POST
    # create post collection
    database.create_collection("post")
    # add poster user
    database.add_user("user", "poster1", "poster1@poster.com", [])
    # get user to link
    user_1 = database.retrieve_single_document("user", { "username": "poster1" })
    # get stand to link
    stand_1 = database.retrieve_single_document("stand", { "stand_name": "Stand 1" })
    photolist = ["green_image1.png", "blue_image1.png"]

    # add a post for the user about
    database.add_post("post", user_1["_id"], stand_1["_id"], datetime.datetime.now(),
                      "New post Title", "This is a post from a new user ", photolist, \
                      ["Tag 1","Tag 2"])
    database.add_post("post", user_1["_id"], stand_1["_id"], datetime.datetime.now(),
                      "No photos post", "This is a post without  ",  "", ["Tag 3","Tag 4"])

    # get all posts so far
    all_posts = database.retrieve_documents("post")
    print("After Add Post:")
    for doc in all_posts:
        print(doc)
    print("\n")

    # look for all photographs tied to posts
    all_posts = database.retrieve_documents("post", {}, {"photos": 1, "_id": 0})
    print("All uploaded photos tied to posts:")
    for doc in all_posts:
        for everyfile in doc["photos"]:
            print(everyfile)
    print("\n")


def demo_photos(database):
    """ Add default pictures """
    photolist = ["default.png"]

    for photofile in photolist:
        with open(photofile, 'rb') as fi_r:
            fcontent = fi_r.read()
            # Now store/put the image via GridFs object.
            database.fs_obj.put(fcontent, filename=photofile)
            #now save flask mongo
            #mongo.save_file(photofile,fi_r)
            print(photofile)


def demo_delete(database):
    """ Demonstration of API methods for MongoDB instance for deleting """

    # DELETE
    # DELETE DOCUMENT
    all_docs = database.delete_documents("item", { "available": False })
    print("After Delete Single Item Document:\n", all_docs.deleted_count, " documents deleted\n")
    all_docs = database.delete_documents("item", {})
    print("After Delete Multiple Item Documents:\n", all_docs.deleted_count, " documents deleted\n")
    all_docs = database.delete_stands("stand", {})
    print("After Delete Multiple Stand Documents:\n", all_docs.deleted_count, \
    " documents deleted\n")

    # Delete all posts and associated photos
    all_docs = database.delete_posts("post", {})
    print("After Delete Multiple Post Documents:\n", all_docs.deleted_count, " documents deleted\n")

    # DELETE COLLECTIONS
    print("Before Delete Collections:\n", database.data_base.list_collection_names(), "\n")
    database.delete_collection("item")
    database.delete_collection("user")
    database.delete_collection("stand")
    database.delete_collection("post")
    database.delete_collection("fs.files")
    database.delete_collection("fs.chunks")
    print("After Delete Collections:\n", database.data_base.list_collection_names(), "\n")


if __name__ == "__main__":
    database_instance = Database()
    demo_photos(database_instance)
    demo_item(database_instance)
    demo_user(database_instance)
    demo_stand(database_instance)
    demo_post(database_instance)
    #demo_delete(database_instance)
