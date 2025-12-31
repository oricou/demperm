import React, { useRef, useEffect } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import { Message } from "@/types/messages";

type Props = {
  messages: Message[];
  selfId: string;
};

const ConversationView: React.FC<Props> = ({ messages, selfId }) => {
  const flatListRef = useRef<FlatList>(null);

  // Scroll automatique vers le bas quand un message arrive
  useEffect(() => {
    if (flatListRef.current) {
      flatListRef.current.scrollToEnd({ animated: true });
    }
  }, [messages]);

  const renderItem = ({ item }: { item: Message }) => {
    const isMe = item.from === selfId;

    return (
      <View
        style={[
          styles.messageContainer,
          isMe ? styles.messageRight : styles.messageLeft,
        ]}
      >
        <View style={[styles.bubble, isMe ? styles.bubbleMe : styles.bubbleOther]}>
          <Text style={styles.text}>{item.text}</Text>
          <Text style={styles.time}>
            {new Date(item.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
          </Text>
        </View>
      </View>
    );
  };

  return (
    <FlatList
      ref={flatListRef}
      data={messages}
      renderItem={renderItem}
      keyExtractor={(item) => item.id}
      contentContainerStyle={{ paddingVertical: 10 }}
    />
  );
};

const styles = StyleSheet.create({
  messageContainer: {
    flexDirection: "row",
    marginVertical: 4,
    paddingHorizontal: 10,
  },
  messageLeft: {
    justifyContent: "flex-start",
  },
  messageRight: {
    justifyContent: "flex-end",
  },
  bubble: {
    maxWidth: "75%",
    padding: 10,
    borderRadius: 18,
  },
  bubbleMe: {
    backgroundColor: "#0078FF",
    borderBottomRightRadius: 0,
  },
  bubbleOther: {
    backgroundColor: "#E5E5EA",
    borderBottomLeftRadius: 0,
  },
  text: {
    color: "#000",
    fontSize: 16,
  },
  time: {
    color: "#555",
    fontSize: 10,
    marginTop: 4,
    alignSelf: "flex-end",
  },
});

export default ConversationView;
