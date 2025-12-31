import { Domain } from "@/api/types/forum/domain";
import { SimpleForum } from "@/api/types/forum/simple-forum";
import { Media, SimplePost } from "@/api/types/common/simple-post";
import { SimpleUser } from "@/api/types/common/simple-user";
import { Comment } from "@/api/types/post/comment";
import { FullPost } from "@/api/types/post/full-post";
import { FullForum } from "@/api/types/forum/full-forum";
import { SimpleChat } from "@/api/types/chat/simple-chat";
import { Message } from "@/api/types/chat/message";
import { FullChat } from "@/api/types/chat/full-chat";
import { Profile } from "@/api/types/profile/profile";
import { Settings, DemocracySettings, SocialSettings } from "@/api/types/profile/settings";
import { MyVotes } from "@/api/types/profile/my-votes";
import { ForYouResults } from "@/api/types/for-you-page/for-you-results";
import { CreatePost } from "@/api/types/post/create-post";
import {CommentServerDto} from "@/api/services/post.service";

// ==== Domains ====
export const domains: Domain[] = [
    { id: 1, name: "Écologie" },
    { id: 2, name: "Culture" },
    { id: 3, name: "Transport" },
];

// ==== Users ====
export const users: SimpleUser[] = [
    { id: 1, displayName: "Omri Zakaria Dakka", profilePictureUrl: "https://picsum.photos/seed/omri/96", bannerUrl: "https://picsum.photos/seed/omri/480", voteCount: 19 },
    { id: 2, displayName: "Basile Sens", profilePictureUrl: "https://picsum.photos/seed/ines/96", bannerUrl: "https://picsum.photos/seed/ines/480", voteCount: 9999 },
    { id: 3, displayName: "Alex Blanco", profilePictureUrl: "https://picsum.photos/seed/alex/96", bannerUrl: "https://picsum.photos/seed/alex/480", voteCount: 34 },
    { id: 4, displayName: "Pierre Maunier", profilePictureUrl: "https://picsum.photos/seed/pierre/96", bannerUrl: "https://picsum.photos/seed/pierre/480", voteCount: 0 },
    { id: 5, displayName: "Titouan Gragnic", profilePictureUrl: "https://picsum.photos/seed/titouan/96", bannerUrl: "https://picsum.photos/seed/titouan/480", voteCount: 123},
    { id: 6, displayName: "Inès Metiba", profilePictureUrl: "https://picsum.photos/seed/basile/96", bannerUrl: "https://picsum.photos/seed/basile/480", voteCount: 1386 },
];

const U = (id: number) => users.find(u => u.id === id)!;
const D = (id: number) => domains.find(d => d.id === id)!;

// ==== Forums ====
export const forums: SimpleForum[] = [
    // ÉCOLOGIE
    {
        id: 101,
        title: "Transition énergétique",
        description: "Mix électrique, rénovation, sobriété…",
        domains: [D(1)],
        memberCount: 1243,
    },
    {
        id: 102,
        title: "Biodiversité & Agriculture",
        description: "Protection des espèces, agroécologie, PAC.",
        domains: [D(1)],
        memberCount: 875,
    },

    // CULTURE
    {
        id: 201,
        title: "Culture & Patrimoine",
        description: "Musées, patrimoine, festivals, politiques culturelles.",
        domains: [D(2)],
        memberCount: 942,
    },
    {
        id: 202,
        title: "Médias & Liberté d'expression",
        description: "Pluralisme, financement, indépendance.",
        domains: [D(2)],
        memberCount: 1103,
    },

    // TRANSPORT
    {
        id: 301,
        title: "Mobilités douces",
        description: "Vélo, marche, aménagements urbains.",
        domains: [D(3)],
        memberCount: 1567,
    },
    {
        id: 302,
        title: "Infrastructures & Rail",
        description: "Réseau ferroviaire, RER métropolitains, fret.",
        domains: [D(3)],
        memberCount: 1320,
    },
];

const F = (id: number) => forums.find(f => f.id === id)!;

// ==== Medias helpers ====
const m = (type: string, url: string): Media => ({ mediaType: type, mediaUrl: url });

