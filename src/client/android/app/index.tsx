import React from "react";
import { Text, View } from "react-native";
import SamplePostPage from "./messagerie_debat/page_post";
import ConnectionScreen from "@/app/(auth)/connection";


export default function Index() {
  return (
    /*<View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>Edit app/index.tsx to edit this screen.</Text>
    </View>*/
    

    // <ListePage />
    <ConnectionScreen />
  );
}