import Post from '@/types/post';
import {Comment1, Comment2, Comment3} from './exemples_comments';

//This file aims to show some example posts to test the PostComponent
const Post1: Post = {
    uuid: '596d8c9d-d006-472b-88ab-2914fe78a5da',
    title: 'Mooo!',
    content: 'Got milk, bitch? Got beef? (Got beef?)\n'
    +'Got steak, ho? Got cheese? (You got it?) Grade A, ho, not lean (not lean)\n'
    +'Got me A1, sauce, please\nThese heifers got nothin\' on me\nStakes high, need a side of collard greens (collard greens)\nCash rules everythin\' around me (everythin\' around me)\nIce cream, ice cream (ice cream)\n'
    + 'You a calf, bitch, you my daughter (you my daughter)\nI ain\'t bothered (I ain\'t bothered), get slaughtered (get slaughtered)\nGot the methane, I\'m a farter (woo)',
    picture: null,
    alias: 'Palo la boss',
    timestamp: new Date(),
    ownerId: 1,
    theme: 'ThèmeExemple2',
    likes: 107,
    comments: []
};

const Post2: Post = {
    uuid: 'd4fa1632-335f-49e5-a08e-b44ee951d46a',
    title: 'Fourmi',
    content: 'Les fourmis sont des insectes, de l\'ordre des Hyménoptères et du sous-ordre des Apocrites, qui constituent la famille des Formicidés (Formicidae).Ce sont des animaux eusociaux qui forment des colonies appelées fourmilières, comportant de quelques dizaines d\'individus à plusieurs millions et parfois extrêmement complexes. Certaines espèces forment des supercolonies de plusieurs centaines de millions d\'individus. Les sociétés de fourmis ont une division du travail (polyéthisme d\'âge et de caste), une communication entre individus et une capacité à résoudre des problèmes complexes. Ces analogies avec les sociétés humaines ont depuis longtemps été une source d\'inspiration et le sujet d\'études scientifiques.',
    picture: null,
    alias: 'Palo la boss',
    timestamp: new Date(),
    ownerId: 1,
    theme: 'Centres d\'intérêt',
    likes: 961,
    comments: [Comment3, Comment1]
};

const Post3: Post = {
    uuid: 'd4fa1632-335f-49e5-a08e-b44ee951d47a',
    title: 'Pieuvre',
    content: 'Pieuvre (f) et poulpe (m) sont des noms vernaculaires ambigus désignant en français certains céphalopodes benthiques du sous-ordre Incirrina (principalement la famille des octopodidés, de l\'ordre Octopoda). Ces animaux sentients se caractérisent, au sein des céphalopodes, par leur grande intelligence et leur capacité à changer de couleur au millième de seconde, à leur guise, par mimétisme avec leur environnement ou en fonction de leurs émotions. Leur corps est entièrement souple, hormis un bec qui ressemble à certains égards à celui des perroquets. Leurs huit bras sont pourvus de ventouses et leur sang est transparent-bleuâtre.',
    picture: null,
    alias: 'Palo la boss',
    timestamp: new Date(),
    ownerId: 1,
    theme: 'Centres d\'intérêt',
    likes: 571,
    comments: []
};

export { Post1, Post2, Post3 };