// ==== Posts (plusieurs par forum) ====
export const posts: SimplePost[] = [
    // Forum 101 - Écologie / Transition énergétique
    {
        id: 1001,
        forum: F(101),
        author: U(1),
        content: "Faut-il accélérer le déploiement du solaire sur toitures publiques d’ici 2030 ?",
        medias: [m("image", "https://picsum.photos/seed/solaire/640/360")],
        likeCount: 87,
        commentCount: 3,
        createdAt: new Date("2025-10-31T09:10:00Z"),
        updatedAt: new Date("2025-11-01T08:00:00Z"),
    },
    {
        id: 1002,
        forum: F(101),
        author: U(5),
        content: "Rénovation thermique : prime ciblée ou dispositif universel ?",
        medias: [],
        likeCount: 34,
        commentCount: 2,
        createdAt: new Date("2025-11-02T11:05:00Z"),
        updatedAt: new Date("2025-11-02T11:05:00Z"),
    },

    // Forum 102 - Écologie / Biodiversité
    {
        id: 1101,
        forum: F(102),
        author: U(4),
        content: "ZAN & corridors écologiques : comment concilier urbanisme et biodiversité ?",
        medias: [m("image", "https://picsum.photos/seed/biodiv/640/360")],
        likeCount: 56,
        commentCount: 4,
        createdAt: new Date("2025-10-28T16:40:00Z"),
        updatedAt: new Date("2025-10-28T16:40:00Z"),
    },

    // Forum 201 - Culture & Patrimoine
    {
        id: 2001,
        forum: F(201),
        author: U(6),
        content: "Doit-on sanctuariser 1% du budget des collectivités pour le patrimoine ?",
        medias: [],
        likeCount: 41,
        commentCount: 3,
        createdAt: new Date("2025-11-03T08:00:00Z"),
        updatedAt: new Date("2025-11-03T08:00:00Z"),
    },
    {
        id: 2002,
        forum: F(201),
        author: U(2),
        content: "Tarification sociale des festivals : quelles conditions d’éligibilité ?",
        medias: [m("image", "https://picsum.photos/seed/festival/640/360")],
        likeCount: 22,
        commentCount: 2,
        createdAt: new Date("2025-11-04T15:22:00Z"),
        updatedAt: new Date("2025-11-04T15:22:00Z"),
    },

    // Forum 202 - Médias
    {
        id: 2101,
        forum: F(202),
        author: U(3),
        content: "Fonds de soutien à l’investigation indépendante : comment l’organiser sans ingérence ?",
        medias: [],
        likeCount: 65,
        commentCount: 3,
        createdAt: new Date("2025-10-26T19:00:00Z"),
        updatedAt: new Date("2025-11-01T10:00:00Z"),
    },

    // Forum 301 - Mobilités douces
    {
        id: 3001,
        forum: F(301),
        author: U(5),
        content: "Généraliser les pistes bidirectionnelles en centre-ville, bonne idée ?",
        medias: [m("image", "https://picsum.photos/seed/velo/640/360")],
        likeCount: 102,
        commentCount: 5,
        createdAt: new Date("2025-11-05T07:45:00Z"),
        updatedAt: new Date("2025-11-05T07:45:00Z"),
    },

    // Forum 302 - Rail
    {
        id: 3101,
        forum: F(302),
        author: U(1),
        content: "RER métropolitains : prioriser les nœuds ferroviaires ou les rames neuves ?",
        medias: [],
        likeCount: 77,
        commentCount: 4,
        createdAt: new Date("2025-11-01T13:30:00Z"),
        updatedAt: new Date("2025-11-01T13:30:00Z"),
    },
];

