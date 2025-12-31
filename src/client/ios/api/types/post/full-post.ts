import { SimplePost } from "@/api/types/common/simple-post";
import { Comment } from "@/api/types/post/comment";
import {CommentServerDto} from "@/api/services/post.service";

export class FullPost {
    post!: SimplePost;
    comments!: CommentServerDto[];
}