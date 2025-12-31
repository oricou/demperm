import {Domain} from "@/api/types/forum/domain";

export class SimpleForum {
    id!: string;
    title!: string;
    description!: string;
    domains!: Domain[];
    memberCount!: number;
}