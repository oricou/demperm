// Definition of the Post interface
interface Post{
    post_id: string;
    author_id: string;
    author_username: string;
    subforum_id: string;
    title: string;
    content: string;
    content_signature: string;
    like_count: number;
    comment_count: number;
    created_at: string;
    updated_at: string;
}

export default Post;