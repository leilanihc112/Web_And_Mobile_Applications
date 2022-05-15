package com.mongodb.app

import android.app.Application
import android.util.Log
import io.realm.BuildConfig

import io.realm.Realm
import io.realm.RealmConfiguration
import io.realm.log.LogLevel
import io.realm.log.RealmLog
import io.realm.mongodb.App
import io.realm.mongodb.AppConfiguration
import io.realm.mongodb.sync.ClientResetRequiredError
import io.realm.mongodb.sync.DiscardUnsyncedChangesStrategy
import io.realm.mongodb.sync.SyncConfiguration
import io.realm.mongodb.sync.SyncSession
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

lateinit var realmApp: App

// global Kotlin extension that resolves to the short version
// of the name of the current class. Used for labelling logs.
inline fun <reified T> T.TAG(): String = T::class.java.simpleName

lateinit var userRealm: Realm
lateinit var config: RealmConfiguration

/*
*  Sets up the Realm App and enables Realm-specific logging in debug mode.
*/
class App: Application() {

    override fun onCreate() {
        super.onCreate()
        Realm.init(this)
        realmApp = App(
            AppConfiguration.Builder(getString(R.string.realm_app_id))
                .defaultSyncClientResetStrategy(object : DiscardUnsyncedChangesStrategy {
                    override fun onBeforeReset(realm: Realm) {
                        Log.w("EXAMPLE", "Beginning client reset for " + realm.path)
                    }
                    override fun onAfterReset(before: Realm, after: Realm) {
                        Log.w("EXAMPLE", "Finished client reset for " + before.path)
                    }
                    override fun onError(session: SyncSession, error: ClientResetRequiredError) {
                        Log.e(
                            "EXAMPLE", "Couldn't handle the client reset automatically." +
                                    " Falling back to manual client reset execution: "
                                    + error.errorMessage
                        )
                        // close all instances of your realm -- this application only uses one
                        userRealm!!.close()
                        try {
                            Log.w("EXAMPLE", "About to execute the client reset.")
                            // execute the client reset, moving the current realm to a backup file
                            error.executeClientReset()
                            Log.w("EXAMPLE", "Executed the client reset.")
                        } catch (e: java.lang.IllegalStateException) {
                            Log.e("EXAMPLE", "Failed to execute the client reset: " + e.message)
                            // The client reset can only proceed if there are no open realms.
                            // if execution failed, ask the user to restart the app, and we'll client reset
                            // when we first open the app connection.
                        }
                        // open a new instance of the realm. This initializes a new file for the new realm
                        // and downloads the backend state. Do this in a background thread so we can wait
                        // for server changes to fully download.
                        val executor = Executors.newSingleThreadExecutor()
                        executor.execute {
                            val newRealm = Realm.getInstance(config)
                            // ensure that the backend state is fully downloaded before proceeding
                            try {
                                realmApp!!.sync.getSession(config as SyncConfiguration)
                                    .downloadAllServerChanges(
                                        10000,
                                        TimeUnit.MILLISECONDS
                                    )
                            } catch (e: InterruptedException) {
                                e.printStackTrace()
                            }
                            Log.w(
                                "EXAMPLE",
                                "Downloaded server changes for a fresh instance of the realm."
                            )
                            newRealm.close()
                        }
                        // execute the recovery logic on a background thread
                        try {
                            executor.awaitTermination(20000, TimeUnit.MILLISECONDS)
                        } catch (e: InterruptedException) {
                            e.printStackTrace()
                        }
                    }
                })
                .baseUrl(getString(R.string.realm_base_url))
                .build())

        // Enable more logging in debug mode
        if (BuildConfig.DEBUG) {
            RealmLog.setLevel(LogLevel.DEBUG)
        }

        Log.v(TAG(), "Initialized the Realm App configuration for: ${realmApp.configuration.appId}")
    }
}
