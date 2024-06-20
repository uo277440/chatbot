
import { getFirestore } from "firebase/firestore";


// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCfTSshGpJZfqkFW4ghce3HVAYX75UzMNA",
  authDomain: "chatbot-tfg-4a55a.firebaseapp.com",
  databaseURL: "https://chatbot-tfg-4a55a-default-rtdb.firebaseio.com",
  projectId: "chatbot-tfg-4a55a",
  storageBucket: "chatbot-tfg-4a55a.appspot.com",
  messagingSenderId: "743740112356",
  appId: "1:743740112356:web:4e6bf7a05e33d78e8f5bf1",
  measurementId: "G-BXEVQVV3NG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);

export { db };

