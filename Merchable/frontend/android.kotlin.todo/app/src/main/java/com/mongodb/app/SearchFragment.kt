package com.mongodb.app

import android.os.Bundle
import android.view.LayoutInflater
import android.view.MenuItem
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.navArgs
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.textfield.TextInputEditText
import com.mongodb.app.*
import com.mongodb.app.PostAdapter
import com.mongodb.app.databinding.FragmentSearchBinding
import io.realm.kotlin.where
import io.realm.mongodb.sync.Subscription

class SearchFragment : Fragment() {

    private var _binding: FragmentSearchBinding? = null
    private lateinit var recyclerView: RecyclerView

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentSearchBinding.inflate(inflater, container, false)
        val root: View = binding.root

        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val subscriptions = userRealm.subscriptions

        // get posts that match the tag
        subscriptions.update { subscriptions ->
            subscriptions.addOrUpdate(
                Subscription.create(
                    "search-posts-tag-search",
                    userRealm.where<post>().isNotNull("_id")
                )
            )
        }

        // recycler view will dynamically populate posts based on results returned from database
        recyclerView = view.findViewById(R.id.search_posts_posts)
        recyclerView.layoutManager = LinearLayoutManager(view.context)
        recyclerView.setHasFixedSize(true)
        val itemDecoration = DividerItemDecoration(view.context, DividerItemDecoration.VERTICAL)
        itemDecoration.setDrawable(ContextCompat.getDrawable(view.context, R.drawable.divider)!!)
        recyclerView.addItemDecoration(itemDecoration)
        recyclerView.adapter = null

        val args: SearchFragmentArgs by navArgs()

        subscriptions.waitForSynchronization()
        userRealm.refresh()

        // put posts based on results from database
        recyclerView.adapter = PostAdapter(userRealm.where<post>().equalTo("tags", args.tag).sort("_id").findAllAsync(), config)

        binding.searchPostsSearch.setOnClickListener {
            recyclerView.adapter = null

            var search_posts_input: TextInputEditText = view.findViewById(R.id.search_posts_input)

            subscriptions.waitForSynchronization()
            userRealm.refresh()

            // put posts based on results from database
            recyclerView.adapter = PostAdapter(userRealm.where<post>().equalTo("tags", search_posts_input.text.toString()).sort("_id").findAllAsync(), config)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
        userRealm.refresh()
    }
}