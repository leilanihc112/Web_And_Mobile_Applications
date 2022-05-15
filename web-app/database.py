""" database.py """
from typing import Tuple, List
import datetime
import pymongo
from decouple import config
import bson

class Database:
    """ MongoDB instance and API methods for create, retrieve, delete, update, etc. """
    uri = None
    data_base = None

    def __init__(self) -> None:
        """ Initialize Database object """
        # Must be configured in .env file in the current working directory
        self.uri = config("DB_URI")
        self.client = pymongo.MongoClient(self.uri)
        self.data_base = self.client.business
        # Indicate that we are connected to the database
        print("Connected")

    def create_collection(self, col: str) -> pymongo.collection.Collection:
        """
        Create a new collection.

        Parameters:
            - col [str] = The name of the new collection.

        Return value:
            - [pymongo.collection.Collection] The newly created collection. If the
              collection already exists, the existing collection will be returned.
        """
        col = self.data_base[col]
        return col

    def delete_collection(self, col: str) -> None:
        """
        Delete a collection.

        Parameters:
            - col [str] = The name of the collection to delete.
        """
        self.data_base[col].drop()

    def delete_documents(self, col: str, query: dict) -> pymongo.results.DeleteResult:
        """
        Delete one or more documents based on a given query.

        Parameters:
            - col [str] = The name of the collection to delete the documents from.
            - query [dict] = Query of the documents to delete from the collection.

        Return value:
            - [pymongo.results.DeleteResult] The result of deleting the documents:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """
        return self.data_base[col].delete_many(query)

    def update_documents(self, col: str, data: dict, query: dict) -> \
    pymongo.results.UpdateResult:
        """
        Update one or more values of a given query of documents.

        Parameters:
            - col [str] = The name of the collection to get the documents from.
            - data [dict] = A set that includes the values to be updated for the documents.
            - query [dict] = Query of the documents to update from the collection.

        Return value:
            - [pymongo.results.UpdateResult] The result of updating the documents:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """
        update_values = { "$set": data }
        return self.data_base[col].update_many(query, update_values)

    def retrieve_single_document(self, col: str, query: dict = None, attributes: dict = None) \
    -> dict:
        """
        Retrieve a single document based on an optional given query. Optionally, only certain
        attributes of the documents can be shown.

        Parameters:
            - col [str] = The name of the collection to get the document from.
            - query [dict] (optional) = Query of the document to return from the
                collection. If no query is specified, the first document from the collection
                will be returned.
            - attributes [dict] (optional) = Attributes of returned document to show. If
                no attributes are specified, all attributes will be returned. 1 = show,
                0 = don't show.

        Return value:
            - [dict] The resulting document.
        """
        return self.data_base[col].find_one(query, attributes)

    def retrieve_documents(self, col: str, query: dict = None, attributes: dict = None,
    first_index: int = None, last_index: int = None) -> pymongo.cursor.Cursor:
        """
        Retrieve one or more documents, based on an optional given query. Optionally, only
        certain attributes of the documents can be shown.

        Parameters:
            - col [str] = The name of the collection to get documents from.
            - query [dict] (optional) = Query of documents to return from the
                collection. If no query is specified, all documents from the collection
                will be returned.
            - attributes [dict] (optional) = Attributes of returned documents to show. If
                no attributes are specified, all attributes will be returned. 1 = show,
                0 = don't show.
            - first_index [int] (optional) = First index to grab from the returned query.
                If no value is entered, the entire result will be returned. This can be entered
                alone to get a single document.
            - last_index [int] (optional) = Last index to grab from the returned query.
                If no value is entered, the entire result will be returned. Must be filled in
                with first_value, otherwise, the entire result will be returned.

        Return value:
            - [pymongo.cursor.Cursor] All of the resulting documents:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html
        """

        if first_index is not None:
            if last_index is not None:
                return self.data_base[col].find(query, attributes)[first_index:last_index]
            else:
                return self.data_base[col].find(query, attributes)[first_index]
        else:
            return self.data_base[col].find(query, attributes)

    def retrieve_sort_query(self, col: str, fieldname: str, query: dict = None,
    attributes: dict = None, direction: int = 1) -> pymongo.cursor.Cursor:
        """
        Retrieve documents based on an optional given query and sort based on a specific
        field, in ascending or descending order. Optionally, only certain attributes of
        the documents can be shown.

        Parameters:
            - col [str] = The name of the collection to get documents from.
            - fieldname [str] = Name of the field to base on for the sort.
            - query [dict] (optional) = Query of documents to return from the
                collection. If no query is specified, all documents from the collection
                will be returned.
            - attributes [dict] (optional) = Attributes of returned documents to show. If
                no attributes are specified, all attributes will be returned.
            - direction [int] (optional) = Direction to sort the results in (ascending or
                descending). Default is ascending. 1 = Ascending, -1 = Descending.

        Return value:
            - [pymongo.cursor.Cursor] All of the resulting documents, sorted:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html
        """
        return self.data_base[col].find(query, attributes).sort(fieldname, direction)

    def add_item(self, col: str, item_name: str, available: bool) \
    -> pymongo.results.InsertOneResult:
        """
        Create a new item. Items are associated with a specific stand.

        Parameters:
            - col [str] = Name of the "item" collection.
            - name [str] = The name of the item.
            - available [bool] = Flag indicating whether the item is available or not.

        Return value:
            - [pymongo.results.InsertOneResult] The newly created item document:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """
        my_item = {"item_name": item_name, "available": available}
        return self.data_base[col].insert_one(my_item)

    def add_user(self, col: str, username: str, email: str,
    subscribed_stands: List[bson.objectid.ObjectId]) -> pymongo.results.InsertOneResult:
        """
        Create a new user. Users can create stands and items and can create posts on a stand
        to indicate whether items are available at that stand.

        Parameters:
            - col [str] = Name of the "user" collection.
            - username [str] = Username for the user account.
            - email [str] = Email for the user account.
            - subscribed_stands [list of bson.objectid.ObjectId] = The IDs of the stands that
                the user has subscribed to.

        Return value:
            - [pymongo.results.InsertOneResult] The newly created user document:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """
        my_user = {"username": username, "email": email,
        "subscribed_stands": subscribed_stands}
        return self.data_base[col].insert_one(my_user)

    def add_stand(self, col: str, stand_name: str, inventory_list: List[bson.objectid.ObjectId],
                  user: bson.objectid.ObjectId, photo: str, location: Tuple[float, float],
                  date_time_open: datetime.datetime, date_time_closed: datetime.datetime) \
                  -> pymongo.results.InsertOneResult:
        """
        Create a new stand. Stands contain items, and posts can be created by users
        on a stand to indicate whether items are available or not.

        Parameters:
            - col [str] = Name of the "stand" collection.
            - stand_name [str] = Name of the stand.
            - inventory_list [list of bson.objectid.ObjectId] = List of IDs of items
                available for purchase at the stand.
            - user [bson.objectid.ObjectId] = ID of the user that created the item.
            - photo [str] = Path to the photo related to the stand.
            - location [tuple of two floats] = Latitude and longitude coordinates of where
                the stand is located.
            - date_time_open [datetime] = Date and time the stand is open.
            - date_time_closed [datetime] = Date and time the stand is closed.

        Return value:
            - [pymongo.results.InsertOneResult] The newly created stand document:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """

        my_stand = { "stand_name": stand_name, "inventory_list": inventory_list,
                     "user": user, "photo": photo, "location": location,
                     "date_time_open": date_time_open, "date_time_closed": date_time_closed }
        return self.data_base[col].insert_one(my_stand)

    def update_stands(self, col: str, data: dict, query: dict) -> \
    pymongo.results.UpdateResult:
        """
        Update one or more values of a given query of stands.

        Parameters:
            - col [str] = Name of the "stand" collection.
            - data [dict] = A set that includes the values to be updated for the stand.
            - query [dict] = Query used to find the specific stand(s) to be updated.

        INFO ON STANDS USED FOR QUERIES AND WHAT CAN BE UPDATED:
            - stand_name [str] = Name of the stand.
            - location [tuple of two floats] = Latitude and longitude coordinates of where
                the stand is located.
            - date_time_open [datetime] = Date and time the stand is open.
            - date_time_closed [datetime] = Date and time the stand is closed.
            - inventory_list [list of str] = List of names of items available for purchase
                at the stand.
            - user [bson.objectid.ObjectId] = ID of the user that created the item.
            - photo [str] = The name of the photo related to the stand.

        Return value:
            - [pymongo.results.UpdateResult] The result of updating the stand documents:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """
        update_values = { "$set": data }
        return self.data_base[col].update_many(query, update_values)

    def delete_stands(self, col: str, query: dict) -> pymongo.results.DeleteResult:
        """
        Delete one or more stands based on a given query.

        Parameters:
            - col [str] = Name of the "stand" collection.
            - query [dict] = Query used to find the specific stand(s) to be deleted.

        INFO ON STANDS USED FOR QUERIES:
            - stand_name [str] = Name of the stand.
            - location [tuple of two floats] = Latitude and longitude coordinates of where
                the stand is located.
            - date_time_open [datetime] = Date and time the stand is open.
            - date_time_closed [datetime] = Date and time the stand is closed.
            - inventory_list [list of str] = List of names of items available for purchase
                at the stand.
            - user [bson.objectid.ObjectId] = ID of the user that created the item.
            - photo [str] = The name of the photo related to the stand.

        Return value:
            - [pymongo.results.DeleteResult] The result of deleting the stand documents:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """
        # Delete the stand documents
        delete = self.data_base[col].delete_many(query)
        return delete

    def add_post(self, col: str, user: bson.objectid.ObjectId, stand: bson.objectid.ObjectId,
    timestamp: datetime.datetime, title: str, text: str, photos: List[str] = [],
    tags: List[str] = None) -> pymongo.results.InsertOneResult:
        """
        Create a new post. Posts are created by users on a stand.

        Parameters:
            - col [str] = Name of the "post" collection.
            - user [bson.objectid.ObjectId] = ID of the user that created the post.
            - stand [bson.objectid.ObjectId] = ID of the stand that the post was made for.
            - timestamp [datetime] = Date and time that the post was created.
            - title [str] = Title of the post.
            - text [str] = Body text of the post.
            - photos [list of str] = List of paths of photos added to the post.
            - tags [list of str] = List of tags added to the post (tags act as hashtags).

        Return value:
            - [pymongo.results.InsertOneResult] The newly created post document:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """
        file_list = []
        for photofile in photos:
            file_list.append(photofile)

        tags = [tag.strip().lower() for tag in tags]

        my_post = { "user": user, "stand": stand, "timestamp": timestamp, "title":
                     title, "text": text, "photos": file_list, "tags": tags}
        return self.data_base[col].insert_one(my_post)

    def update_posts(self, col: str, data: dict, query: dict) -> \
    pymongo.results.UpdateResult:
        """
        Update one or more values of a given query of posts.

        Parameters:
            - col [str] = Name of the "post" collection.
            - data [dict] = A set that includes the values to be updated for the post.
            - query [dict] = Query used to find the specific post(s) to be updated.

        INFO ON POSTS USED FOR QUERIES AND WHAT CAN BE UPDATED:
            - user [bson.objectid.ObjectId] = ID of the user that created the post.
            - stand [bson.objectid.ObjectId] = ID of the stand that the post was made for.
            - timestamp [datetime] = Date and time that the post was created.
            - title [str] = Title of the post.
            - photos [list of str] = A list of the names of photos to be related
                to the post.
            - text [str] = Body text of the post.
            - tags [list of str] = List of tags added to the post (tags act as hashtags).

        Return value:
            - [pymongo.results.UpdateResult] The result of updating the post documents:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """
        update_values = { "$set": data }
        # automatically make tags lower case and remove whitespace
        if "tags" in update_values["$set"].keys():
            tags = [tag.strip().lower() for tag in tags]
            update_values["$set"]["tags"] = tags
        return self.data_base[col].update_many(query, update_values)

    def delete_posts(self, col: str, query: dict) -> pymongo.results.DeleteResult:
        """
        Delete one or more posts.

        Parameters:
            - col [str] = Name of the "post" collection.
            - query [dict] = Query used to find the specific post(s) to be deleted.

        INFO ON POSTS USED FOR QUERIES:
            - user [bson.objectid.ObjectId] = ID of the user that created the post.
            - stand [bson.objectid.ObjectId] = ID of the stand that the post was made for.
            - timestamp [datetime] = Date and time that the post was created.
            - title [str] = Title of the post.
            - photos [list of str] = A list of the names of photos to be related
                to the post.
            - text [str] = Body text of the post.
            - tags [list of str] = List of tags added to the post (tags act as hashtags).

        Return value:
            - [pymongo.results.DeleteResult] The result of deleting the post documents:
                https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html
        """
        # Delete the post documents
        delete = self.data_base[col].delete_many(query)
        return delete
