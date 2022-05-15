package com.mongodb.app

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import com.mongodb.app.databinding.FragmentViewAllStandsBinding
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import io.realm.kotlin.where
import io.realm.mongodb.sync.Subscription


/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class ViewAllStandsFragment : Fragment() {

    private var _binding: FragmentViewAllStandsBinding? = null
    private lateinit var recyclerView: RecyclerView

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentViewAllStandsBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        Log.d(TAG(), "VIEW CREATED VIEW ALL STANDS")

        // recycler view will dynamically populate based on database results for how many stands
        // there are
        recyclerView = view.findViewById(R.id.stand_list)
        recyclerView.layoutManager = LinearLayoutManager(view.context)
        recyclerView.setHasFixedSize(true)
        val itemDecoration = DividerItemDecoration(view.context, DividerItemDecoration.VERTICAL)
        itemDecoration.setDrawable(ContextCompat.getDrawable(view.context, R.drawable.divider)!!)
        recyclerView.addItemDecoration(itemDecoration)

        // get stands
        val subscriptions = userRealm.subscriptions
        subscriptions.update { subscriptions ->
            subscriptions.addOrUpdate(
                Subscription.create(
                    "all-stands-search",
                    userRealm.where<stand>().isNotNull("_id")
                )
            )
        }

        subscriptions.waitForSynchronization()
        userRealm.refresh()

        // fill in the recycler view based on what was retrieved from database
        recyclerView.adapter = StandAdapter(userRealm.where<stand>().sort("_id").findAllAsync(), config)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
        recyclerView.adapter = null
    }
}