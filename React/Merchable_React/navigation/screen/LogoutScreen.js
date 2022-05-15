import * as React from 'react';
import { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import auth from '@react-native-firebase/auth';
import axios from 'axios';

const LogoutScreen = (props) => {
    //const [signedIn, setSignedIn] = useState(true);

    const logout = () => {
        auth().signOut().then(() => console.log('User signed out!'));

        /*
        axios.get('${baseUrl}/api/logout/')
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
        */

        props.setSignedIn(false)
    }

    return (
        <View style = {styles.container}>
            <Text style = {styles.text}>Merchable</Text>
            <TouchableOpacity style={styles.button} onPress = {logout}>
                <Text style={styles.button}>LOGOUT</Text>
            </ TouchableOpacity>
        </View>
    )
}
 
const styles = StyleSheet.create({
    container:{
      flex:1, 
      justifyContent:'center',
      alignItems:'center',
      backgroundColor: '#212529'
    },
    text:{
      fontSize: 36,
      fontWeight: "bold",
      paddingBottom: 80,
      color: "#59bfff",
    },
    button:{
        borderRadius: 5,
        color: "white",
        backgroundColor: "#59bfff",
        width: 300,
        height: 40,
        textAlign: 'center',
        textAlignVertical: 'center'
    },
  });

export default LogoutScreen;