package com.mongodb.app

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.api.ApiException
import com.google.android.gms.tasks.Task
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.auth.GoogleAuthProvider
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase
import com.mongodb.app.databinding.ActivityLoginBinding
import io.realm.mongodb.Credentials
import io.realm.mongodb.auth.GoogleAuthType


class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding
    private lateinit var googleSignInClient: GoogleSignInClient
    private lateinit var firebaseAuth: FirebaseAuth

    // sign in launcher for Google sign in support
    private val signInLauncher: ActivityResultLauncher<Intent> =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult())
        { result ->
            val task: Task<GoogleSignInAccount> =
                GoogleSignIn.getSignedInAccountFromIntent(result.data)
            onSignInResult(task)
        }

    private companion object{
        private const val TAG = "GOOGLE_SIGN_IN_TAG"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        firebaseAuth = Firebase.auth

        //Google SignIn Button, Click to begin
        binding.googleSignInBtn.setOnClickListener{
            //begin Google SignIn
            Log.d(TAG, "onCreate: begin Google SignIn")
            googleSignIn()
        }
    }

    private fun googleSignIn() {
        // configure the Google SignIn
        val googleSignInOptions = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken(getString(R.string.default_web_client_id))
            .build()
        googleSignInClient = GoogleSignIn.getClient(this, googleSignInOptions)
        val signInIntent: Intent = googleSignInClient.signInIntent
        signInLauncher.launch(signInIntent)
    }

    private fun onSignInResult(completedTask: Task<GoogleSignInAccount>) {
        try {
            if (completedTask.isSuccessful) {
                val account: GoogleSignInAccount? = completedTask.getResult(ApiException::class.java)
                val token: String = account?.idToken!!
                Log.d(TAG(), token)
                val googleCredentials: Credentials =
                    Credentials.google(token, GoogleAuthType.ID_TOKEN)
                // sign in to realm with google credentials
                realmApp.loginAsync(googleCredentials) {
                    if (it.isSuccess) {
                        Log.v(TAG(),"Successfully logged in to MongoDB Realm using Google OAuth.")
                        // sign in to firebase to get user information later
                        val firebaseCredential = GoogleAuthProvider.getCredential(token, null)
                        firebaseAuth.signInWithCredential(firebaseCredential)
                            .addOnCompleteListener(this) { task ->
                                if (task.isSuccessful) {
                                    Log.d(TAG(), "signInWithCredential: success")
                                    val user = firebaseAuth.currentUser
                                    updateUI(user)
                                }
                                else {
                                    Log.w(TAG(), "signInWithCredential: failure", task.exception)
                                    updateUI(null)
                                }
                            }
                    } else {
                        Toast.makeText(this, "Sign In Failed", Toast.LENGTH_SHORT).show()
                        Log.e(TAG(), "Failed to log in to MongoDB Realm", it.error)
                    }
                }
            } else {
                Toast.makeText(this, "Sign In Failed", Toast.LENGTH_SHORT).show()
                Log.e(TAG(), "Google Auth failed: ${completedTask.exception}")
            }
        } catch (e: ApiException) {
            Toast.makeText(this, "Sign In Failed", Toast.LENGTH_SHORT).show()
            Log.e(TAG(), "Failed to authenticate using Google OAuth: " + e.message);
        }
    }

    private fun updateUI(user: FirebaseUser?) {
        if (user != null){
            //user is already logged in
            //start main activity
            Toast.makeText(this, "Signed in", Toast.LENGTH_SHORT).show()
            Log.i("updateUI", "Signed in")
            startActivity(Intent(this@LoginActivity, MainActivity::class.java))
            finish()
        }
        else{
            Toast.makeText(this, "Not signed in", Toast.LENGTH_SHORT).show()
            Log.i("updateUI", "Not signed in")
        }
    }
}