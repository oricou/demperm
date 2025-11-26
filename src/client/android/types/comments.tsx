// Definition of the Comments interface
interface Comments{
    uuid: string;
    postId: string;
    alias: string;
    authorId: number;
    content: string;
    timestamp: Date;
    likes: number;
    answers: Comments[];
}
export default Comments;