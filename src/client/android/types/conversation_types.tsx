import { UserModel } from "./user_model";

export type ConversationPreview = {
  id: string;
  with: UserModel;
  lastMessage: string;
  lastTime: number;
};
