import Comments from "./comments";

// Definition of the Post interface
interface Post{
    uuid: string;
    title: string;
    content: string;
    picture: string | null;
    timestamp: Date;
    ownerId: number;
    alias: string;
    theme: string;
    likes: number;
    comments: Comments[];
}

export default Post;