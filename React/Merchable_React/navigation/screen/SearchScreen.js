import * as React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView,TextInput } from 'react-native';
import { useState, useEffect } from 'react';
import axios from 'axios';



const Post = (props) => {
    return (
        <View>
            <TouchableOpacity onPress = {() => props.navigation.navigate('View Single Stand', {id: props.id})}>
                <Text style={styles.name}>{props.standName}</Text>
            </ TouchableOpacity>
            <Text style={styles.Title}>
                {props.Title}
            </Text>
            <Text style={styles.text}>
                {props.User}
            </Text>
            <Text style={styles.text}>
                Date: {props.Date}
            </Text>
            <Text style={styles.text}>
                {props.Description}
            </Text>
            <Text style={styles.name}>
                {props.Tags}
            </Text>
            <Image 
                style = {styles.image}
                source={{uri: props.Images}}
            />
        </View>
    )

}

const Divider = () => {
  return (
      <View style={styles.divider}>
      </View>
  )
}

const SearchScreen = ({navigation}) => {
  const baseUrl = 'https://team6merchable.uc.r.appspot.com/';
  const [tag, setTag] = React.useState("");
  const [postCount, setPostCount] = React.useState(0);
  const [standName, setStandName] = React.useState([]);
  const [postUser, setPostUser] = React.useState([]);
  const [postDate, setPostDate] = React.useState([]);
  const [tags, setTags] = React.useState([[]]);
  const [posts, setPosts] = React.useState([]);
  const [postData, setPostData] = React.useState([]);
  const [image, setImage] = React.useState([]);
  const [standIds, setStandIds] = React.useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasError, setErrorFlag] = useState(false);
  const [pressed, setPressed] = useState(false);

  useEffect(() => {
    const baseUrl = 'https://team6merchable.uc.r.appspot.com/';

    async function search(){
      setIsLoading(true);
      axios.get(`${baseUrl}/api/search/${tag.toLowerCase()}/`)
      .then(function (response) {
        //console.log(response)
        setVariables(response);
        setIsLoading(false);
      })
      .catch(function (error) {
        //console.log(error);
        setErrorFlag(true);
        setIsLoading(false);
      });
    }
    
    search();

  }, [tag, pressed]);

  const setVariables = (response) => {
    setStandName(response.data.post_stands_names);
    setPostCount(response.data.post_count);
    setPostData(response.data.posts);
    setPostUser(response.data.post_users);
    setPostDate(response.data.post_hours);
    setImage(response.data.post_image_names);
    setStandIds(response.data.stand_ids);
    var tagList = [];
    for(var i = 0; i < response.data.post_count; i++){
      tagList.push(response.data.posts[i].tags)
    }

    setTags(tagList);

    var profiles = [];
    for(var i = 0; i < postCount; i++){
      profiles.push(<Post key={i} standName={standName[i]} Title={postData[i].title} User={postUser[i]} Date={postDate[i]} Description={postData[i].text}
      Tags={"Tags: " + tags[i].toString()} Images={image[i][0]} id={standIds[i]}  navigation={navigation}/>, );
      profiles.push(<Divider key={1000 - i}/>);
    }

    setPosts(profiles);
  }

  const togglePressed = () => {
    if(pressed){
      setPressed(false);
    }else{
      setPressed(true);
    }
  }



    return (
      <ScrollView style = {styles.container}>
          <View style = {styles.textContainer}>
            <View style={styles.inputContainer}>
                <TextInput
                  style={styles.input}
                  onChangeText={setTag}
                  placeholder="Tag to Search!"
                  value={tag}
                />
            </View>
            <TouchableOpacity style={styles.button} onPress = {togglePressed}>
                <Text style={styles.button}>Search</Text>
            </ TouchableOpacity>
        </View>      
        {!isLoading && !hasError && posts}

      </ScrollView>
    )
}

const styles = StyleSheet.create({
  container:{
    flex:1, 
    paddingLeft: 10,
    paddingTop: 10,
    backgroundColor: '#212529'
  },
  textContainer:{
    flex:1, 
    paddingLeft: 10,
    paddingTop: 10,
    backgroundColor: '#212529',
    flexDirection:"row"
  },
  text:{
    fontSize: 18,
    color: "white",
  },
  name:{
    fontSize: 24,
    fontWeight: "bold",
    textDecorationLine:"underline",
    color: "white",
  },
  Title:{
    fontSize: 24,
    fontWeight: "bold",
    color: "white",
  },
  image:{
      width: 110,
      height: 110,
  },
  divider:{
      borderBottomColor: 'white',
      borderBottomWidth: StyleSheet.hairlineWidth,
      paddingTop: 10,
      paddingBottom: 10,
      paddingLeft: 10,
      paddingRight: 10,
  },
  button:{
    borderRadius: 5,
    color: "white",
    backgroundColor: "#59bfff",
    width: 100,
    height: 50,
    textAlign: 'center',
    textAlignVertical: 'center',
  },  
  input:{
    fontSize: 14,
    textAlign: 'center',
  },
  inputContainer:{
    marginBottom: 10,
    width: 250,
    backgroundColor: 'white',
  },
});

export default SearchScreen;