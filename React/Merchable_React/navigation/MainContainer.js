import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';

// Screens
import DashboardContainer from './DashboardContainer';
import LogoutScreen from './screen/LogoutScreen';
import SearchContainer from './SearchContainer';

//Screen Names
const dashboardName = 'Dashboard Container';
const searchName = 'Search Container';
const logoutName = 'Log Out';

const Tab = createBottomTabNavigator();

const MainContainer = (props) => {
    return(
        <NavigationContainer>
            <Tab.Navigator
                initialRouteName={dashboardName}
                screenOptions={({ route }) => ({
                    tabBarIcon: ({focused, color, size}) => {

                        let iconName;
                        let rn = route.name;

                        if(rn === dashboardName){
                            iconName = focused ? 'list' : 'list-outline';
                        }else if (rn === searchName){
                            iconName = focused ? 'search' : 'search-outline';
                        }else if(rn === logoutName){
                            iconName = focused ? 'log-out' : 'log-out-outline';
                        }

                        return <Ionicons name={iconName} size={size} color={color} />;
                    },
                    tabBarActiveTintColor: '#59bfff',
                    tabBarInactiveTintColor: 'gray',
                    tabBarLabelStyle: { paddingBottom: 10, fontSize: 10 },
                    tabBarStyle: { padding: 10, height: 70},
                })}

            >

                <Tab.Screen 
                    name={dashboardName} 
                    component={DashboardContainer}
                    options={{
                        headerStyle: {
                          backgroundColor: '#59bfff',
                        },
                        headerTintColor: '#fff',
                        headerShown: false,
                    }}
                    initialParams={{ email: props.user.additionalUserInfo.profile.email }}
                />
                <Tab.Screen 
                    name={searchName} 
                    component={SearchContainer}
                    options={{
                        headerStyle: {
                          backgroundColor: '#59bfff',
                        },
                        headerTintColor: '#fff',
                        headerShown: false,
                    }}
                    
                />
                <Tab.Screen 
                    name={logoutName} 
                    children={()=><LogoutScreen showProps={true} {...props}/>}
                    options={{
                        headerStyle: {
                          backgroundColor: '#59bfff',
                        },
                        headerTintColor: '#fff',
                    }}
                />
                

            </Tab.Navigator>
        </NavigationContainer>
    );
}

export default MainContainer;