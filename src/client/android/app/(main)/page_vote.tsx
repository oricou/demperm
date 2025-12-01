import React, { useState } from "react";
import { View, Text, TextInput, Image } from "react-native";
import styles from '@/styles/vote_style';
import ComponentList, { Person } from '@/components/ComponentList';

export default function VotePage() {
  const [searchText, setSearchText] = useState('');

    // { id: "1", Nom: "Dupont", Prenom: "Jean1", Photo_de_Profil: require('@/public/images/utilisateur2.png'), points: 10 },
    // { id: "2", Nom: "Dupont", Prenom: "Jean2", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
    // { id: "3", Nom: "Dupont", Prenom: "Jean3", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
    // { id: "4", Nom: "Dupont", Prenom: "Jean4", Photo_de_Profil: require('@/public/images/utilisateur2.png') },

  const data: Person[] = [
    { id: "1", Nom: "Dupont", Prenom: "Jean1", Photo: require('@/public/images/utilisateur2.png'), points: "10", unit: "voix", extra:"+13 point" },
    { id: "2", Nom: "Dupont", Prenom: "Jean2", Photo: require('@/public/images/utilisateur2.png') },
    { id: "3", Nom: "Dupont", Prenom: "Jean3", Photo: require('@/public/images/utilisateur2.png') },
    { id: "4", Nom: "Dupont", Prenom: "Jean4", Photo: require('@/public/images/utilisateur2.png') },
  ];

  // Filtrage selon la barre de recherche
  const filteredData = data.filter((item) => {
    const fullName = `${item.Prenom} ${item.Nom}`.toLowerCase();
    const search = searchText.toLowerCase();
    return fullName.includes(search);
  });

return (
  <View style={styles.container}>
    <Text style={styles.title}>Séléction pour le vote</Text>
    

<View style={styles.searchContainer}>
  <Image
    source={require('@/public/images/search.png')}
    style={styles.searchIcon}
  />
  
  <TextInput
    style={styles.searchBar}
    placeholder="Recherche"
    value={searchText}
    onChangeText={setSearchText}
  />

  <Text style={styles.text_voix}>9 Voix</Text>
</View>



      <ComponentList data={filteredData} />
    </View>
  );
}
