import {Media} from "@/api/types/common/simple-post";

export class CreatePost {
    title!: string;
    content!: string;
    medias!: Media;
}