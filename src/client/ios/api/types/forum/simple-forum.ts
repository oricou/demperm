import {Domain} from "@/api/types/forum/domain";

export class SimpleForum {
    id!: number;
    title!: string;
    description!: string;
    domains!: Domain[];
    memberCount!: number;
}