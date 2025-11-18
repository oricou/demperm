export type iconVariants =
    'home'
    | 'paper-plane'
    | 'person-add'
    | 'megaphone'
    | 'heart'
    | 'chatbox'
    | 'chatbubbles'
    | 'share-social'
    | 'duplicate'
    | 'repeat'
    | 'search'
    | 'person'
    | 'newspaper'
    | 'create'
    | 'bookmark'
    | 'close'
    | 'settings'
    | 'chevron-back'
    | 'add'
    | 'chevron-down'
    | 'image'
    | 'exit';

export const fontFamily : string = 'Inter-Regular, sans-serif';

export type Ministere =
    | "Écologie"
    | "Agriculture"
    | "Transports"
    | "Santé"
    | "Éducation"
    | "Économie"
    | "Finances"
    | "Industrie"
    | "Intérieur"
    | "Sécurité"
    | "Justice"
    | "Culture"
    | "Défense"
    | "Travail"
    | "Recherche"
    | "Enseignement supérieur"
    | "Logement"
    | "Territoires"
    | "Numérique"
    | "Outre-mer"
    | "Affaires étrangères"
    | "Europe";

export const ministereDomainColors: Record<Ministere, string> = {
    "Écologie": "#A8E6CF",
    "Agriculture": "#91D18B",
    "Transports": "#FF8B94",
    "Santé": "#A0CED9",
    "Éducation": "#AED9E0",
    "Économie": "#C9A0DC",
    "Finances": "#C3B091",
    "Industrie": "#B2B7FF",
    "Intérieur": "#9AC3FF",
    "Sécurité": "#7FA6E6",
    "Justice": "#B0BEC5",
    "Culture": "#D7A9E3",
    "Défense": "#B0B7C3",
    "Travail": "#FFBC99",
    "Recherche": "#C7B5E6",
    "Enseignement supérieur": "#B7C6F6",
    "Logement": "#D0B8A8",
    "Territoires": "#A7E3DD",
    "Numérique": "#9FE3E8",
    "Outre-mer": "#9DD7E0",
    "Affaires étrangères": "#9EBBE6",
    "Europe": "#A7B8E9"
}