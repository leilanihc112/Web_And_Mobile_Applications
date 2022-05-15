package com.mongodb.app

import androidx.fragment.app.Fragment

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.location.Location
import android.location.Location.distanceBetween
import android.os.Bundle
import android.util.Log
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.navigation.fragment.findNavController
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.Marker
import com.google.android.gms.maps.model.MarkerOptions
import com.mongodb.app.databinding.FragmentViewNearbyStandsBinding
import com.google.android.material.internal.ContextUtils
import io.realm.kotlin.where
import io.realm.mongodb.sync.Subscription
import org.bson.types.ObjectId

class ViewNearbyStandsFragment : Fragment() {

    private var map: GoogleMap? = null
    private lateinit var binding: FragmentViewNearbyStandsBinding

    // The entry point to the Fused Location Provider.
    private lateinit var fusedLocationProviderClient: FusedLocationProviderClient

    // A default location (Sydney, Australia) and default zoom to use when location permission is
    // not granted.
    private val defaultLocation = LatLng(-33.8523341, 151.2106085)
    private var locationPermissionGranted = false
    private var lastKnownLocation: Location? = null
    private var cameraPosition: CameraPosition? = null

    private var standCount = 0
    private var standList: MutableList<stand> = ArrayList()

    private var markerMap : MutableMap<Marker, String> = HashMap()

    private val callback = OnMapReadyCallback { googleMap ->
        /**
         * Manipulates the map once available.
         * This callback is triggered when the map is ready to be used.
         * If Google Play services is not installed on the device, the user will be prompted to
         * install it inside the SupportMapFragment. This method will only be triggered once the
         * user has installed Google Play services and returned to the app.
         */
        Log.d(TAG, "callback")

        map = googleMap

        // Prompt the user for permission.
        getLocationPermission()

        // Turn on the My Location layer and the related control on the map.
        updateLocationUI()

        // Get information about the stands
        getStandInfo()

        // Get the current location of the device and set the position of the map.
        getDeviceLocation()
    }

    @SuppressLint("RestrictedApi")
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d(TAG, "onCreateView")

        // Retrieve location and camera position from saved instance state.
        if (savedInstanceState != null) {
            lastKnownLocation = savedInstanceState.getParcelable(KEY_LOCATION)
            cameraPosition = savedInstanceState.getParcelable(KEY_CAMERA_POSITION)
        }

        // Construct a FusedLocationProviderClient.
        //fusedLocationProviderClient = myLocationHelper.getFusedLocationProviderClient()
        val act = ContextUtils.getActivity(context)
        if(act != null) {
            fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(act)
        }

        return inflater.inflate(R.layout.fragment_view_nearby_stands, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        Log.d(TAG, "onViewCreated")

        val mapFragment = childFragmentManager.findFragmentById(R.id.map) as SupportMapFragment?
        mapFragment?.getMapAsync(callback)
    }

