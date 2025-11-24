import {SimpleUser} from "@/api/types/common/simple-user";
import {SimplePost} from "@/api/types/common/simple-post";

export class Profile {
    user!: SimpleUser;
    voteCount!: number;
    bio!: string;
    posts!: SimplePost[]
}