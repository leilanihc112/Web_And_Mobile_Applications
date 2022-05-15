import * as React from 'react';
import { useState, useEffect } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  useColorScheme,
  View,
  Button,
  Image
} from 'react-native';
import { GoogleSignin, GoogleSigninButton } from '@react-native-google-signin/google-signin';
import auth from '@react-native-firebase/auth';
import axios from 'axios';
import PushNotification from "react-native-push-notification";

const Login = (props) => {
  const baseUrl = 'https://team6merchable.uc.r.appspot.com/';

  GoogleSignin.configure({
    webClientId: '1012349947363-8neuet7lefkhr3a1edhf6r85jafo71jh.apps.googleusercontent.com',
  });

  useEffect(() => {
    createChannels();
  }, []);

  const signInWithGoogleAsync = async () => {
    // Get the users ID token
    const { idToken } = await GoogleSignin.signIn();

    //console.log(idToken);

    /*
    axios.get(`${baseUrl}/api/search/shirt/`)
      .then(function (response) {
        console.log(response.data.post_count);
      })
      .catch(function (error) {
        //console.log(error);
      });
    */

    // Create a Google credential with the token
    const googleCredential = auth.GoogleAuthProvider.credential(idToken);

    // Sign-in the user with the credential
    const user_sign_in = auth().signInWithCredential(googleCredential);

    user_sign_in.then((user)=>{
     //console.log(user.additionalUserInfo.profile.email);
      props.sendUserToParent(user)
      props.setSignedIn(true);
    })
    .catch((error)=>{
      console.log(error)
    })

  }

  const createChannels = () => {
    PushNotification.createChannel(
      {
        channelId: "subscribed-stands-channel",
        channelName: "Subscribed Stands Channel"
      })
  }

  return (
    <View style = {styles.container}>
      <Image 
        style = {styles.image}
        source={require('./img/merchable_logo_white.png')} 
      />
      <Text style = {styles.text}>Merchable</Text>
      <GoogleSigninButton style = {styles.button}
        title='Sign in with Google'
        onPress={signInWithGoogleAsync}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container:{
    flex:1, 
    justifyContent:'center',
    alignItems:'center',
    backgroundColor: '#59bfff'
  },
  text:{
    color: 'white',
    fontSize: 30,
    fontWeight: "bold",
    paddingBottom: 160,
  },
  image:{
    width: 130,
    height: 110,
  },
  button:{
    width: 120,
  }
});

export default Login;
