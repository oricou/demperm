import React from "react";
import { View, TextInput, Image, TouchableOpacity } from "react-native";
import styles from "@/styles/searchbar_style";

type Props = {
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
};

const SearchBarComponent: React.FC<Props> = ({
  value,
  onChangeText,
  placeholder = "Rechercher",
}) => {
  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder={placeholder}
        placeholderTextColor="#8fa2c9"
        value={value}
        onChangeText={onChangeText}
      />

      <TouchableOpacity>
        <Image
          source={require("@/public/images/search.png")}
          style={styles.icon}
        />
      </TouchableOpacity>
    </View>
  );
};

export default SearchBarComponent;
