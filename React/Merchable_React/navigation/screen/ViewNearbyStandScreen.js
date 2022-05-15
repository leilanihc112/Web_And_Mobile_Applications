import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, PermissionsAndroid } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import Geolocation from 'react-native-geolocation-service';
import GetLocation from 'react-native-get-location';

const StandMarker = (props) => {
    return(
        <Marker
            coordinate={props.coordinate}
            title={props.markerTitle}>
        </Marker>
    )

}

const ViewNearbyStandScreen = ({navigation}) => {
  const [longtiude, setLongitude] = React.useState(0);
  const [latitude, setLatitude] = React.useState(0);
  const [locationFlag, setLocationFlag] = useState(false);

    const [region, setRegion] = useState({
      latitude: 29.626787,
      longitude: -95.6865535,
      latitudeDelta: 0.01,
      longitudeDelta: 0.01,
    });

    const tokyoRegion = {
      latitude: 35.6762,
      longitude: 139.6503,
      latitudeDelta: 0.01,
      longitudeDelta: 0.01,
    };


    const _getCourts = () => {
      GetLocation.getCurrentPosition({
        enableHighAccuracy: true,
        timeout: 15000,
      })
      .then(location => {
          //console.log(location);
          setLatitude(parseFloat(location.latitude));
          setLongitude(parseFloat(location.longitude));
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
    }, []);


    return (
      <View style={styles.container}>
        <MapView
            style={styles.map}
            initialRegion={region}>       
            <StandMarker coordinate={region} markerTitle="Stand 1"/>
            <StandMarker coordinate={{latitude: latitude, longitude: longtiude}} markerTitle="Current Location"/>
            <StandMarker coordinate={tokyoRegion} markerTitle="Tokyo Region"/>
            <StandMarker coordinate={{latitude: 35.67714827145542, longitude: 139.6551462687416}} markerTitle="Stand 2"/>
        </MapView>


      </View>
    )
}

const styles = StyleSheet.create({
    // container:{
    //   flex:1, 
    //   justifyContent:'center',
    //   alignItems:'center',
    //   backgroundColor: '#212529'
    // },
    container: {
        ...StyleSheet.absoluteFillObject,
        flex: 1,
        justifyContent: 'flex-end',
        alignItems: 'center',
      },
      map: {
        ...StyleSheet.absoluteFillObject,
      },
    text:{
      fontSize: 36,
      fontWeight: "bold",
      paddingBottom: 80,
      color: "#59bfff",
    }
  });

export default ViewNearbyStandScreen;
