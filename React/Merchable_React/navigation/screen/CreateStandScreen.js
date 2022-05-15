import * as React from 'react';
import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, TextInput, ScrollView, Alert, Platform, PermissionsAndroid } from 'react-native';
import DateTimePickerModal from "react-native-modal-datetime-picker";
import * as ImagePicker from "react-native-image-picker";
import GetLocation from 'react-native-get-location'
import axios from 'axios';
import moment from "moment";

const CreateStandScreen = ({navigation}) => {
  const [name, setName] = React.useState("");
  const [inventory, setInventory] = React.useState("");
  const [longtiude, setLongitude] = React.useState("");
  const [latitude, setLatitude] = React.useState("");
  const [open, setOpen] = useState(null);
  const [close, setClose] = useState(null);
  const [imageSource, setImageSource] = useState(null);
  const [isDatePickerVisibleOpen, setDatePickerVisibilityOpen] = useState(false);
  const [isDatePickerVisibleClose, setDatePickerVisibilityClose] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [locationFlag, setLocationFlag] = useState(false);

  const baseUrl = 'https://team6merchable.uc.r.appspot.com';
    

    const showDatePickerOpen = () => {
      setDatePickerVisibilityOpen(true);
    };

    const hideDatePickerOpen = () => {
      setDatePickerVisibilityOpen(false);
    };

    const handleConfirmOpen = (date) => {
      setOpen(date);
      hideDatePickerOpen();
    };

    const showDatePickerClose = () => {
      setDatePickerVisibilityClose(true);
    };

    const hideDatePickerClose = () => {
      setDatePickerVisibilityClose(false);
    };

    const handleConfirmClose = (date) => {
      setClose(date);
      hideDatePickerClose();
    };

    
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

  const _getCourts = () => {
    GetLocation.getCurrentPosition({
      enableHighAccuracy: true,
      timeout: 15000,
    })
    .then(location => {
        //console.log(location);
        setLatitude(location.latitude);
        setLongitude(location.longitude);
    })
    .catch(error => {
        const { code, message } = error;
        console.warn(code, message);
    })
  }

  useEffect(() => {
    const requestLocationPermission = async () => {
      if (Platform.OS === 'ios') {
        const auth = await Geolocation.requestAuthorization('whenInUse');
        if (auth === 'granted') {
          _getCourts();
        }
      }
      
      if (Platform.OS === 'android') {
        try{
          const granted = await PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
              {
                title: 'Location Access Required',
                message: 'This App needs to Access your location',
              },
            );
          if (granted === PermissionsAndroid.RESULTS.GRANTED) {
            _getCourts();
          } else {
            console.log(granted);
          }
        } catch (err) {
            console.warn(err);
        }
      }
    }

    requestLocationPermission();
  }, [locationFlag]);

  const clickedCreate = () => {
    setLocationFlag(!locationFlag);
    createStand();
  }

  

  const createStand = () => {
    if(latitude != "" && longtiude != ""){
      if(name == "" || open == null || close == null){
        Alert.alert("Populate all fields");
      }else{
        setIsLoading(true);
        axios.post(`${baseUrl}/api/create_stand/`, {
          Email: global.email,
          StandName: name,
          Latitude: latitude,
          Longitude: longtiude,
          Inventory: inventory,
          OpenDate: moment(open,"yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",true).format("yyyy-MM-DDTHH:mm"),
          CloseDate: moment(close,"yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",true).format("yyyy-MM-DDTHH:mm"),
        } )
        .then(function (response) {
          console.log(response);
          Alert.alert("Stand created");
          setIsLoading(false);
        })
        .catch(function (error) {
          console.log(error);
          Alert.alert("Error creating stand");
          setIsLoading(false);
        });
        //img:'<img>'
      }
    }
  };

    return (
        <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: 'center', alignItems: "center", backgroundColor: '#212529'}}>
            <Text style={styles.text_required}>Fields marked with an * are required</Text>
            <Text style={styles.text}>*Stand Name</Text>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                onChangeText={setName}
                editable={!isLoading}
                placeholder="Insert a stand name"
                value={name}
              />
            </View>
            <Text style={styles.text}>Inventory (separate items by comma)</Text>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                onChangeText={setInventory}
                editable={!isLoading}
                placeholder="Insert item"
                value={inventory}
              />
            </View>
            <Text style={styles.text}>*Opens</Text>
            <TouchableOpacity style={styles.date}  disabled={isLoading} onPress={showDatePickerOpen}>
                <Text style={styles.date}>CHOOSE DATE</Text>
            </ TouchableOpacity>
            <DateTimePickerModal
              isVisible={isDatePickerVisibleOpen}
              mode="datetime"
              onConfirm={handleConfirmOpen}
              onCancel={hideDatePickerOpen}
            />
            <Text style={styles.text}>*Closes</Text>
            <TouchableOpacity style={styles.date}  disabled={isLoading} onPress={showDatePickerClose}>
                <Text style={styles.date}>CHOOSE DATE</Text>
            </ TouchableOpacity>
            <DateTimePickerModal 
              isVisible={isDatePickerVisibleClose}
              mode="datetime"
              onConfirm={handleConfirmClose}
              onCancel={hideDatePickerClose}
            />
            <TouchableOpacity style={styles.date} disabled={isLoading} onPress={selectImage}>
                <Text style={styles.date}>LAUNCH CAMERA</Text>
            </ TouchableOpacity>
            <TouchableOpacity style={styles.button} disabled={isLoading} onPress={clickedCreate}>
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
    button:{
      borderRadius: 5,
      color: "white",
      backgroundColor: "#59bfff",
      width: 300,
      height: 40,
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
    date:{
      borderRadius: 7,
      color: "white",
      backgroundColor: "#2196F3",
      width: 150,
      height: 40,
      textAlign: 'center',
      textAlignVertical: 'center',
      marginBottom: 10,
    },
  });

export default CreateStandScreen;