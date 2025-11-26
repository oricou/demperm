import Post from './post';
// Definition of the Theme interface
interface Theme{
    uuid: string;
    name: string;
    likes: number;
    description: string;
    posts: Post[]
}
export default Theme;