// ==== Commentaires ====
export const commentsByPostId: CommentServerDto[] = [
    // POST 1001
    {
        comment_id: "5001",
        post_id: "1001",
        author_id: "2",
        author_username: "Basile Sens",
        parent_comment_id: null,
        content: "Oui, surtout sur les écoles et gymnases déjà bien exposés.",
        created_at: "2025-10-31T09:30:00Z",
        updated_at: "2025-10-31T09:30:00Z",
    },
    {
        comment_id: "5002",
        post_id: "1001",
        author_id: "1",
        author_username: "Omri Zakaria Dakka",
        parent_comment_id: "5001",
        content: "On peut mutualiser la production pour les quartiers.",
        created_at: "2025-10-31T10:15:00Z",
        updated_at: "2025-10-31T10:15:00Z",
    },
    {
        comment_id: "5003",
        post_id: "1001",
        author_id: "4",
        author_username: "Pierre Maunier",
        parent_comment_id: null,
        content: "Attention aux contraintes structurelles des toitures anciennes.",
        created_at: "2025-10-31T11:00:00Z",
        updated_at: "2025-10-31T11:00:00Z",
    },

    // POST 1002
    {
        comment_id: "5010",
        post_id: "1002",
        author_id: "6",
        author_username: "Inès Metiba",
        parent_comment_id: null,
        content: "Un dispositif universel mais dégressif selon les revenus.",
        created_at: "2025-11-02T11:20:00Z",
        updated_at: "2025-11-02T11:20:00Z",
    },
    {
        comment_id: "5011",
        post_id: "1002",
        author_id: "5",
        author_username: "Titouan Gragnic",
        parent_comment_id: "5010",
        content: "+1, et bonus pour les passoires thermiques.",
        created_at: "2025-11-02T12:10:00Z",
        updated_at: "2025-11-02T12:10:00Z",
    },

    // POST 1101
    {
        comment_id: "5020",
        post_id: "1101",
        author_id: "3",
        author_username: "Alex Blanco",
        parent_comment_id: null,
        content: "Les trames vertes doivent être opposables aux PLU.",
        created_at: "2025-10-28T16:55:00Z",
        updated_at: "2025-10-28T16:55:00Z",
    },
    {
        comment_id: "5021",
        post_id: "1101",
        author_id: "4",
        author_username: "Pierre Maunier",
        parent_comment_id: "5020",
        content: "Et financées via les projets d’aménagement.",
        created_at: "2025-10-28T17:10:00Z",
        updated_at: "2025-10-28T17:10:00Z",
    },
    {
        comment_id: "5022",
        post_id: "1101",
        author_id: "1",
        author_username: "Omri Zakaria Dakka",
        parent_comment_id: "5020",
        content: "Mesurer l’efficacité par espèces indicatrices.",
        created_at: "2025-10-28T17:35:00Z",
        updated_at: "2025-10-28T17:35:00Z",
    },

    // POST 2001
    {
        comment_id: "5030",
        post_id: "2001",
        author_id: "5",
        author_username: "Titouan Gragnic",
        parent_comment_id: null,
        content: "Oui, fléchage minimal pour entretien des monuments.",
        created_at: "2025-11-03T09:10:00Z",
        updated_at: "2025-11-03T09:10:00Z",
    },
    {
        comment_id: "5031",
        post_id: "2001",
        author_id: "2",
        author_username: "Basile Sens",
        parent_comment_id: null,
        content: "Et conditionner à la médiation culturelle locale.",
        created_at: "2025-11-03T09:45:00Z",
        updated_at: "2025-11-03T09:45:00Z",
    },
    {
        comment_id: "5032",
        post_id: "2001",
        author_id: "6",
        author_username: "Inès Metiba",
        parent_comment_id: "5031",
        content: "Bonne idée pour l’ancrage territorial.",
        created_at: "2025-11-03T10:05:00Z",
        updated_at: "2025-11-03T10:05:00Z",
    },

    // POST 2002
    {
        comment_id: "5040",
        post_id: "2002",
        author_id: "1",
        author_username: "Omri Zakaria Dakka",
        parent_comment_id: null,
        content: "Indexation sur quotient familial pour éviter les effets d’aubaine.",
        created_at: "2025-11-04T16:00:00Z",
        updated_at: "2025-11-04T16:00:00Z",
    },
    {
        comment_id: "5041",
        post_id: "2002",
        author_id: "3",
        author_username: "Alex Blanco",
        parent_comment_id: null,
        content: "Quota de billets solidaires imposé aux organisateurs ?",
        created_at: "2025-11-04T16:20:00Z",
        updated_at: "2025-11-04T16:20:00Z",
    },

    // POST 2101
    {
        comment_id: "5050",
        post_id: "2101",
        author_id: "2",
        author_username: "Basile Sens",
        parent_comment_id: null,
        content: "Gouvernance indépendante + comité des donateurs non décisionnel.",
        created_at: "2025-10-26T19:30:00Z",
        updated_at: "2025-10-26T19:30:00Z",
    },
    {
        comment_id: "5051",
        post_id: "2101",
        author_id: "6",
        author_username: "Inès Metiba",
        parent_comment_id: null,
        content: "Transparence : rapport public annuel par média aidé.",
        created_at: "2025-10-26T19:50:00Z",
        updated_at: "2025-10-26T19:50:00Z",
    },

    // POST 3001
    {
        comment_id: "5060",
        post_id: "3001",
        author_id: "4",
        author_username: "Pierre Maunier",
        parent_comment_id: null,
        content: "Attention aux carrefours : priorité à droite peu lisible.",
        created_at: "2025-11-05T07:55:00Z",
        updated_at: "2025-11-05T07:55:00Z",
    },
    {
        comment_id: "5061",
        post_id: "3001",
        author_id: "5",
        author_username: "Titouan Gragnic",
        parent_comment_id: "5060",
        content: "Traitements en plateau + marquage renforcé.",
        created_at: "2025-11-05T08:10:00Z",
        updated_at: "2025-11-05T08:10:00Z",
    },

    // POST 3101
    {
        comment_id: "5070",
        post_id: "3101",
        author_id: "3",
        author_username: "Alex Blanco",
        parent_comment_id: null,
        content: "D’abord les nœuds : ils démultiplient l’effet des rames.",
        created_at: "2025-11-01T14:00:00Z",
        updated_at: "2025-11-01T14:00:00Z",
    },
    {
        comment_id: "5071",
        post_id: "3101",
        author_id: "1",
        author_username: "Omri Zakaria Dakka",
        parent_comment_id: null,
        content: "D’accord, mais moderniser le matériel réduit aussi les pannes.",
        created_at: "2025-11-01T14:25:00Z",
        updated_at: "2025-11-01T14:25:00Z",
    },
];

