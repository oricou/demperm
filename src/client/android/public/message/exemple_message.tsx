import { PrivateConversation } from "../../types/messages";

export const conversationsFull: PrivateConversation[] = [
  {
    with: {
      id: "42",
      username: "Jean Dupont",
      photo: require("../../public/images/utilisateur2.png"),
    },
    messages: [
      {
        id: "m1",
        text: "Salut !",
        timestamp: Date.now() - 60000,
        from: "42",
      },
      {
        id: "m2",
        text: "Comment ça va ?",
        timestamp: Date.now() - 55000,
        from: "42",
      },
      {
        id: "m3",
        text: "Bien et toi ?",
        timestamp: Date.now() - 50000,
        from: "me",
      },
    ],
  },

  {
    with: {
      id: "12",
      username: "Marie Curie",
      photo: require("../../public/images/utilisateur2.png"),
    },
    messages: [
      {
        id: "m1",
        text: "On se voit demain ?",
        timestamp: Date.now() - 3600000,
        from: "12",
      },
      {
        id: "m2",
        text: "Oui, vers 14h ça va ?",
        timestamp: Date.now() - 3500000,
        from: "me",
      },
    ],
  },
];

// Fonction utilitaire
export function getConversationById(userId: string) {
  return conversationsFull.find(conv => conv.with.id === userId) || null;
}
