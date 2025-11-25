import { initializeApp } from "firebase/app";
import {
  initializeAuth,
} from "firebase/auth";
import * as firebaseAuth from 'firebase/auth';
import AsyncStorage from "@react-native-async-storage/async-storage";

const firebaseConfig = {

    apiKey: "AIzaSyDvFfs-_AqsIn2UHvGUpoJUvhomsKLRu7E",

    authDomain: "demperm-153aa.firebaseapp.com",

    projectId: "demperm-153aa",

    storageBucket: "demperm-153aa.firebasestorage.app",

    messagingSenderId: "944084627432",

    appId: "1:944084627432:web:964231aa650147c724be5d"

};

const reactNativePersistence = (firebaseAuth as any).getReactNativePersistence;


const app = initializeApp(firebaseConfig);
export const auth = initializeAuth(app, {
  persistence: reactNativePersistence ? reactNativePersistence(AsyncStorage) : undefined,
});