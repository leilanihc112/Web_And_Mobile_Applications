package com.mongodb.app

import io.realm.RealmObject;
import io.realm.annotations.PrimaryKey
import org.bson.types.ObjectId;

// data model matching the schema in MongoDB for "item"
open class item(
    @PrimaryKey var _id: ObjectId? = null,

    var available: Boolean? = null,

    var item_name: String? = null
): RealmObject() {}