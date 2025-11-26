import React, { useState } from "react";
import { View, TextInput, TouchableOpacity, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";

type Props = {
  onSend: (text: string) => void;
};

const MessageInput: React.FC<Props> = ({ onSend }) => {
  const [text, setText] = useState("");

  const send = () => {
    if (text.trim().length === 0) return;
    onSend(text.trim());
    setText("");
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Écrire un message..."
        value={text}
        onChangeText={setText}
        multiline
      />

      <TouchableOpacity onPress={send} style={styles.sendButton}>
        <Ionicons name="send" size={26} color="#0078FF" />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    padding: 8,
    backgroundColor: "#fff",
    borderTopWidth: 1,
    borderColor: "#ccc",
    alignItems: "flex-end",
  },
  input: {
    flex: 1,
    maxHeight: 120,
    padding: 10,
    borderRadius: 20,
    backgroundColor: "#f2f2f2",
    fontSize: 16,
  },
  sendButton: {
    paddingHorizontal: 10,
    paddingVertical: 6,
  },
});

export default MessageInput;
