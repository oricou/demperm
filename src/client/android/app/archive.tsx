import React, { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import ComponentList, { Person } from '@/components/ComponentList';
export default function ArchiveScreen() {
const [activeTab, setActiveTab] = useState('MesVotes');

const data1: Person[] = [
{ id: "1", Nom: "Dupont", Prenom: "Jean1", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
{ id: "2", Nom: "Dupont", Prenom: "Jean2", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
{ id: "3", Nom: "Dupont", Prenom: "Jean3", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
{ id: "4", Nom: "Dupont", Prenom: "Jean4", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
];

const data2: Person[] = [
{ id: "1", Nom: "Dupont", Prenom: "Paul1", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
{ id: "2", Nom: "Dupont", Prenom: "Paul2", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
{ id: "3", Nom: "Dupont", Prenom: "Paul3", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
{ id: "4", Nom: "Dupont", Prenom: "Paul4", Photo_de_Profil: require('@/public/images/utilisateur2.png') },
];

return (
<View style={{ flex: 1, backgroundColor: '#fff' }}>
{/* Barre de navigation */}
<View style={{ flexDirection: 'row', justifyContent: 'space-around', paddingVertical: 15, borderBottomWidth: 2, borderBottomColor: '#ccc' }}>
<TouchableOpacity onPress={() => setActiveTab('MesVotes')}>

<Text style={{
fontSize: 16,
fontWeight: 'bold',
color: activeTab === 'MesVotes' ? '#000091' : '#bbb',
borderBottomWidth: activeTab === 'MesVotes' ? 2 : 0,
borderBottomColor: '#000091',
paddingBottom: 5
}}>
Mes Votes </Text> </TouchableOpacity>

    <TouchableOpacity onPress={() => setActiveTab('LesElus')}>
      <Text style={{
        fontSize: 16,
        fontWeight: 'bold',
        color: activeTab === 'LesElus' ? '#000091' : '#bbb',
        borderBottomWidth: activeTab === 'LesElus' ? 2 : 0,
        borderBottomColor: '#000091',
        paddingBottom: 5
      }}>
        Les Élus
      </Text>
    </TouchableOpacity>
  </View>

  {/* Contenu selon l'onglet */}
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    {activeTab === 'MesVotes' ? (
        // zone 1
    <>

      <ComponentList data={data1} />
      
    </>
    ) : (
        // zone 2
    <>
        
      <ComponentList data={data2} />

    </>
    )}
  </View>
</View>

);
}
