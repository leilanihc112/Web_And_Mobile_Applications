package com.mongodb.app

import io.realm.RealmList
import io.realm.RealmObject
import io.realm.annotations.PrimaryKey
import io.realm.annotations.Required
import org.bson.types.ObjectId
import java.util.*

// data model matching the schema in MongoDB for "stand"
open class stand(
    @PrimaryKey var _id: ObjectId? = null,

    var date_time_closed: Date? = null,

    var date_time_open: Date? = null,

    @Required
    var inventory_list: RealmList<ObjectId> = RealmList(),

    @Required
    var location: RealmList<Double> = RealmList(),

    var photo: String? = null,

    var stand_name: String? = null,

    var user: ObjectId? = null
): RealmObject() {}
