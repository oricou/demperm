import {Profile} from "@/api/types/profile/profile";
import {SimplePost} from "@/api/types/common/simple-post";

export class ForYouResults {
    users!: Profile[];
    posts!: SimplePost[];
}