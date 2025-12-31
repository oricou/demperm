import { SimpleUser } from "@/api/types/common/simple-user";
import {SimpleForum} from "@/api/types/forum/simple-forum";

export class Media {
    mediaType!: string;
    mediaUrl!: string;
}

export class SimplePost {
    id!: string;
    forum!: SimpleForum | null;
    author!: SimpleUser;
    title!: string;
    content!: string;
    medias!: Media[];
    likeCount!: number;
    commentCount!: number;
    createdAt!: Date;
    updatedAt!: Date;
    liked?: boolean;
}