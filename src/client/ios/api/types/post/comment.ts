import {SimpleUser} from "@/api/types/common/simple-user";

export class Comment {
    commentId!: number;
    author!: SimpleUser;
    content!: string;
    subComments!: Comment[];
    createdAt!: Date;
    updatedAt!: Date;
}