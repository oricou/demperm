import { SimplePost } from "@/api/types/common/simple-post";
import { Comment } from "@/api/types/post/comment";

export class FullPost {
    post!: SimplePost;
    comments!: Comment[];
}