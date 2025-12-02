import React from "react";
import { Text, View } from "react-native";
import SamplePostPage from "./messagerie_debat/page_post";

// import ListePage from "./page_vote";

import PrivateMessagePage from "./messagerie_debat/page_private_message";
import MessagePage from "./messagerie_debat/page_chat";
import ConnectionScreen from "@/app/(auth)/connection";
import ThemePage from "./messagerie_debat/theme";

export default function Index() {
  return (
    <ConnectionScreen />
  );
}
