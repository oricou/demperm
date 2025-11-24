import {SimpleUser} from "@/api/types/common/simple-user";
import {Message} from "@/api/types/chat/message";
import {SimpleChat} from "@/api/types/chat/simple-chat";


export class FullChat {
    chat!: SimpleChat
    messages!: Message[];
}