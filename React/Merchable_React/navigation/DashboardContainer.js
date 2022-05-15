import * as React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

//Screens
import DashboardScreen from './screen/DashboardScreen';
import CreateStandScreen from './screen/CreateStandScreen';
import ViewNearbyStandScreen from './screen/ViewNearbyStandScreen';
import StandContainer from './StandContainer';
import ManagementContainer from './ManagementContainer';

const Stack = createStackNavigator();

const DashboardContainer = ({props, navigation}) => {
    return (
        <Stack.Navigator initialRouteName="Dashboard">
            <Stack.Screen 
              name="Dashboard" 
              component={DashboardScreen} 
              options={{
                headerStyle: {
                  backgroundColor: '#59bfff',
                },
                headerTintColor: '#fff',
              }}
            />
            <Stack.Screen 
              name="Management Container" 
              component={ManagementContainer} 
              options={{
                  headerStyle: {
                    backgroundColor: '#59bfff',
                  },
                  headerTintColor: '#fff',
                  headerShown: false,
              }}
            />
            <Stack.Screen 
              name="Create Stand" 
              component={CreateStandScreen} 
              options={{
                  headerStyle: {
                    backgroundColor: '#59bfff',
                  },
                  headerTintColor: '#fff',
              }}
            />
            <Stack.Screen 
              name="Stand Container" 
              component={StandContainer} 
              options={{
                  headerStyle: {
                    backgroundColor: '#59bfff',
                  },
                  headerTintColor: '#fff',
                  headerShown: false,
              }}
            />
            <Stack.Screen 
              name="View Nearby Stands" 
              component={ViewNearbyStandScreen} 
              options={{
                  headerStyle: {
                    backgroundColor: '#59bfff',
                  },
                  headerTintColor: '#fff',
              }}
            />
        </Stack.Navigator>
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
    }
  });

export default DashboardContainer;