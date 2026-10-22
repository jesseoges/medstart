// MedStart Firebase web configuration. Client-side config is public; secure data with Firestore rules.
const firebaseConfig = {
  apiKey: "AIzaSyAyAIbc-OynEKpvVY01b5ngG5SKzcGqFz4Yc",
  authDomain: "medstart-aa55c.firebaseapp.com",
  projectId: "medstart-aa55c",
  storageBucket: "medstart-aa55c.firebasestorage.app",
  messagingSenderId: "265393052344",
  appId: "1:265393052344:web:b07a860a0427fcbaf9b24d",
  measurementId: "G-QN47YLNCHJ"
};
if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
window.medstartAuth = firebase.auth();
window.medstartDb = firebase.firestore();
