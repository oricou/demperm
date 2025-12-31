import { socialApiClient } from "../client";
import { SimpleForum } from "../types/forum/simple-forum";
import { Domain } from "../types/forum/domain";
import { CreateForumDto } from "../dtos/forum.dto";
// DTOs for domains
export interface DomainDto {
  domain_id: string;
  name: string;
  description: string;
  created_at: string;
}

export interface SubforumsDto {
  subforum_id: string;
  name: string;
  description: string;
  parent_domain_id: string;
  parent_forum_id: string;
  created_at: string;
}

// export interface CreateForumDto {
//   name: string;
//   description: string;
//   parent_subforum_id?: string;
// }

function DomainDtoToDomain(domainDto: DomainDto): Domain {
  return {
    id: domainDto.domain_id,
    name: domainDto.name,
  };
}

function DomainDtosToDomains(domainDtos: DomainDto[]): Domain[] {
  return domainDtos.map((domainDto) => DomainDtoToDomain(domainDto));
}

function SubforumsDtoToSimpleForum(subforumDto: SubforumsDto): SimpleForum {
  const simpleForum = new SimpleForum();
  simpleForum.id = subforumDto.subforum_id;
  simpleForum.title = subforumDto.name;
  simpleForum.description = subforumDto.description;
  simpleForum.domains = [];
  simpleForum.memberCount = 0;
  return simpleForum;
}

function SubforumsDtosToSimpleForums(
  subforumDtos: SubforumsDto[]
): SimpleForum[] {
  return subforumDtos.map((subforumDto) =>
    SubforumsDtoToSimpleForum(subforumDto)
  );
}

/**
 * Service pour interagir avec l'API Domains
 */
export const domainsService = {
  /**
   * Récupère la liste de tous les domaines
   * GET /api/v1/domains/
   */
  async getDomains(): Promise<Domain[]> {
    try {
      const response = await socialApiClient.get<DomainDto[]>(
        "/api/v1/domains/"
      );
      return DomainDtosToDomains(response.data);
    } catch (error: any) {
      console.error(
        "Erreur lors de la récupération des domaines:",
        error.response?.data || error.message
      );
      throw error;
    }
  },

  /**
   * Récupère les détails d'un domaine par son ID
   * GET /api/v1/domains/{domain_id}/
   */
  async getDomainById(domainId: string): Promise<Domain> {
    try {
      const response = await socialApiClient.get<DomainDto>(
        `/api/v1/domains/${domainId}/`
      );
      return DomainDtoToDomain(response.data);
    } catch (error: any) {
      console.error(
        "Erreur lors de la récupération du domaine:",
        error.response?.data || error.message
      );
      throw error;
    }
  },

  /**
   * Récupère les sous-forums d'un domaine
   * GET /api/v1/domains/{domain_id}/subforums/
   */
  async getSubforums(domainId: string): Promise<SimpleForum[]> {
    try {
      const response = await socialApiClient.get<SubforumsDto[]>(
        `/api/v1/domains/${domainId}/subforums/`
      );
      return SubforumsDtosToSimpleForums(response.data);
    } catch (error: any) {
      console.error(
        "Erreur lors de la récupération des sous-forums:",
        error.response?.data || error.message
      );
      throw error;
    }
  },

  /**
   * Crée un sous-forum dans un domaine
   * POST /api/v1/domains/{domain_id}/subforums/create/
   */
  async createSubforum(
    domainId: string,
    forumData: CreateForumDto
  ): Promise<SimpleForum> {
    try {
      const response = await socialApiClient.post<SubforumsDto>(
        `/api/v1/domains/${domainId}/subforums/create/`,
        forumData
      );
      return SubforumsDtoToSimpleForum(response.data);
    } catch (error: any) {
      console.error(
        "Erreur lors de la création du sous-forum:",
        error.response?.data || error.message
      );
      throw error;
    }
  },
};
