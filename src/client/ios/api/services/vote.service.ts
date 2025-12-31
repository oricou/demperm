import { voteApiClient } from "../client";

export interface VoteRequestDto {
    targetUserId: string;
    domain: string;
}

export interface VoteDto {
    id: string;
    voterId: string;
    targetUserId: string;
    domain: string;
    createdAt: string;
}

export interface ReceivedVotesDto {
    userId: string;
    total: number;
    byDomain: Record<string, number>;
    usersByDomain: Record<string, string>;
}

export interface VoteCountSummaryDto {
    date: string;
    count: number;
}

export interface DailyVotesEvolutionDto {
    userId: string;
    daily: VoteCountSummaryDto[];
    delta: number;
}

export interface MonthlyVotesEvolutionDto {
    userId: string;
    monthly: {
        year: number;
        month: number;
        count: number;
    }[];
}

export interface VoteResultDto {
    userId: string;
    domain: string;
    count: number;
    elected: boolean;
    electedAt?: string;
}

export interface PublicationSettingDto {
    userId: string;
    publishVotes: boolean;
}

export interface ThresholdSettingDto {
    userId: string;
    threshold: number;
}


export const voteService = {

    async createVote(data: VoteRequestDto): Promise<VoteDto> {
        try {
            const res = await voteApiClient.post<VoteDto>("/votes", data);
            return res.data;
        } catch (err: any) {
            console.error("Erreur createVote:", err.response?.data || err);
            throw err;
        }
    },

    async deleteVote(domain: string): Promise<void> {
        try {
            await voteApiClient.delete(`/votes/${domain}`);
        } catch (err: any) {
            console.error("Erreur deleteVote:", err.response?.data || err);
            throw err;
        }
    },

    async getVotesByVoter(voterId: string, domain?: string): Promise<VoteDto[]> {
        try {
            const res = await voteApiClient.get<VoteDto[]>(`/votes/by-voter/${voterId}`, {
                params: domain ? { domain } : undefined,
            });
            return res.data;
        } catch (err: any) {
            console.error("Erreur getVotesByVoter:", err.response?.data || err);
            throw err;
        }
    },

    async getVotesByVoterMe(domain?: string): Promise<VoteDto[]> {
        try {
            const res = await voteApiClient.get<VoteDto[]>("/votes/by-voter/me", {
                params: domain ? { domain } : undefined,
            });
            return res.data;
        } catch (err: any) {
            console.error("Erreur getVotesByVoterMe:", err.response?.data || err);
            throw err;
        }
    },

    async getVotesForUser(userId: string, domain?: string): Promise<ReceivedVotesDto> {
        try {
            const res = await voteApiClient.get<ReceivedVotesDto>(`/votes/for-user/${userId}`, {
                params: domain ? { domain } : undefined,
            });
            return res.data;
        } catch (err: any) {
            console.error("Erreur getVotesForUser:", err.response?.data || err);
            throw err;
        }
    },

    async getVotesForUserMe(domain?: string): Promise<ReceivedVotesDto> {
        try {
            const res = await voteApiClient.get<ReceivedVotesDto>("/votes/for-user/me", {
                params: domain ? { domain } : undefined,
            });
            return res.data;
        } catch (err: any) {
            console.error("Erreur getVotesForUserMe:", err.response?.data || err);
            throw err;
        }
    },

    /* ------------- publication prefs ------------- */

    async getPublicationSettings(userId: string): Promise<PublicationSettingDto> {
        try {
            const res = await voteApiClient.get<PublicationSettingDto>(`/publication/${userId}`);
            return res.data;
        } catch (err: any) {
            console.error("Erreur getPublicationSettings:", err.response?.data || err);
            throw err;
        }
    },

    async updatePublicationSettings(userId: string, publishVotes: boolean): Promise<PublicationSettingDto> {
        try {
            const res = await voteApiClient.put<PublicationSettingDto>(`/publication/${userId}`, {
                publishVotes,
            });
            return res.data;
        } catch (err: any) {
            console.error("Erreur updatePublicationSettings:", err.response?.data || err);
            throw err;
        }
    },

    async getThreshold(userId: string): Promise<ThresholdSettingDto> {
        try {
            const res = await voteApiClient.get<ThresholdSettingDto>(`/threshold/${userId}`);
            return res.data;
        } catch (err: any) {
            console.error("Erreur getThreshold:", err.response?.data || err);
            throw err;
        }
    },

    async updateThreshold(data: ThresholdSettingDto): Promise<ThresholdSettingDto> {
        try {
            const res = await voteApiClient.put<ThresholdSettingDto>(`/threshold/${data.userId}`, data);
            return res.data;
        } catch (err: any) {
            console.error("Erreur updateThreshold:", err.response?.data || err);
            throw err;
        }
    },

    async getResults(domain?: string, top: number = 100, since?: string): Promise<VoteResultDto[]> {
        try {
            const res = await voteApiClient.get<VoteResultDto[]>("/results", {
                params: {
                    domain,
                    top,
                    since,
                },
            });
            return res.data;
        } catch (err: any) {
            console.error("Erreur getResults:", err.response?.data || err);
            throw err;
        }
    },
};
