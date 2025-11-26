import React, { useState } from 'react';
import { View, Text, Image, TextInput, TouchableOpacity } from 'react-native';
import styles from '@/styles/vote_style';


export default function ConnectionScreen() {
  const [Identifiant, setIdentifiant] = useState('');
  const [Pasword, setPasword] = useState('');

  const handleLogin = () => {
    // connection
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
