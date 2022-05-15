import * as React from 'react';
import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView, Alert } from 'react-native';
import axios from 'axios';
import PushNotification from "react-native-push-notification";

const Stand = (props) => {
  const createNotification = () => {
    console.log(props.Date)
    let hours = props.Date.split("-")
    console.log(hours)

    // Calculate date + time for stand open hours
    let openTime = hours[0].slice(0, -1)
    let trimOpenTime = openTime.split(",");  // remove the comma from the datetime
    var openDate = new Date(trimOpenTime[0] + trimOpenTime[1]); 
    //console.log(openDate)
    var openMilliseconds = openDate.getTime(); 

    // Calculate date + time for stand close hours
    let closeTime = hours[1].substring(1)
    let trimCloseTime = closeTime.split(",");  // remove the comma from the datetime
    var closeDate = new Date(trimCloseTime[0] + trimCloseTime[1]); 
    //console.log(closeDate)
    var closeMilliseconds = closeDate.getTime(); 

    console.log(props._id)
    console.log(props.standName)

    console.log(props._id.substring(18))
    let standIdInt = parseInt(props._id.substring(18), 16)
    let standIdIntOpen = standIdInt * 10;
    // Stand open 
    if(Date.now() < openDate) {
        PushNotification.localNotificationSchedule({
            id: JSON.stringify(standIdIntOpen),
            userInfo: { id: JSON.stringify(standIdIntOpen)},
            channelId: "subscribed-stands-channel",
            title: "A stand is about to open",
            message: props.standName + " is about to open in 5 minutes",
            date: new Date(openMilliseconds - 5 * 60 * 1000),
            allowWhileIdle: true
        });
    }

    let standIdIntClose = (standIdInt * 10) + 1;
    // Stand close
    if(Date.now() < closeDate) {
        PushNotification.localNotificationSchedule({
            id: JSON.stringify(standIdIntClose),
            userInfo: { id: JSON.stringify(standIdIntClose)},
            channelId: "subscribed-stands-channel",
            title: "A stand is about to close",
            message: props.standName + " is about to close in 5 minutes",
            date: new Date(closeMilliseconds - 5 * 60 * 1000),
            allowWhileIdle: true
        });
    }
  }

  const baseUrl = 'https://team6merchable.uc.r.appspot.com/';

  const subscribe =  async () => {
    axios.post(`${baseUrl}/api/view/stand/${props._id}/subscribe/`, {
      Email: global.email,
    } )
    .then(function (response) {
      //console.log(response);
      props.setSub("Unsubscribe");
      Alert.alert("Subscribed");
      createNotification();
    })
    .catch(function (error) {
      console.log(error);
      Alert.alert("Could not subscribe");
    });
  }

  const unsubscribe =  async () => {
    axios.post(`${baseUrl}/api/view/stand/${props._id}/unsubscribe/`, {
      Email: global.email,
    } )
    .then(function (response) {
      //console.log(response);
      props.setSub("Subscribe");
      console.log(props._id.substring(18))
      let standIdInt = parseInt(props._id.substring(18), 16)
      standIdInt = standIdInt * 10;
      let standIdStr = standIdInt.toString();
      PushNotification.cancelLocalNotification(standIdStr);
      standIdInt = standIdInt + 1;
      standIdStr = standIdInt.toString();
      PushNotification.cancelLocalNotification(standIdStr);
      Alert.alert("Unsubscribed");
    })
    .catch(function (error) {
      //console.log(error);
      Alert.alert("Could not unsubscribe");
    });

  }

    return (
      <View>
          <Text style={styles.name}>
              {props.standName}
          </Text>
          <Image 
              style = {styles.image}
              source={{uri: props.Image}} 
          />
          <Text style={styles.text}>
              {props.User}
          </Text>
          <View style={{ flexDirection:"row", justifyContent: "center", margin: 20 }}>
            <TouchableOpacity style={[styles.button, {marginRight: 30}]} onPress = {() => props.navigation.navigate('Create Post', 
              {
                id: props.id, 
                standName: props.standName,
              })}
            >
                <Text style={styles.button}>Create Post</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress = {props.isSub ? unsubscribe : subscribe}>
                <Text style={styles.button}>{props.sub}</Text>
            </TouchableOpacity>
          </View>
          <Text style={styles.text}>
              Hours: {props.Date}
          </Text>
          <Text style={styles.text}>
              Location: {props.standLocation}
          </Text>
      </View>
  ) 
}

