import * as React from 'react';
import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import PushNotification from "react-native-push-notification";
import axios from 'axios';


const DashboardScreen = ({navigation}) => {
    const [standName, setStandName] = React.useState([]);
    const [standHours, setStandHours] = React.useState([]);
    const [standCount, setStandCount] = React.useState(0);
    const [standIds, setStandIds] = React.useState([]);
    const [stands, setStands] = React.useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [hasError, setErrorFlag] = useState(false);
    const [firstLoad, setFirstLoad] = useState(true);
    
    useEffect(() => {
    const fetchSubscribedStands = async () => {
        if(firstLoad == true){
            const baseUrl = 'https://team6merchable.uc.r.appspot.com/';
            setIsLoading(true);
            axios.post(`${baseUrl}/api/management/`, {
                Email: global.email,
            })
            .then(function (response) {
                //console.log(response);
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
        }
        
        fetchSubscribedStands();

      }, [standCount]);

    // Stand hours format: DD/MM/YYYY, HH:MM - DD/MM/YYYY, HH:MM

    const setVariables = (response) => {
        setStandName(response.data.stand_names);
        setStandHours(response.data.stand_times);
        setStandIds(response.data.stand_ids);
        setStandCount(response.data.stand_count);

        var profiles = [];
        for(var i = 0; i < standCount; i++){
            profiles.push({key:i, id:standIds[i], standName:standName[i], standHours:standHours[i]});
        }

        setStands(profiles);
        setNotifications();
        setFirstLoad(false);
    }

    const setNotifications = () => {
        console.log("setNotifications")
        // console.log(standCount.toString())

        for (var i = 0; i < standCount; i++) {
            console.log(standHours[i])

            let hours = standHours[i].split("-")
            console.log(hours)

            // Calculate date + time for stand open hours
            let openTime = hours[0].slice(0, -1)
            let trimOpenTime = openTime.split(",");  // remove the comma from the datetime
            var openDate = new Date(trimOpenTime[0] + trimOpenTime[1]); 
            var openMilliseconds = openDate.getTime(); 

            // Calculate date + time for stand close hours
            let closeTime = hours[1].substring(1)
            let trimCloseTime = closeTime.split(",");  // remove the comma from the datetime
            var closeDate = new Date(trimCloseTime[0] + trimCloseTime[1]); 
            var closeMilliseconds = closeDate.getTime(); 

            console.log(standIds[i].substring(18))
            let standIdInt = parseInt(standIds[i].substring(18), 16)
			let standIdIntOpen = standIdInt * 10;
            // Stand open 
            if(Date.now() < openDate) {
                PushNotification.localNotificationSchedule({
                    id: JSON.stringify(standIdInt),
                    userInfo: { id: JSON.stringify(standIdInt)},
                    channelId: "subscribed-stands-channel",
                    title: "A stand is about to open",
                    message: standName[i] + " is about to open in 5 minutes",
                    date: new Date(openMilliseconds - 5 * 60 * 1000),
                    allowWhileIdle: true
                });
            }

			let standIdIntClose = (standIdInt * 10) + 1;
            // Stand close
            if(Date.now() < closeDate) {
                PushNotification.localNotificationSchedule({
                    id: JSON.stringify(standIdInt),
                    userInfo: { id: JSON.stringify(standIdInt)},
                    channelId: "subscribed-stands-channel",
                    title: "A stand is about to close",
                    message: standName[i] + " is about to close in 5 minutes",
                    date: new Date(closeMilliseconds - 5 * 60 * 1000),
                    allowWhileIdle: true
                });
            }

        }

    }

    return (
        <View style = {styles.container}>
            <TouchableOpacity style={styles.button} onPress = {() => navigation.navigate('Management Container')}>
                <Text style={styles.button}>MANAGEMENT</Text>
            </ TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress = {() => navigation.navigate('Create Stand')}>
                <Text style={styles.button}>CREATE STAND</Text>
            </ TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress = {() => navigation.navigate('Stand Container')}>
                <Text style={styles.button}>VIEW STANDS</Text>
            </ TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress = {() => navigation.navigate('View Nearby Stands')}>
                <Text style={styles.button}>VIEW NEARBY STANDS</Text>
            </ TouchableOpacity>
        </View>
    )
}

const styles = StyleSheet.create({
    container:{
      flex:1, 
      justifyContent:'center',
      alignItems:'center',
      backgroundColor: '#212529',
    },
    text:{
      fontSize: 36,
      fontWeight: "bold",
      //paddingBottom: 80,
      color: "#59bfff",
    },
    button:{
        borderRadius: 5,
        color: "white",
        backgroundColor: "#59bfff",
        width: 300,
        height: 40,
        textAlign: 'center',
        textAlignVertical: 'center',
        marginBottom: 30,
    },
  });

export default DashboardScreen;