package com.mongodb.app

import android.os.Bundle
import android.text.TextUtils
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.navigation.findNavController
import androidx.navigation.fragment.navArgs
import com.google.android.material.textfield.TextInputEditText
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase
import com.mongodb.app.databinding.FragmentCreateStandBinding
import io.realm.RealmList
import io.realm.kotlin.where
import io.realm.mongodb.sync.Subscription
import org.bson.types.ObjectId
import java.text.ParseException
import java.text.SimpleDateFormat
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.time.format.DateTimeParseException
import java.util.*


/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class CreateStandFragment : Fragment() {

    private var _binding: FragmentCreateStandBinding? = null
    private lateinit var firebaseAuth: FirebaseAuth

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentCreateStandBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val defaultZoneId = ZoneId.systemDefault()

        binding.buttonCreateStand.setOnClickListener {
            var create_stand_stand_name: TextInputEditText =
                view.findViewById(R.id.create_stand_stand_name)
            var create_stand_latitude: TextInputEditText =
                view.findViewById(R.id.create_stand_latitude)
            var create_stand_longitude: TextInputEditText =
                view.findViewById(R.id.create_stand_longitude)
            var create_stand_inventory: TextInputEditText =
                view.findViewById(R.id.create_stand_inventory)
            var create_stand_opens: TextInputEditText = view.findViewById(R.id.create_stand_opens)
            var create_stand_closes: TextInputEditText = view.findViewById(R.id.create_stand_closes)
            val formatter = DateTimeFormatter.ofPattern("MM/dd/yyyy HH:mm")

            if (TextUtils.isEmpty(create_stand_stand_name.text.toString())) {
                create_stand_stand_name.setError(" Please Enter Stand Name ");
            } else {
                if (TextUtils.isEmpty(create_stand_latitude.text.toString())) {
                    create_stand_latitude.setError(" Please Enter Latitude ");
                } else {
                    if (create_stand_latitude.text.toString()
                            .toDouble() < -90 || create_stand_latitude.text.toString()
                            .toDouble() > 90
                    ) {
                        create_stand_latitude.setError(" Please Enter a Number from -90 to 90 ")
                    } else {
                        if (TextUtils.isEmpty(create_stand_longitude.text.toString())) {
                            create_stand_longitude.setError(" Please Enter Longitude ");
                        } else {
                            if (create_stand_longitude.text.toString()
                                    .toDouble() < -180 || create_stand_longitude.text.toString()
                                    .toDouble() > 180
                            ) {
                                create_stand_longitude.setError(" Please Enter a Number from -180 to 180 ")
                            } else {
                                if (TextUtils.isEmpty(create_stand_inventory.text.toString())) {
                                    create_stand_inventory.setError(" Please Enter At Least One Item ")
                                } else {
                                    if (TextUtils.isEmpty(create_stand_opens.text)) {
                                        create_stand_opens.setError(" Please Enter Open Date Time ");
                                    } else {
                                        try {
                                            LocalDateTime.parse(
                                                create_stand_opens.text.toString(),
                                                formatter
                                            )
                                            if (TextUtils.isEmpty(create_stand_closes.text)) {
                                                create_stand_closes.setError(" Please Enter Close Date Time ");
                                            } else {
                                                try {
                                                    LocalDateTime.parse(
                                                        create_stand_closes.text.toString(),
                                                        formatter
                                                    )
                                                    if (Date.from(
                                                            LocalDateTime.parse(
                                                                create_stand_opens.text.toString(),
                                                                formatter
                                                            ).atZone(defaultZoneId).toInstant()
                                                        ).after(
                                                            Date.from(
                                                                LocalDateTime.parse(
                                                                    create_stand_closes.text.toString(),
                                                                    formatter
                                                                ).atZone(defaultZoneId).toInstant()
                                                            )
                                                        )
                                                    ) {
                                                        create_stand_closes.setError(" Close date time must be after Open date time ")
                                                    } else {
                                                        firebaseAuth = Firebase.auth

                                                        // get current user
                                                        val subscriptions = userRealm.subscriptions
                                                        subscriptions.update { subscriptions ->
                                                            subscriptions.addOrUpdate(
                                                                Subscription.create(
                                                                    "stand-user-search",
                                                                    userRealm.where<user>()
                                                                        .isNotNull("_id")
                                                                )
                                                            )
                                                        }

                                                        subscriptions.waitForSynchronization()
                                                        userRealm.refresh()

                                                        val firebaseUser = firebaseAuth.currentUser

                                                        val curUser =
                                                            userRealm.where<user>()
                                                                .equalTo(
                                                                    "email",
                                                                    (firebaseUser!!).email
                                                                )
                                                                .sort("_id")
                                                                .findAll().first()

                                                        var create_stand_inventory =
                                                            create_stand_inventory.text.toString()
                                                                .split(", ")

                                                        val stand = stand()
                                                        stand.stand_name =
                                                            create_stand_stand_name.text.toString()
                                                        stand.user = (curUser!!)._id
                                                        stand._id = ObjectId()
                                                        stand.inventory_list = RealmList()

                                                        for (item in create_stand_inventory) {
                                                            if (item != "") {
                                                                Log.d(TAG(), item)
                                                                var curItem = item()
                                                                curItem._id = ObjectId()
                                                                curItem.item_name = item
                                                                curItem.available = false
                                                                stand.inventory_list.add(curItem._id)
                                                                userRealm.executeTransactionAsync({ realm ->
                                                                    realm.insert(curItem)
                                                                    Log.d(
                                                                        TAG(),
                                                                        "Inserted item"
                                                                    )
                                                                },
                                                                    {
                                                                        Log.v(
                                                                            TAG(),
                                                                            "Successfully completed the transaction"
                                                                        )
                                                                    },
                                                                    { error ->
                                                                        Log.e(
                                                                            TAG(),
                                                                            "Failed the transaction: $error"
                                                                        )
                                                                    })
                                                            }
                                                        }

                                                        stand.location = RealmList()
                                                        stand.location.add(
                                                            create_stand_latitude.text.toString()
                                                                .toDouble()
                                                        )
                                                        stand.location.add(
                                                            create_stand_longitude.text.toString()
                                                                .toDouble()
                                                        )

                                                        stand.date_time_closed = Date.from(
                                                            LocalDateTime.parse(
                                                                create_stand_closes.text.toString(),
                                                                formatter
                                                            )
                                                                .atZone(defaultZoneId).toInstant()
                                                        )
                                                        stand.date_time_open = Date.from(
                                                            LocalDateTime.parse(
                                                                create_stand_opens.text.toString(),
                                                                formatter
                                                            )
                                                                .atZone(defaultZoneId).toInstant()
                                                        )

                                                        stand.photo =
                                                            "https://storage.googleapis.com/team6merchable.appspot.com/default.png"

                                                        userRealm.executeTransactionAsync { realm ->
                                                            realm.insert(stand)
                                                            Log.d(TAG(), "Inserted stand")
                                                        }
                                                    }
                                                } catch (e: DateTimeParseException) {
                                                    create_stand_closes.setError(" Close date time format must be MM/DD/YYYY HH:MM ")
                                                    Log.e(TAG(), e.toString())
                                                }
                                            }
                                        } catch (e: DateTimeParseException) {
                                            create_stand_opens.setError(" Open date time format must be MM/DD/YYYY HH:MM ")
                                            Log.e(TAG(), e.toString())
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}