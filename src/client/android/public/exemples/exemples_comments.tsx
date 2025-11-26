import Comments from '@/types/comments';

//This file aims to show some example posts to test the CommentComponent
const Comment1: Comments = {
    uuid: "c1a2b3d4-e5f6-7890-ab12-cd34ef56gh78",
    postId: "596d8c9d-d006-472b-88ab-2914fe78a5da",
    alias: "Hugo Saison",
    authorId: 2,
    content: "Ouais t'as grave raison",
    timestamp: new Date(),
    likes: 191,
    answers: [],
};

const Comment2: Comments = {
    uuid: "c2a2b3d4-e5f6-7890-ab12-cd34ef56gh78",
    postId: "d4fa1632-335f-49e5-a08e-b44ee951d46a",
    alias: "Absolument tout le monde",
    authorId: 2,
    content: "Je suis totalement d'accord avec toi",
    timestamp: new Date(),
    likes: 361,
    answers: [],
};

const Comment4: Comments = {
    uuid: "c2a2b3d4-e5f6-7810-ab12-cd34ef56gh79",
    postId: "d4fa1632-335f-49e5-a08e-b44ee951d46a",
    alias: "Test",
    authorId: 2,
    content: "Je suis totalement d'accord avec toi",
    timestamp: new Date(),
    likes: 361,
    answers: [],
};

const Comment3: Comments = {
    uuid: "c2a2b3d4-e5f6-7890-ab12-cd34ef56gh79",
    postId: "d4fa1632-335f-49e5-a08e-b44ee951d46a",
    alias: "Hugo saison",
    authorId: 2,
    content: "Tu mérites d'avoir 20/20 carrément",
    timestamp: new Date(),
    likes: 641,
    answers: [Comment2, Comment4],
};

export { Comment1, Comment2, Comment3, Comment4 };