import {UserDto} from "@/api/dtos/user.dto";
import {PostDto} from "@/api/dtos/post.dto";
import {DomainDto} from "@/api/dtos/domain.dto";

export class ForumDto {
    forumId!: number;
    creator!: UserDto;
    forumName!: string;
    description!: string;
    forumImageUrl!: string;
    domains!: DomainDto[];
    posts!: PostDto[];
    memberCount!: number;
    postCount!: number;
    createdAt!: Date;
    updatedAt!: Date;
}