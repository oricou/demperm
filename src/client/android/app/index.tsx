import React from "react";
import { Text, View } from "react-native";
import SamplePostPage from "./messagerie_debat/page_post";

// import ListePage from "./page_vote";

import ListePage from "./page_vote";
import PrivateMessagePage from "./messagerie_debat/page_private_message";
import MessagePage from "./messagerie_debat/page_chat";


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
    <SamplePostPage />
  );
}