import {UserProfileDto} from "@/api/dtos/user-profile.dto";
import {ForumDto} from "@/api/dtos/forum.dto";
import {PostMediaDto} from "@/api/dtos/post-media.dto";
import {CommentDto} from "@/api/dtos/comment-dto";

export class PostDto {
    postId!: number;
    author!: UserProfileDto;
    forum!: ForumDto;
    content!: string;
    medias!: PostMediaDto[];
    comments!: CommentDto[];
    createdAt!: Date;
    updatedAt!: Date;
}