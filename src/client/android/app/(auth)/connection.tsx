import React, { useState } from 'react';
import { View, Text, Image, TextInput, TouchableOpacity, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import styles from '@/styles/vote_style';
import { useUser } from '@/contexts/user-context';


export default function ConnectionScreen() {
  const { login, register } = useUser()!;
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);

  const handleAction = async () => {
    if (isRegistering) {
      const e = await register(email, password);
      if (e) {
        alert("Erreur lors de l'inscription: " + e);
      } else {
        alert("Inscription réussie !");
      }
    } else {
      const e = await login(email, password);
      if (e) {
        alert("Erreur lors de la connexion: " + e);
      }
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={{ flex: 1 }}
    >
      <ScrollView
        contentContainerStyle={{ flexGrow: 1, alignItems: 'center', justifyContent: 'center', padding: 20 }}
        keyboardShouldPersistTaps="handled"
      >

        <Image
          source={require('@/public/images/logo.png')}
        />
        <Text style={{ fontSize: 50, color: '#000091', marginBottom: 30 }}>DemPerm</Text>

        <TextInput
          style={[styles.searchBar, { marginBottom: 20, padding: 10, borderRadius: 10, borderWidth: 1, borderColor: '#ccc', backgroundColor: '#fff', width: '100%' }]}
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
        />
        <TextInput
          style={[styles.searchBar, { marginBottom: 30, padding: 10, borderRadius: 10, borderWidth: 1, borderColor: '#ccc', backgroundColor: '#fff', width: '100%' }]}
          placeholder="Mot de Passe"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <TouchableOpacity
          style={{
            backgroundColor: '#000091',
            paddingVertical: 15,
            paddingHorizontal: 50,
            borderRadius: 10,
            width: '100%',
            alignItems: 'center',
            marginBottom: 20
          }}
          onPress={handleAction}
        >
          <Text style={{ color: '#fff', fontSize: 18, fontWeight: 'bold' }}>
            {isRegistering ? "S'inscrire" : "Connexion"}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => setIsRegistering(!isRegistering)}>
          <Text style={{ color: '#000091', fontSize: 16 }}>
            {isRegistering ? "Déjà un compte ? Connectez-vous" : "Pas de compte ? Inscrivez-vous"}
          </Text>
        </TouchableOpacity>

      </ScrollView>
    </KeyboardAvoidingView>
  );
}
