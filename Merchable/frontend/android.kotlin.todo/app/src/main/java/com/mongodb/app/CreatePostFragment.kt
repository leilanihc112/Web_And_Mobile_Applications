package com.mongodb.app

import android.app.Activity.RESULT_OK
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.text.TextUtils
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.navigation.findNavController
import androidx.navigation.fragment.navArgs
import com.google.android.material.textfield.TextInputEditText
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase
import com.mongodb.app.databinding.FragmentCreatePostBinding
import io.realm.RealmList
import io.realm.kotlin.where
import io.realm.mongodb.sync.Subscription
import org.bson.types.ObjectId
import java.util.*


/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class CreatePostFragment : Fragment() {

    private var _binding: FragmentCreatePostBinding? = null
    private lateinit var firebaseAuth: FirebaseAuth
    private val pickImage = 100
    private var imageUri: Uri? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentCreatePostBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        var create_post_stand_name: TextView = view.findViewById(R.id.create_post_stand_name)
        var photos_post: RealmList<String> = RealmList()

        // get stand
        val subscriptions = userRealm.subscriptions
        subscriptions.update { subscriptions ->
            subscriptions.addOrUpdate(
                Subscription.create(
                    "post-stand-search",
                    userRealm.where<stand>().isNotNull("_id")
                )
            )
        }

        subscriptions.waitForSynchronization()
        userRealm.refresh()

        val args: CreatePostFragmentArgs by navArgs()

        val curStand =
            userRealm.where<stand>().equalTo("_id", ObjectId(args.standId)).sort("_id").findAll().first()

        create_post_stand_name.text = (curStand!!).stand_name

        binding.buttonCreatePost.setOnClickListener {
            var create_post_post_title: TextInputEditText =
                view.findViewById(R.id.create_post_post_title)
            var create_post_post_text: TextInputEditText =
                view.findViewById(R.id.create_post_post_text)
            var create_post_post_tag: TextInputEditText =
                view.findViewById(R.id.create_post_post_tag)

            if (TextUtils.isEmpty(create_post_post_title.text)) {
                create_post_post_title.setError(" Please Enter Post Title ");
            } else {
                if (TextUtils.isEmpty(create_post_post_text.text)) {
                    create_post_post_text.setError(" Please Enter Post Text ");
                } else {
                    if (TextUtils.isEmpty(create_post_post_tag.text)) {
                        create_post_post_tag.setError(" Please Enter At Least One Tag ");
                    } else {
                        firebaseAuth = Firebase.auth

                        // get current user
                        val subscriptions = userRealm.subscriptions
                        subscriptions.update { subscriptions ->
                            subscriptions.addOrUpdate(
                                Subscription.create(
                                    "post-user-search",
                                    userRealm.where<user>().isNotNull("_id")
                                )
                            )
                        }

                        subscriptions.waitForSynchronization()
                        userRealm.refresh()

                        val firebaseUser = firebaseAuth.currentUser

                        val curUser =
                            userRealm.where<user>().equalTo("email", (firebaseUser!!).email)
                                .sort("_id")
                                .findAll().first()

                        var create_post_post_tags = create_post_post_tag.text.toString().split(", ")

                        val post = post()
                        post.title = create_post_post_title.text.toString()
                        post.text = create_post_post_text.text.toString()
                        post.stand = ObjectId(args.standId)
                        post.tags = RealmList<String>()

                        for (item in create_post_post_tags) {
                            if (item != "") {
                                post.tags.add(item)
                            }
                        }

                        post.photos =
                            RealmList<String>("https://storage.googleapis.com/team6merchable.appspot.com/default.png")
                        post._id = ObjectId()
                        post.timestamp = Date()
                        post.user = (curUser!!)._id

                        userRealm.executeTransactionAsync { realm ->
                            realm.insert(post)
                        }

                        val action =
                            CreatePostFragmentDirections.actionCreatePostToViewSingleStandFragment(
                                args.standId
                            )
                        view.findNavController().navigate(action)
                    }
                }
            }
        }

        // Camera
        view.findViewById<Button>(R.id.take_photos_button).setOnClickListener {
            val intent = Intent(activity, CameraXActivity::class.java)
            activity?.startActivity(intent)
        }

        // Upload photo
        view.findViewById<Button>(R.id.upload_photo_button).setOnClickListener {
            val gallery =
                Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI)
            activity?.startActivityForResult(gallery, pickImage)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == RESULT_OK && requestCode == pickImage) {
            imageUri = data?.data
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}