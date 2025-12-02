import { ConversationPreview } from "../../types/conversation_types";

export const conversations: ConversationPreview[] = [
  {
    id: "conv1",
    with: { 
      id: "42",
      username: "Jean Dupont",
      photo: require("../../public/images/utilisateur2.png")
    },
    lastMessage: "Salut !",
    lastTime: Date.now() - 60000,
  },
  {
    id: "conv2",
    with: { 
      id: "12",
      username: "Marie Curie",
      photo: require("../../public/images/utilisateur2.png")
    },
    lastMessage: "On se voit demain ?",
    lastTime: Date.now() - 3600000,
  },
];
