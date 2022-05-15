import * as React from 'react';
import { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView, Alert, } from 'react-native';
import * as ImagePicker from "react-native-image-picker";
import axios from 'axios';

const CreatePostScreen = ({route, navigation}) => {
  const [tags, setTags] = React.useState("");
  const [title, setTitle] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [imageSource, setImageSource] = useState(null);

  const baseUrl = 'https://team6merchable.uc.r.appspot.com';
  const { id, standName } = route.params;

    
  const selectImage = () => {
    let options = {
      title: 'You can choose one image',
      maxWidth: 256,
      maxHeight: 256,
      includeBase64: true,
      storageOptions: {
        skipBackup: true
      }
    };

    ImagePicker.launchCamera(options, response => {
      console.log({ response });

      if (response.didCancel) {
        console.log('User cancelled photo picker');
        Alert.alert('You did not select any image');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
      } else {
        let source = { uri: response.uri };
        console.log({ source });
      }
    });
  }

  const createPost = () => {
    if(title == "" || description == ""){
        Alert.alert("Populate all fields");
    }else{
        axios.post(`${baseUrl}/api/add_post/`, {
            Email: global.email,
            PostTitle: title,
            post_description: description,
            stand_id: id,
            PostTags: tags,
        } )
        .then(function (response) {
            console.log(response);
            Alert.alert("Post created");
        })
        .catch(function (error) {
            console.log(error);
            Alert.alert("Error creating stand");
        });
    }
  };

    return (
        <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: 'center', alignItems: "center", backgroundColor: '#212529'}}>
            <Text style={styles.text_required}>Fields marked with an * are required</Text>
            <Text style={styles.text}>Stand Name: {standName}</Text>
            <Text style={styles.text}>Post Tags</Text>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                onChangeText={setTags}
                placeholder="Add Post Tags"
                value={tags}
              />
            </View>
            <Text style={styles.text}>*Post Title</Text>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                onChangeText={setTitle}
                placeholder="Add Post Title"
                value={title}
              />
            </View>
            <Text style={styles.text}>*Post Description</Text>
            <View style={styles.descriptionContainer}>
              <TextInput
                style={styles.input}
                onChangeText={setDescription}
                value={description}
              />
            </View>
            <TouchableOpacity style={styles.pbutton}  onPress={selectImage}>
                <Text style={styles.pbutton}>LAUNCH CAMERA</Text>
            </ TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={createPost}>
                <Text style={styles.button}>CREATE</Text>
            </ TouchableOpacity>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    container:{
      flex:1, 
      justifyContent:'center',
      alignItems:'center',
      backgroundColor: '#212529'
    },
    text_required:{
      fontSize: 12,
      paddingBottom: 10,
      color: "white",
    },
    text:{
      fontSize: 18,
      paddingBottom: 20,
      color: "white",
    },
    pbutton:{
      borderRadius: 5,
      color: "white",
      backgroundColor: "#59bfff",
      width: 200,
      height: 40,
      marginBottom: 10,
      textAlign: 'center',
      textAlignVertical: 'center',
    },
    button:{
      borderRadius: 5,
      color: "white",
      backgroundColor: "#59bfff",
      width: 300,
      height: 40,
      marginBottom: 10,
      textAlign: 'center',
      textAlignVertical: 'center',
    },
    input:{
      fontSize: 14,
      textAlign: 'center',
    },
    inputContainer:{
      marginBottom: 10,
      width: 300,
      backgroundColor: 'white',
    },
    descriptionContainer:{
      marginBottom: 10,
      width: 300,
      height: 175,
      backgroundColor: 'white',
    },
  });

export default CreatePostScreen;