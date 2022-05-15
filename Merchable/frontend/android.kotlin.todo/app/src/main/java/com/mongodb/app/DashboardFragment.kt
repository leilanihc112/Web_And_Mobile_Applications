package com.mongodb.app

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.mongodb.app.R
import com.mongodb.app.databinding.FragmentDashboardBinding

class DashboardFragment : Fragment() {

    private var _binding: FragmentDashboardBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentDashboardBinding.inflate(inflater, container, false)

        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Navigate to create stand
        view.findViewById<Button>(R.id.create_stand_button).setOnClickListener {
            findNavController().navigate(R.id.action_navigation_dashboard_to_createStandFragment)
        }

        // Navigate to view stands
        view.findViewById<Button>(R.id.view_stands_button).setOnClickListener {
            findNavController().navigate(R.id.action_navigation_dashboard_to_viewAllStandsFragment3)
        }

        // Navigate to view nearby stands
        view.findViewById<Button>(R.id.view_nearby_stands_button).setOnClickListener {
            findNavController().navigate(R.id.action_navigation_dashboard_to_viewNearbyStandsFragment)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}