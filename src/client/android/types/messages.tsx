import { UserModel } from "./user_model";

export type Message = {
  id: string;
  text: string;
  timestamp: number;
  from: string; // id du user
};

export type PrivateConversation = {
  with: UserModel;
  messages: Message[];
};
