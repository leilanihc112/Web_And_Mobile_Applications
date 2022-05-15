package com.mongodb.app

import android.graphics.Paint
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.navigation.findNavController
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.RecyclerView
import com.squareup.picasso.Picasso
import io.realm.OrderedRealmCollection
import io.realm.RealmConfiguration
import io.realm.RealmRecyclerViewAdapter
import org.bson.types.ObjectId
import java.text.SimpleDateFormat
import java.util.TimeZone

internal class StandAdapter(data: OrderedRealmCollection<stand?>?, private val config: RealmConfiguration) :
    RealmRecyclerViewAdapter<stand, StandAdapter.StandViewHolder?>(data, true) {

    internal inner class StandViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        var id: ObjectId? = null
        var stand_name: TextView = view.findViewById(R.id.stand_name)
        var stand_hours: TextView = view.findViewById(R.id.stand_hours)
        var stand_location: TextView = view.findViewById(R.id.stand_location)
        var stand_image: ImageView = view.findViewById(R.id.stand_image)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): StandViewHolder {
        val standView = LayoutInflater.from(parent.context).inflate(R.layout.stand_view, parent, false)
        return StandViewHolder(standView)
    }

    override fun onBindViewHolder(holder: StandViewHolder, position: Int) {
        val curStand: stand = getItem(position) ?: return

        // fill in stand information
        holder.id = curStand._id
        holder.stand_name.text = curStand.stand_name
        holder.stand_name.paintFlags = Paint.UNDERLINE_TEXT_FLAG
        // format datetime in readable format
        val pattern = "MM-dd-yyyy hh:mma"
        val simpleDateFormat = SimpleDateFormat(pattern)
        val simpleDateFormat2 = SimpleDateFormat(pattern)
        simpleDateFormat.setTimeZone(TimeZone.getTimeZone("UTC"))
        simpleDateFormat2.setTimeZone(TimeZone.getTimeZone("UTC"))
        holder.stand_hours.text = simpleDateFormat.format(curStand.date_time_open) + " - " + simpleDateFormat2.format(curStand.date_time_closed)
        val stand_location_string_builder = StringBuilder()
        stand_location_string_builder.append("(")
            .append((curStand).location[0].toString())
            .append(", ").append((curStand).location[1].toString())
            .append(")")
        holder.stand_location.text = "See location on map"
        holder.stand_location.paintFlags = Paint.UNDERLINE_TEXT_FLAG
        Picasso.get().load(curStand.photo).resize(170, 170).centerCrop().into(holder.stand_image)
        // allow user to view stand info by clicking the name
        holder.stand_name.setOnClickListener { view: View ->
            val action = ViewAllStandsFragmentDirections.actionViewAllStandsFragment3ToViewSingleStandFragment3(holder.id.toString())
            view.findNavController().navigate(action)
        }
        // allow user to see where the stand is located on the map
        holder.stand_location.setOnClickListener { view: View ->
            val action = ViewAllStandsFragmentDirections
                .actionViewNearbyStandsFragmentToStandLocationMapFragment(((curStand).stand_name).toString(), stand_location_string_builder.toString())
            view.findNavController().navigate(action)
        }
    }
}