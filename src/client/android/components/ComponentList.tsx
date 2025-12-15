import React from "react";
import { View, Text, FlatList, Image } from "react-native";
import styles from '@/styles/vote_style';

export type Person = {
  id: string;
  Nom: string;
  Prenom: string;
  Photo: any;
  points?: string;
  unit?: string;
  extra?: string;
};

type ListePersonnesProps = {
  data: Person[];
};

const ComponentList: React.FC<ListePersonnesProps> = ({ data }) => {
  const renderItem = ({ item }: { item: Person }) => (
    <View style={[styles.item, { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }]}>
      <View style={{ flexDirection: 'row', alignItems: 'center' }}>
        <Image source={item.Photo} style={styles.avatar} />
        <View style={{ marginLeft: 10 }}>
          {/* Nom et Prénom */}
          <Text style={styles.text}>{item.Prenom + " " + item.Nom}</Text>
          {/* ID */}
          <Text style={[styles.text, { color: 'gray', fontSize: 12 }]}># {item.id}</Text>
        </View>
      </View>
      {item.points !== undefined && item.points !== null && (
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          {/* Points */}
          <Text style={[styles.text, { fontSize: 20, fontWeight: 'bold' }]}>{item.points}</Text>
          <View style={{ marginLeft: 10 }}>
            {/* Extra */}
            {item.extra && <Text style={{ color: 'gray', fontSize: 12, marginLeft: 4 }}>{item.extra}</Text>}
            {/* Unit */}
            {item.unit && <Text style={{ fontSize: 15, marginLeft: 4 }}>{item.unit}</Text>}
          </View>
        </View>
      )}
    </View>
  );

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={(item) => item.id}
    />
  );
};

export default ComponentList;
