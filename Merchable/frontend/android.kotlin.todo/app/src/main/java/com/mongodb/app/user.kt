package com.mongodb.app

import io.realm.RealmList
import io.realm.RealmObject
import io.realm.annotations.PrimaryKey
import io.realm.annotations.Required
import org.bson.types.ObjectId

// data model matching the schema in MongoDB for "user"
open class user(
    @PrimaryKey var _id: ObjectId? = null,

    var email: String? = null,

    @Required
    var subscribed_stands: RealmList<ObjectId> = RealmList(),

    var username: String? = null
): RealmObject() {}