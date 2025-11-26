import React from "react";
import { View, FlatList, StyleSheet } from "react-native";
import { TouchableOpacity, Text, Image } from "react-native";
import { useRouter } from "expo-router";
import { ConversationPreview } from "@/types/conversation_types";
import { conversations } from "@/public/message/exemple_preview_message" //<< ?


export default function ChatPage() {
  const router = useRouter();

  const renderItem = (item: ConversationPreview) => {
    const time = new Date(item.lastTime).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    return (
      <TouchableOpacity
        style={styles.itemContainer}
        onPress={() => {
          router.push({
            pathname: "/page_private_message",
            params: {
              withId: item.with.id,
              username: item.with.username,
              photo: item.with.photo, // attention : require() ne passe pas dans params directement
            },
          });
        }}
      >
        <Image source={item.with.photo} style={styles.avatar} />
        <View style={{ flex: 1, marginLeft: 12 }}>
          <Text style={styles.name}>{item.with.username}</Text>
          <Text numberOfLines={1} style={styles.lastMessage}>{item.lastMessage}</Text>
        </View>
        <View style={{ alignItems: "flex-end" }}>
          <Text style={styles.time}>{time}</Text>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={conversations}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => renderItem(item)}
        contentContainerStyle={{ paddingVertical: 10 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F5F5F5" },
  itemContainer: { flexDirection: "row", padding: 12, backgroundColor: "#FFF", marginBottom: 10, borderRadius: 12, marginHorizontal: 10, alignItems: "center", shadowColor: "#000", shadowOpacity: 0.07, shadowRadius: 4, shadowOffset: { width: 0, height: 2 }, elevation: 3 },
  avatar: { width: 54, height: 54, borderRadius: 27 },
  name: { fontSize: 18, fontWeight: "600", marginBottom: 3 },
  lastMessage: { fontSize: 14, color: "gray" },
  time: { fontSize: 12, color: "gray", marginBottom: 6 },
  unreadBadge: { backgroundColor: "#0078FF", paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 },
  unreadText: { color: "#FFF", fontWeight: "bold", fontSize: 12 },
});