const Post = (props) => {
  if(props.imageExists){
    return (
      <View>
          <Text style={styles.name}>
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
          <Text style={styles.tag}>
              {props.Tags}
          </Text>
          <Image 
                style = {styles.image}
                source={{uri: props.Images}}
            />
      </View>
    )
  }else{
    return (
      <View>
          <Text style={styles.name}>
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
          <Text style={styles.tag}>
              {props.Tags}
          </Text>
      </View>
    )
  }
}

const Divider = () => {
  return (
      <View style={styles.divider}>
      </View>
  )
}

const ViewSingleStandScreen = ({route, navigation}) => {
  const { id, standLocation } = route.params;
  
  const [posts, setPosts] = React.useState([]);
  const [postUser, setPostUser] = React.useState([]);
  const [postDate, setPostDate] = React.useState([]);
  const [postData, setPostData] = React.useState([]);
  const [postCount, setPostCount] = React.useState(0);
  const [sub, setSub] = useState("Subscribe");

  const [creator, setCreator] = React.useState(undefined);
  const [standName, setStandName] = React.useState(undefined);
  const [image, setImage] = React.useState(undefined);
  const [standDate, setStandDate] = React.useState(undefined);
  const [stand, setStand] = React.useState([]);

  const [isLoading, setIsLoading] = useState(false);
  const [hasError, setErrorFlag] = useState(false);
  const [loadSub, setLoadSub] = useState(true);



  const baseUrl = 'https://team6merchable.uc.r.appspot.com/';


  useEffect(() => {
    const view = async () => {
        setIsLoading(true);
        axios.post(`${baseUrl}/api/view/stand/${id}/`, {
          Email: global.email,
        })
        .then(function (response) {
            if(loadSub){
              setLoadSub(false);
              setSubscribeState(response);
            }

            setVaraibles(response);
            setIsLoading(false);

            //console.log(response.data.post_count);
            //console.log(response);
            return;
        })
        .catch(function (error) {
            //console.log(error);
            setErrorFlag(true);
            setIsLoading(false);
        });
    };

    view();
  }, [sub, postCount, creator]);

  const setSubscribeState = (response) => {
    if(response.data.isSub){
      setSub("Unsubscribe");
    }else{
      setSub("Subscribe");
    }
  }

  const setVaraibles = (response) => {
    //Stand
    setStandName(response.data.stand_name);
    setImage(response.data.image_name)
    setStandDate(response.data.time);
    setCreator(response.data.creator);
    
    //Posts
    setPostData(response.data.posts);
    setPostUser(response.data.post_users);
    setPostDate(response.data.post_hours);
    setPostCount(response.data.post_count);
    
    var tagList = [];
    var titleList = [];
    var descriptionList = [];
    var imageList = [];
    var imageExists = [];

    for(var i = 0; i < response.data.post_count; i++){
      tagList.push(response.data.posts[i].tags);
      titleList.push(response.data.posts[i].title);
      descriptionList.push(response.data.posts[i].text);
      imageList.push(response.data.post_image_names[i][0])
      if(typeof response.data.post_image_names[i][0] != "undefined"){
        imageExists.push(true);
      }else{
        imageExists.push(false);
      }
    }
  
    if(typeof response != "undefined"){
      //Make Stand
      var profile = [];
      profile.push(<Stand key={1} id={id} navigation={navigation} standName={standName} sub = {sub} setSub={setSub}
        Image={image} User={creator} Date={standDate} standLocation={standLocation} _id={id} isSub={response.data.isSub}/>);
      profile.push(<Divider key={2}/>);

      setStand(profile);

      //Make Post
      var profiles = [];
      for(var i = 0; i < response.data.post_count; i++){
        profiles.push(<Post key={i} Title={titleList[i]} User={postUser[i]} Date={postDate[i]} Description={descriptionList[i]} 
            Tags={"Tags: " + tagList[i]} Images={imageList[i]} imageExists = {imageExists[i]}/>);
        profiles.push(<Divider key={1000 - i}/>);
      }
      
      setPosts(profiles);
    }
  }      

    return (
        <ScrollView style = {styles.container}>
          {!isLoading && !hasError && stand}  
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
  text:{
    fontSize: 18,
    color: "white",
  },
  tag:{
    fontSize: 18,
    color: "white",
    fontWeight: "bold",
  },
  name:{
    fontSize: 24,
    fontWeight: "bold",
    textDecorationLine:"underline",
    color: "white",
    paddingTop: 10,
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
  });

export default ViewSingleStandScreen;