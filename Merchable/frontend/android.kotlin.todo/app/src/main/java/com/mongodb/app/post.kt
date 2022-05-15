package com.mongodb.app

import io.realm.RealmList
import io.realm.RealmObject
import io.realm.annotations.PrimaryKey
import io.realm.annotations.Required
import org.bson.types.ObjectId
import java.util.*

// data model matching the schema in MongoDB for "post"
open class post(
    @PrimaryKey var _id: ObjectId? = null,

    @Required
    var photos: RealmList<String> = RealmList(),

    var stand: ObjectId? = null,

    @Required
    var tags: RealmList<String> = RealmList(),

    var text: String? = null,

    var timestamp: Date? = null,

    var title: String? = null,

    var user: ObjectId? = null
): RealmObject() {}