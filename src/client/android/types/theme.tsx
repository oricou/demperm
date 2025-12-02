// Definition of the Theme interface
interface Theme{
    forum_id: string;
    name: string;
    description: string;
    creator_id: string;
    member_count: number;
    post_count: number;
    created_at: string;
}
export default Theme;