package com.mongodb.app

import android.graphics.Color
import android.graphics.Paint
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.widget.LinearLayoutCompat
import androidx.core.content.ContextCompat
import androidx.core.view.updateLayoutParams
import androidx.navigation.findNavController
import androidx.recyclerview.widget.RecyclerView
import com.squareup.picasso.Picasso
import io.realm.OrderedRealmCollection
import io.realm.Realm.getApplicationContext
import io.realm.RealmConfiguration
import io.realm.RealmRecyclerViewAdapter
import io.realm.kotlin.where
import io.realm.mongodb.sync.Subscription
import org.bson.types.ObjectId
import java.text.SimpleDateFormat
import java.util.*

internal class PostAdapter(data: OrderedRealmCollection<post?>?, private val config: RealmConfiguration) :
    RealmRecyclerViewAdapter<post, PostAdapter.PostViewHolder?>(data, true) {

    internal inner class PostViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        var id: ObjectId? = null
        var post_title: TextView = view.findViewById(R.id.post_title)
        var post_creator: TextView = view.findViewById(R.id.post_creator)
        var post_date: TextView = view.findViewById(R.id.post_date)
        var post_text: TextView = view.findViewById(R.id.post_text)
        var post_tags: LinearLayout = view.findViewById(R.id.post_tags)
        var post_photos: LinearLayout = view.findViewById(R.id.post_photos)
    }

    override fun getItemViewType(position: Int): Int {
        return position
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PostAdapter.PostViewHolder {
        val postView = LayoutInflater.from(parent.context).inflate(R.layout.post_view, parent, false)
        return PostViewHolder(postView)
    }

    override fun onBindViewHolder(holder: PostAdapter.PostViewHolder, position: Int) {
        val curPost: post = getItem(position) ?: return

        // get user
        val subscriptions = userRealm.subscriptions
        subscriptions.update { subscriptions ->
            subscriptions.addOrUpdate(
                Subscription.create(
                    "current-post-user-search",
                    userRealm.where<user>().isNotNull("_id")
                )
            )
        }

        // wait for sync
        subscriptions.waitForSynchronization()
        userRealm.refresh()

        // get user that created the post
        val user = userRealm.where<user>().equalTo("_id", curPost.user).sort("_id").findAll().first()

        // fill in post information
        holder.id = curPost._id
        holder.post_title.text = curPost.title
        holder.post_creator.text = (user!!).username
        val pattern = "MM-dd-yyyy hh:mma"
        val simpleDateFormat = SimpleDateFormat(pattern)
        simpleDateFormat.setTimeZone(TimeZone.getTimeZone("UTC"))
        holder.post_date.text = simpleDateFormat.format(curPost.timestamp)
        holder.post_text.text = curPost.text

        val tag_list = curPost.tags

        // dynamically add tags
        for (item in tag_list) {
            val textView = TextView(getApplicationContext())
            val lparams = LinearLayoutCompat.LayoutParams(
                LinearLayoutCompat.LayoutParams.WRAP_CONTENT,
                LinearLayoutCompat.LayoutParams.WRAP_CONTENT
            )
            textView.setLayoutParams(lparams)
            textView.text = "#" + item
            textView.textSize = 14F
            textView.paintFlags = Paint.UNDERLINE_TEXT_FLAG
            textView.setTextColor(ContextCompat.getColor(getApplicationContext()!!, R.color.blue_merchable))
            textView.updateLayoutParams<ViewGroup.MarginLayoutParams>{ setMargins(0, 0, 3, 0) }
            holder.post_tags.addView(textView)

            textView.setOnClickListener { view: View ->
                val action = ViewSingleStandFragmentDirections.actionViewSingleStandFragment3ToNavigationSearch(item)
                view.findNavController().navigate(action)
            }
        }

        val photos_list = curPost.photos

        // dynamically add photos
        for (item in photos_list) {
            val imageView = ImageView(getApplicationContext())
            val lparams = LinearLayoutCompat.LayoutParams(170, 170)
            imageView.setLayoutParams(lparams)
            Picasso.get().load(item).resize(170, 170).centerCrop().into(imageView)
            imageView.updateLayoutParams<ViewGroup.MarginLayoutParams>{ setMargins(0, 0, 3, 0) }
            holder.post_photos.addView(imageView)
        }
    }
}