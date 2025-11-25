import { SimpleUser } from "@/api/types/common/simple-user";
import {SimpleForum} from "@/api/types/forum/simple-forum";

export class Media {
    mediaType!: string;
    mediaUrl!: string;
}

export class SimplePost {
    id!: number;
    forum!: SimpleForum | null;
    author!: SimpleUser;
    content!: string;
    medias!: Media[];
    likeCount!: number;
    commentCount!: number;
    createdAt!: Date;
    updatedAt!: Date;
}