import React, { useState } from 'react';
import { View, Text, Image, TextInput, TouchableOpacity } from 'react-native';
import styles from '@/styles/vote_style';
import { useRouter } from "expo-router";
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { signInWithEmailAndPassword } from "firebase/auth";

const router = useRouter();


const firebaseConfig = {
  apiKey: "AIzaSyDvFfs-_AqsIn2UHvGUpoJUvhomsKLRu7E",
  authDomain: "demperm-153aa.firebaseapp.com",
  projectId: "demperm-153aa",
  storageBucket: "demperm-153aa.firebasestorage.app",
  messagingSenderId: "944084627432",
  appId: "1:944084627432:web:964231aa650147c724be5d"
};


const app = initializeApp(firebaseConfig);

export const auth = getAuth(app)

export default function ConnectionScreen() {
  const [Identifiant, setIdentifiant] = useState('');
  const [Pasword, setPasword] = useState('');

const handleLogin = async () => {
    if (!Identifiant || !Pasword) {;
      return;
    }
    
    try {
      const userCredential = await signInWithEmailAndPassword(auth, Identifiant, Pasword);
        const user = userCredential.user;
        const userId = await user.getIdToken();
        router.push({ pathname: '/profile', params: { userId: userId } })
    } catch (error: any) {
    }

  };
  return (
<View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', padding: 20}}>

  <Image
    source={require('@/public/images/logo.png')}
  />
  <Text style={{ fontSize: 50, color: '#000091', marginBottom: 30 }}>DemPerm</Text>

  <TextInput
    style={[styles.searchBar, { marginBottom: 20, padding: 10, borderRadius: 10, borderWidth: 1, borderColor: '#ccc', backgroundColor: '#fff', width: '100%' }]}
    placeholder="Email"
    value={Identifiant}
    onChangeText={setIdentifiant}
  />
  <TextInput
    style={[styles.searchBar, { marginBottom: 30, padding: 10, borderRadius: 10, borderWidth: 1, borderColor: '#ccc', backgroundColor: '#fff', width: '100%' }]}
    placeholder="Mot de Passe"
    value={Pasword}
    onChangeText={setPasword}
    secureTextEntry
  />

  <TouchableOpacity
    style={{
      backgroundColor: '#000091',
      paddingVertical: 15,
      paddingHorizontal: 50,
      borderRadius: 10,
      width: '100%',
      alignItems: 'center'
    }}
    onPress={handleLogin}
  >
    <Text style={{ color: '#fff', fontSize: 18, fontWeight: 'bold' }}>Connexion</Text>
  </TouchableOpacity>

</View>
  );
}
