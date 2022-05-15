package com.mongodb.app

import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import androidx.appcompat.widget.LinearLayoutCompat
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.navigation.findNavController
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.mongodb.app.databinding.FragmentViewSingleStandBinding
import com.squareup.picasso.Picasso
import io.realm.kotlin.where
import io.realm.mongodb.sync.Subscription
import org.bson.types.ObjectId
import java.text.SimpleDateFormat
import java.util.*


/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class ViewSingleStandFragment : Fragment() {

    private var _binding: FragmentViewSingleStandBinding? = null
    private lateinit var recyclerView: RecyclerView

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentViewSingleStandBinding.inflate(inflater, container, false)
        return binding.root
    }

    val args: ViewSingleStandFragmentArgs by navArgs()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // recycler view will dynamically populate posts based on results returned from database
        recyclerView = view.findViewById(R.id.post_list)
        recyclerView.layoutManager = LinearLayoutManager(view.context)
        recyclerView.setHasFixedSize(true)
        val itemDecoration = DividerItemDecoration(view.context, DividerItemDecoration.VERTICAL)
        itemDecoration.setDrawable(ContextCompat.getDrawable(view.context, R.drawable.divider)!!)
        recyclerView.addItemDecoration(itemDecoration)

        // get stand
        val subscriptions = userRealm.subscriptions
        subscriptions.update { subscriptions ->
            subscriptions.addOrUpdate(
                Subscription.create(
                    "current-stand-search",
                    userRealm.where<stand>().isNotNull("_id")
                )
            )
        }

        subscriptions.waitForSynchronization()
        userRealm.refresh()

        Log.d("ViewSingleStandFragment", "onViewCreated: ${ObjectId(args.standId)}")

        val curStand = userRealm.where<stand>().equalTo("_id", ObjectId(args.standId)).sort("_id").findAll().first()

        binding.viewStandCreatePost.setOnClickListener {
            val action = ViewSingleStandFragmentDirections.actionViewSingleStandFragment3ToCreatePostFragment3((curStand!!)._id.toString())
            view.findNavController().navigate(action)
        }

        var stand_name: TextView = view.findViewById(R.id.view_stand_stand_name)
        var stand_image: ImageView = view.findViewById(R.id.view_stand_image)
        val stand_creator: TextView = view.findViewById(R.id.view_stand_creator)
        var stand_hours: TextView = view.findViewById(R.id.view_stand_date_time)
        var stand_location: TextView = view.findViewById(R.id.view_stand_location_coordinates)
        var stand_inventory_list: LinearLayout = view.findViewById(R.id.view_stand_inventory_list_items)

        // get user that created the stand
        subscriptions.update { subscriptions ->
            subscriptions.addOrUpdate(
                Subscription.create(
                    "current-stand-user-search",
                    userRealm.where<user>().isNotNull("_id")
                )
            )
        }

        subscriptions.waitForSynchronization()
        userRealm.refresh()

        // fill in stand information
        stand_name.text = (curStand!!).stand_name
        stand_creator.text = (userRealm.where<user>().equalTo("_id", (curStand!!).user).sort("_id").findAll().first()!!).username
        // make datetime in readable format
        val pattern = "MM-dd-yyyy hh:mma"
        val simpleDateFormat = SimpleDateFormat(pattern)
        val simpleDateFormat2 = SimpleDateFormat(pattern)
        simpleDateFormat.setTimeZone(TimeZone.getTimeZone("UTC"))
        simpleDateFormat2.setTimeZone(TimeZone.getTimeZone("UTC"))
        stand_hours.text = simpleDateFormat.format(curStand.date_time_open) + " - " + simpleDateFormat2.format(curStand.date_time_closed)
        val stand_location_string_builder = StringBuilder()
        stand_location_string_builder.append("(")
            .append((curStand).location[0].toString())
            .append(", ").append((curStand).location[1].toString())
            .append(")")
        stand_location.text = "See location on map"
        stand_location.paintFlags = Paint.UNDERLINE_TEXT_FLAG
        // allow user to see where the stand is located on the map
        stand_location.setOnClickListener { view: View ->
            val action = ViewSingleStandFragmentDirections
                .actionViewSingleStandFragment3ToStandLocationMapFragment(((curStand).stand_name).toString(), stand_location_string_builder.toString())
            view.findNavController().navigate(action)
        }
        Picasso.get().load((curStand!!).photo).resize(170, 170).centerCrop().into(stand_image)

        val inventory_list = curStand.inventory_list

        // get user that created the stand
        subscriptions.update { subscriptions ->
            subscriptions.addOrUpdate(
                Subscription.create(
                    "current-stand-inventory-list-search",
                    userRealm.where<item>().isNotNull("_id")
                )
            )
        }

        subscriptions.waitForSynchronization()
        userRealm.refresh()

        // dynamically fill in inventory list
        for (item in inventory_list) {
            val inventory_item = userRealm.where<item>().equalTo("_id", item).sort("_id").findAll().first()
            val textView = TextView(getActivity())
            val lparams = LinearLayoutCompat.LayoutParams(
                LinearLayoutCompat.LayoutParams.WRAP_CONTENT,
                LinearLayoutCompat.LayoutParams.WRAP_CONTENT
            )
            textView.setLayoutParams(lparams)
            textView.text = (inventory_item)!!.item_name
            textView.textSize = 14F
            textView.setTextColor(Color.BLACK)
            stand_inventory_list.addView(textView)
        }

        // get posts associated with stand
        subscriptions.update { subscriptions ->
            subscriptions.addOrUpdate(
                Subscription.create(
                    "current-post-search",
                    userRealm.where<post>().isNotNull("_id")
                )
            )
        }

        subscriptions.waitForSynchronization()
        userRealm.refresh()

        // put posts based on results from database
        recyclerView.adapter = PostAdapter(userRealm.where<post>().equalTo("stand", (curStand!!)._id).sort("_id").findAllAsync(), config)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
        userRealm.refresh()
        //recyclerView.adapter = null
    }
}