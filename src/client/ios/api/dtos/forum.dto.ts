import {UserDto} from "@/api/dtos/user.dto";
import {PostDto} from "@/api/dtos/post.dto";
import {DomainDto} from "@/api/dtos/domain.dto";

export class ForumDto {
    forum_id!: string;
    name!: string;
    description!: string;
    creator_id!: UserDto;
    member_count!: number;
    post_count!: number;
    created_at!: Date;
}

export interface CreateForumDto {
  name: string;
  description: string;
}

export interface SubforumsDto {
    subforums_id: string;
    name: string;
    description: string;
    parent_domain_id: string;
    parent_forum_id: string;
    created_at: Date;
}