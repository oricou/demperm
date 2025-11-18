import {SimpleUser} from "@/api/types/common/simple-user";

export class Message {
    author!: SimpleUser;
    content!: string;
}