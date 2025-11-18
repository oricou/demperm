import {UserDto} from "@/api/dtos/user.dto";

export class CommentDto {
    commentId!: number;
    author!: UserDto;
    comments!: CommentDto[];
    content!: string;
    createdAt!: Date;
    updatedAt!: Date;
}