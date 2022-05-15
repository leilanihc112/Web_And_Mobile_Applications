package com.mongodb.app

import androidx.fragment.app.Fragment

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup

import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions

class StandLocationMapFragment : Fragment() {

    private val callback = OnMapReadyCallback { googleMap ->
        /**
         * Manipulates the map once available.
         * This callback is triggered when the map is ready to be used.
         * This is where we can add markers or lines, add listeners or move the camera.
         * In this case, we just add a marker near Sydney, Australia.
         * If Google Play services is not installed on the device, the user will be prompted to
         * install it inside the SupportMapFragment. This method will only be triggered once the
         * user has installed Google Play services and returned to the app.
         */

        val args = arguments
        val standName = args?.getString("standName")
        val standLocation = args?.getString("latLngString")
        val standLatLng : LatLng = parseLatLng(standLocation)
        googleMap.addMarker(MarkerOptions().position(standLatLng).title("$standName: $standLocation"))
        googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(standLatLng, DEFAULT_ZOOM.toFloat()))
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_stand_location_map, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val mapFragment = childFragmentManager.findFragmentById(R.id.map) as SupportMapFragment?
        mapFragment?.getMapAsync(callback)
    }

    private fun parseLatLng(latLngStr : String?): LatLng {
        var latLng : LatLng = LatLng(-34.0, 151.0)

        if(latLngStr != null) {
            val splitComma : List<String> = latLngStr.split(",", ignoreCase=true, limit=2)
            var latRawStr = splitComma[0].replace(" ", "")
            var lngRawStr = splitComma[1].replace(" ", "")
            latRawStr = latRawStr.replace("(", "")
            lngRawStr = lngRawStr.replace(")", "")
            latLng = LatLng(latRawStr.toDouble(), lngRawStr.toDouble())
        }

        return latLng
    }

    companion object {
        private const val DEFAULT_ZOOM = 15
    }
}