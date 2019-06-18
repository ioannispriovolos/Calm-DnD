import firebase from 'firebase'

var config = { /* COPY THE ACTUAL CONFIG FROM FIREBASE CONSOLE */

    apiKey: "AIzaSyD418RA8eA0z6U83Y_9ZuZ9oaHLsVsPABA",
    authDomain: "calmdnd.firebaseapp.com",
    databaseURL: "https://calmdnd.firebaseio.com",
    projectId: "calmdnd",
    storageBucket: "calmdnd.appspot.com",
    messagingSenderId: "877464327985"

};
var fire = firebase.initializeApp(config);
export default fire;