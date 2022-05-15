package com.mongodb.app

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.MenuItem
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase
import com.mongodb.app.LoginActivity
import com.mongodb.app.R
import com.mongodb.app.databinding.ActivityMainBinding
import io.realm.Realm
import io.realm.RealmList
import io.realm.kotlin.where
import io.realm.mongodb.sync.Subscription
import io.realm.mongodb.sync.SyncConfiguration
import org.bson.types.ObjectId
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {

    //view bidding
    private lateinit var binding: ActivityMainBinding

    //firebase auth
    private lateinit var firebaseAuth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSupportActionBar(binding.toolbar)

        //init firebase auth
        firebaseAuth = FirebaseAuth.getInstance()
        checkUserLogIn()

        //handle click, logout user
        binding.logoutBtn.setOnClickListener{
            realmApp.currentUser()?.logOutAsync {
                if (it.isSuccess) {
                    Log.v(TAG(), "user logged out")
                    firebaseAuth.signOut()
                    userRealm.close()
                    startActivity(Intent(this, LoginActivity::class.java))
                } else {
                    Log.e(TAG(), "log out failed! Error: ${it.error}")
                }
            }
        }

        val navView: BottomNavigationView = binding.navView

        val navController = findNavController(R.id.nav_host_fragment_activity_main)
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        val appBarConfiguration = AppBarConfiguration(
            setOf( R.id.navigation_home, R.id.navigation_dashboard, R.id.navigation_search )
        )
        setupActionBarWithNavController(navController, appBarConfiguration)
        navView.setupWithNavController(navController)
    }

    override fun onOptionsItemSelected(item: MenuItem) : Boolean {
        if (item.itemId == android.R.id.home) {
            onBackPressed()
            return true
        }
        else {
            return super.onOptionsItemSelected(item)
        }
    }

    private fun checkUserLogIn(){
        val user = realmApp.currentUser()
        if (user == null) {
            startActivity(Intent(this, LoginActivity::class.java))
            Log.d(TAG(), "User not logged in Realm")
        }
        else {
            config = SyncConfiguration.Builder(user)
                .waitForInitialRemoteData(
                    2112,
                    TimeUnit.MILLISECONDS
                )
                .build()
            Realm.getInstanceAsync(config, object : Realm.Callback() {
                override fun onSuccess(realm: Realm) {
                    userRealm = realm
                    Log.d(TAG(), "Successfully connected to Realm.")

                    // add user to database
                    val new_user = user()

                    val firebaseUser = firebaseAuth.currentUser

                    if (firebaseUser == null){
                        userRealm.close()
                        //user not logged in
                        startActivity(Intent(this@MainActivity, LoginActivity::class.java))
                    }
                    else {
                        Log.d(TAG(), "Updating subscriptions")
                        val subscriptions = userRealm.subscriptions
                        // remove all current subscriptions
                        subscriptions.update { subscriptions ->
                            subscriptions.removeAll()
                        }
                        subscriptions.waitForSynchronization()
                        userRealm.refresh()

                        // subscribe to users and find if user exists already in database or not
                        subscriptions.update { subscriptions ->
                            subscriptions.addOrUpdate(
                                Subscription.create(
                                    "users-search",
                                    realm.where<user>()
                                        .equalTo("email", firebaseUser.email)
                                )
                            )
                        }

                        Log.d(TAG(), "Subscriptions updated")

                        // sync first
                        subscriptions.waitForSynchronization()
                        userRealm.refresh()

                        val curUser = userRealm.where<user>().count()

                        Log.d(TAG(), "Got count of users with current email")

                        // if the user does not exist, add them to the user database
                        if (curUser.equals(0)) {
                            new_user._id = ObjectId()
                            new_user.username = firebaseUser.displayName
                            new_user.email = firebaseUser.email
                            new_user.subscribed_stands = RealmList()

                            userRealm.executeTransactionAsync { realm ->
                                realm.insert(new_user)
                            }

                            Log.d(TAG(), "Inserted user into database")

                            // remove subscription
                            subscriptions.update { subscriptions ->
                                subscriptions.removeAll()
                            }
                            subscriptions.waitForSynchronization()
                            userRealm.refresh()
                        }
                        else {
                            Log.d(TAG(), "User already exists")
                        }
                    }
                }
            })
        }
    }
}