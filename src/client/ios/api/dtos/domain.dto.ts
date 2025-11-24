import {ForumDto} from "@/api/dtos/forum.dto";

export class DomainDto {
    domainId!: number;
    domainName!: string;
    forums!: ForumDto[];
}