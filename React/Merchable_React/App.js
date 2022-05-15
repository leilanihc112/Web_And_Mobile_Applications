import * as React from 'react';
import { useState } from 'react';
import LoginScreen from './navigation/LoginScreen'
import MainContainer from './navigation/MainContainer';

global.email = "";

const App = () => {
  const [signedIn, setSignedIn] = useState(false);
  const [user, setUser] = useState(null);

  const signIn = (status) => {
    setSignedIn(status);
  }

  const sendUserToParent = (user) => {
    //console.log(user);
    setUser(user);
    global.email = user.additionalUserInfo.profile.email;
  }

  return (
    signedIn ?
    <MainContainer setSignedIn={signIn} user={user}/>
    : <LoginScreen setSignedIn={signIn} sendUserToParent={sendUserToParent} />
  );
};

export default App;
