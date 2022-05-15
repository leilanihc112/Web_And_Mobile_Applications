import * as React from 'react';
import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView, Alert } from 'react-native';
import axios from 'axios';

const Stand = (props) => {
    const baseUrl = 'https://team6merchable.uc.r.appspot.com/';

    const unsubscribe =  async () => {
        axios.post(`${baseUrl}/api/view/stand/${props.id}/unsubscribe/`, {
          Email: global.email,
        } )
        .then(function (response) {
          //console.log(response);
          props.setResult(response);
          Alert.alert("Unsubscribed");
        })
        .catch(function (error) {
          //console.log(error);
          Alert.alert("Could not unsubscribe");
        });
    }

    return (
        <View>
            <TouchableOpacity onPress = {() => props.navigation.navigate('View Single Stand', {id: props.id, standLocation: props.standLocation})}>
                <Text style={styles.name}>{props.standName}</Text>
            </ TouchableOpacity>
            <Image 
                style = {styles.image}
                source={{uri: props.Images}} 
            />
            <Text style={styles.text}>
                Hours: {props.standHours}
            </Text>
            <Text style={styles.text}>
                Location: {props.standLocation}
            </Text>
            <TouchableOpacity style={[styles.button]} onPress = {unsubscribe}>
                <Text style={styles.button}>Unsubscribe</Text>
            </TouchableOpacity>
        </View>
    )
}

const Divider = () => {
    return (
        <View style={styles.divider}>
        </View>
    )
}

const ManagementScreen = ({navigation}) => {
    const [standName, setStandName] = React.useState([]);
    const [postHours, setPostHours] = React.useState([]);
    const [location, setLocation] = React.useState([]);
    const [standCount, setStandCount] = React.useState(0);
    const [image, setImage] = React.useState([]);
    const [standIds, setStandIds] = React.useState([]);
    const [stands, setStands] = React.useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [hasError, setErrorFlag] = useState(false);
    const [result, setResult] = useState(null);
    
    useEffect(() => {
        const baseUrl = 'https://team6merchable.uc.r.appspot.com/';

        const view = async () => {
            setIsLoading(true);
            axios.post(`${baseUrl}/api/management/`, {
                Email: global.email,
            })
            .then(function (response) {
                console.log(response);
                setVariables(response);
                setIsLoading(false);
                return;
            })
            .catch(function (error) {
                console.log(error);
                setErrorFlag(true);
                setIsLoading(false);
            });
        };

        view();
    }, [standCount, result]);

    const setVariables = (response) => {
        setStandName(response.data.stand_names);
        setPostHours(response.data.stand_times);
        setImage(response.data.stand_images);
        setLocation(response.data.stand_locations);
        setStandIds(response.data.stand_ids);
        setStandCount(response.data.stand_count);

        var profiles = [];
        for(var i = 0; i < standCount; i++){
            profiles.push(<Stand key={i} id={standIds[i]} standName={standName[i]} standHours={postHours[i]} standLocation={location[i]} 
                Images={image[i]} navigation={navigation} setResult={setResult}/>);
            profiles.push(<Divider key={1000 - i}/>);
        }

        setStands(profiles);
    }

    

    return (
        <ScrollView style = {styles.container}>
            <Text style={styles.header}>
                Subscribed Stands
            </Text>
            {!isLoading && !hasError && stands}
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
    header:{
        fontSize: 30,
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

export default ManagementScreen;