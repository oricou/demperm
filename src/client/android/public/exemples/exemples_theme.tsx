import Theme from '@/types/theme';
import { Post1, Post2, Post3 } from './exemples_posts';

//This file aims to show some example posts to test the PostComponent
const theme1: Theme = {
    uuid: "t1a2b3d4-e5f6-7890-ab12-cd34ef56gh78",
    name: "ThèmeExemple1",
    description: "oui c'est un exempleeeeeeeeeeeeeeeeeee ouais ouais ouais.",
    likes: 1500,
    posts: [Post1, Post2, Post3],
};

const theme2: Theme = {
    uuid: "t1b2b3d4-e5f6-7890-ab12-dd34ef56gh79",
    name: "ThèmeExemple2",
    description: "oui c'est un exememr,zpr,ozezpleeeeeeeeeeeeeeeeeee ouais ouais ouais.",
    likes: 10,
    posts: [],
};

const theme3: Theme = {
    uuid: "t1a2b3d4-e5f6-7890-ab12-dd34ef56gh79",
    name: "ThèmeExemple3",
    description: "oui c'est un exempleeeeeeeeeeeeeeeeeee ouais ouais ouais.",
    likes: 10,
    posts: [],
};

const theme4: Theme = {
    uuid: "t1a2b3d4-e5f6-6890-ab12-cd34ef56gh79",
    name: "ThèmeExemple4",
    description: "oui c'est un exemkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkpleeeeeeeeeeeeeeeeeee ouais ouais ouais.",
    likes: 10,
    posts: [],
};

const theme5: Theme = {
    uuid: "t1a2b3d4-e5f6-7890-ab22-cd34ef56gh79",
    name: "ThèmeExemple5",
    description: "oui c'est un exempleeeeeeeeeeeeeeeeeee ouais ouais ouais.",
    likes: 10,
    posts: [],
};

const theme6: Theme = {
    uuid: "t1a2b3d4-e5f6-7890-ab92-cd34ef56gh79",
    name: "ThèmeExemple9",
    description: "oui c'est un exempleeeeeeeeeeeeeeeeeee ouais ouais ouais.",
    likes: 10,
    posts: [],
};

export { theme1, theme2,theme3, theme4, theme5, theme6 };
