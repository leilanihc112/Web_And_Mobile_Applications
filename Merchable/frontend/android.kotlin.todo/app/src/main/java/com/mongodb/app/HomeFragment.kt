package com.mongodb.app

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.mongodb.app.R
import com.mongodb.app.databinding.FragmentHomeBinding

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val root: View = binding.root

        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        activity?.findViewById<TextView>(R.id.merchable_main)?.visibility = View.VISIBLE
        activity?.findViewById<Button>(R.id.logoutBtn)?.visibility = View.VISIBLE

    }

    override fun onDestroyView() {
        super.onDestroyView()
        activity?.findViewById<TextView>(R.id.merchable_main)?.visibility = View.INVISIBLE
        activity?.findViewById<Button>(R.id.logoutBtn)?.visibility = View.INVISIBLE
        _binding = null
    }
}