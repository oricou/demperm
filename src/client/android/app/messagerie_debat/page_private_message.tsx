import React, { useState, useEffect } from "react";
import { View, StyleSheet, KeyboardAvoidingView } from "react-native";
import { useLocalSearchParams } from "expo-router";
import ConversationView from "@/components/ConversationView";
import MessageInput from "@/components/MessageInput";
import ChatHeader from "@/components/ChatHeader";
import { Message, PrivateConversation } from "@/types/messages";
import { conversationsFull, getConversationById } from "@/public/message/exemple_message" // <<


export default function PrivateMessagePage() {
  const params = useLocalSearchParams();

  const [conversation, setConversation] = useState<PrivateConversation | null>(null);

  useEffect(() => {
    const conv = getConversationById(params.withId);
    if (conv) {
      setConversation(conv);
    } else {
      setConversation({
        with: {
          id: params.withId,
          username: params.username,
          photo: require("@/public/images/utilisateur2.png"),
        },
        messages: [],
      });
    }
  }, [params.withId, params.username]);


  const handleSend = (text: string) => {
    if (!conversation) return;
    
    const newMessage: Message = {
      id: Math.random().toString(),
      text,
      timestamp: Date.now(),
      from: "me",
    };

    setConversation({
      ...conversation,
      messages: [...conversation.messages, newMessage],
    });
  };

  if (!conversation) return null;

  return (
    <KeyboardAvoidingView 
      style={styles.container} 
      behavior={"height"}
      keyboardVerticalOffset={80}
    >
      <ChatHeader 
        name={conversation.with.username}
        photo={conversation.with.photo}
      />

      <ConversationView
        messages={conversation.messages}
        selfId="me"
      />

      <MessageInput onSend={handleSend} />
    </KeyboardAvoidingView>
  );

}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#FFF" }
});
