import React from "react";
import { View, Text, Image, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";

type Props = {
  name: string;
  photo?: any;
};

const ChatHeader: React.FC<Props> = ({ name, photo }) => {
  return (
    <View style={[styles.container, { backgroundColor: "#FFFFFF" }]}>
      {/* Photo + Nom */}
      <View style={styles.userInfo}>
        {photo && (
          <Image
            source={photo}
            style={styles.avatar}
          />
        )}
        <Text style={styles.name}>{name}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
  height: 85,
  flexDirection: "row",
  alignItems: "center",
  paddingHorizontal: 15,

  backgroundColor: "#FFFFFF",

  shadowColor: "#000",
  shadowOpacity: 0.12,
  shadowRadius: 6,
  shadowOffset: { width: 0, height: 3 },
  elevation: 6,

  marginHorizontal: 10,
  marginTop: 10,
  borderRadius: 12,
},


  backButton: {
    paddingRight: 15,
    paddingVertical: 6,
  },

  userInfo: {
    flexDirection: "row",
    alignItems: "center",
  },

  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "#ddd",
  },

  name: {
    fontSize: 20,
    marginLeft: 12,
    fontWeight: "600",
    color: "#000",
  },
});


export default ChatHeader;