    /**
     * Prompts the user for permission to use the device location.
     */
    @SuppressLint("RestrictedApi")
    private fun getLocationPermission() {
        /*
         * Request location permission, so that we can get the location of the
         * device. The result of the permission request is handled by a callback,
         * onRequestPermissionsResult.
         */
        val cxt = context
        if(cxt != null) {
            if (ContextCompat.checkSelfPermission(cxt,
                    Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED) {
                locationPermissionGranted = true
            } else {
                val act = ContextUtils.getActivity(context)
                if(act != null) {
                    ActivityCompat.requestPermissions(act, arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
                        PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION
                    )
                }

            }
        }
    }

    /**
     * Updates the map's UI settings based on whether the user has granted location permission.
     */
    @SuppressLint("MissingPermission")
    private fun updateLocationUI() {
        if (map == null) {
            return
        }
        try {
            if (locationPermissionGranted) {
                map?.isMyLocationEnabled = true
                map?.uiSettings?.isMyLocationButtonEnabled = true
            } else {
                map?.isMyLocationEnabled = false
                map?.uiSettings?.isMyLocationButtonEnabled = false
                lastKnownLocation = null
                getLocationPermission()
            }
        } catch (e: SecurityException) {
            Log.e("Exception: %s", e.message, e)
        }
    }

    /**
     * Gets the current location of the device, and positions the map's camera.
     */
    @SuppressLint("MissingPermission", "RestrictedApi")
    private fun getDeviceLocation() {
        /*
         * Get the best and most recent location of the device, which may be null in rare
         * cases when a location is not available.
         */
        try {
            if (locationPermissionGranted) {
                Log.d(TAG, "Location permission granted")

                val locationResult = fusedLocationProviderClient.lastLocation
                val act = ContextUtils.getActivity(context)
                if(act != null) {
                    locationResult.addOnCompleteListener(act) { task ->
                        if (task.isSuccessful) {
                            // Set the map's camera position to the current location of the device.
                            lastKnownLocation = task.result
                            if (lastKnownLocation != null) {
                                // Override for testing purposes
                                lastKnownLocation!!.latitude = 29.626787
                                lastKnownLocation!!.longitude = -95.6865535
                                map?.moveCamera(CameraUpdateFactory.newLatLngZoom(
                                    LatLng(lastKnownLocation!!.latitude,
                                        lastKnownLocation!!.longitude), DEFAULT_ZOOM.toFloat()))
                                searchForNearbyStands(lastKnownLocation)
                            }
                        } else {
                            Log.d(TAG, "Current location is null. Using defaults.")
                            Log.e(TAG, "Exception: %s", task.exception)
                            map?.moveCamera(CameraUpdateFactory
                                .newLatLngZoom(defaultLocation, DEFAULT_ZOOM.toFloat()))
                            map?.uiSettings?.isMyLocationButtonEnabled = false
                        }
                    }
                }

            }
        } catch (e: SecurityException) {
            Log.e("Exception: %s", e.message, e)
        }
    }

    private fun getStandInfo() {
        Log.d(TAG, "Get stand info")

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

        // Get stands
        standList = userRealm.where<stand>().sort("_id").findAll()

        // Get number of stands
        standCount = standList.size

    }

    private fun searchForNearbyStands(centerLocation : Location?) {
        val nearbyStandsList: MutableList<stand> = ArrayList()
        val distance: FloatArray = FloatArray(1)
        if(centerLocation != null && standList.isNotEmpty()) {
            Log.d(TAG, "searchForNearbyStands: ${centerLocation.latitude}, ${centerLocation.longitude}")
            for(stand in standList) {
                stand.location[0]?.let { lat ->
                    stand.location[1]?.let { lng ->
                        distanceBetween(centerLocation.latitude, centerLocation.longitude,
                            lat, lng, distance)
                    }
                }
                Log.d(TAG, "searchForNearbyStands: ${distance[0]}")
                if(distance[0] <= MAX_NEARBY_DISTANCE) {
                    nearbyStandsList.add(stand)
                    Log.d(TAG, "searchForNearbyStands: ${stand._id.toString()}")

                }
            }

            if(nearbyStandsList.isNotEmpty()) {
                markNearbyStands(nearbyStandsList)
            }
        }
    }

    private fun markNearbyStands(nearbyStandsList : MutableList<stand>) {
        if(nearbyStandsList.isNotEmpty()) {
            for (stand in nearbyStandsList) {
                val lat = stand.location[0]
                val lng = stand.location[1]
                var location = defaultLocation
                if (lat != null && lng != null) {
                     location = LatLng(lat, lng)
                }
                Log.d(TAG, "markNearbyStands: ${stand.stand_name.toString()}")
                Log.d(TAG, "markNearbyStands: ${stand._id.toString()}")
                val id = stand._id.toString()
                Log.d(TAG, "markNearbyStands 2: $id")
                val stand_marker = MarkerOptions().title(stand.stand_name).position(location)
                val marker = map?.addMarker(stand_marker)
                if (marker != null) {
                    markerMap[marker] = id
                }
            }

            // Setup the info window click listener for the stands
            map?.setOnInfoWindowClickListener {
                markerListener(it)
            }
        }
    }
    private fun markerListener(marker : Marker) {
        val stand_id = markerMap.get(marker)
        if(stand_id != null) {
            val action = ViewNearbyStandsFragmentDirections.actionViewNearbyStandsFragmentToViewSingleStandFragment(stand_id)
            findNavController().navigate(action)
        }
    }

    private
    companion object {
        private val TAG = ViewNearbyStandsFragment::class.java.simpleName
        private const val DEFAULT_ZOOM = 15
        private const val PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION = 1

        // Keys for storing activity state.
        private const val KEY_CAMERA_POSITION = "camera_position"
        private const val KEY_LOCATION = "location"

        private const val MAX_NEARBY_DISTANCE = 1000    // meters

    }
}