// ==== FullPosts (post + commentaires) ====
export const fullPosts: FullPost[] = (posts || []).map(p => ({
    post: p,
    comments: commentsByPostId.filter(c => c.post_id === p.id.toString()),
} as unknown as FullPost));

// ==== FullForums (forum + posts du forum) ====
export const fullForums: FullForum[] = [
    { forum: F(101), posts: posts.filter(p => p.forum?.id === 101) },
    { forum: F(102), posts: posts.filter(p => p.forum?.id === 102) },
    { forum: F(201), posts: posts.filter(p => p.forum?.id === 201) },
    { forum: F(202), posts: posts.filter(p => p.forum?.id === 202) },
    { forum: F(301), posts: posts.filter(p => p.forum?.id === 301) },
    { forum: F(302), posts: posts.filter(p => p.forum?.id === 302) },
];

// ==== Chats ====
export const chats: SimpleChat[] = [
    { id: 9001, user: U(1) },
    { id: 9002, user: U(2) },
];

export const messagesByChatId: Record<number, Message[]> = {
    9001: [
        { author: U(2), content: "Tu as vu le thread sur les RER métropolitains ?" },
        { author: U(1), content: "Oui, je pense qu’il faut prioriser les nœuds." },
        { author: U(2), content: "Go résumer et proposer un amendement." },
    ],
    9002: [
        { author: U(6), content: "On monte un questionnaire sur la tarification sociale ?" },
        { author: U(2), content: "Partant, je prépare un doc ce soir." },
    ],
};

export const fullChats: FullChat[] = chats.map(c => ({
    chat: c,
    messages: messagesByChatId[c.id] ?? [],
}));

// ==== Profiles ====
export const profiles: Profile[] = [
    {
        user: U(1),
        voteCount: 128,
        bio: "Ingénieure énergie. Intérêt : solaire, rail, culture scientifique.",
        posts: [posts.find(p => p.author.id === 1)!],
    },
    {
        user: U(2),
        voteCount: 96,
        bio: "Une vraie citoyenne curieuse.",
        posts: [posts.find(p => p.author.id === 2)!],
    },
    {
        user: U(3),
        voteCount: 74,
        bio: "Journalisme & politiques culturelles.",
        posts: [posts.find(p => p.author.id === 6)!],
    },
    {
        user: U(4),
        voteCount: 128,
        bio: "Ingénieure énergie. Intérêt : solaire, rail, culture scientifique.",
        posts: [posts.find(p => p.author.id === 1)!],
    },
    {
        user: U(5),
        voteCount: 96,
        bio: "Dev & citoyen curieux. Intérêt : mobilité, open data, audio.",
        posts: [posts.find(p => p.author.id === 2)!],
    },
    {
        user: U(6),
        voteCount: 74,
        bio: "Journalisme & politiques culturelles.",
        posts: [posts.find(p => p.author.id === 6)!],
    },
];

// ==== Settings (attention: le type utilise shuwMyVote) ====
export const democracySettings: DemocracySettings = {
    shuwMyVote: false, // (sic) orthographe du type respectée
    limitVotes: true,
};

export const socialSettings: SocialSettings = {
    public: true,
};

export const settings: Settings = {
    democracy: democracySettings,
    social: socialSettings,
};

// ==== Votes de l'utilisateur courant (exemple) ====
export const myVotes: MyVotes = [U(1), U(4), U(5)];

// ==== For You (suggestions) ====
export const forYou: ForYouResults = {
    users: profiles,
    posts: [posts[0], posts[3], posts[6], posts[8]].filter(Boolean),
};

// ==== Exemples de payloads de création de post ====
export const createPostSamples: CreatePost[] = [
    {
        title: "Plan vélo 2030 : priorité aux collèges",
        content: "Déployer des voies sécurisées autour de chaque établissement.",
        medias: m("image", "https://picsum.photos/seed/planvelo/640/360"),
    },
    {
        title: "Fonds d’aide à l’investigation locale",
        content: "Proposition d’un modèle d’allocation transparent et indépendant.",
        medias: m("link", "https://example.org/whitepaper.pdf"),
    },
];

// ==== Export global pratique ====
export const db = {
    domains,
    users,
    forums,
    posts,
    commentsByPostId,
    fullPosts,
    fullForums,
    chats,
    messagesByChatId,
    fullChats,
    profiles,
    settings,
    myVotes,
    forYou,
    createPostSamples,
};

export default db;
