import {SimpleForum} from "@/api/types/forum/simple-forum";
import {SimplePost} from "@/api/types/common/simple-post";

export class FullForum {
    forum!: SimpleForum;
    posts!: SimplePost[]; 
}