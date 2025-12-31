import { socialApiClient } from '../client';
import { PostMediaDto } from '@/api/dtos/post-media.dto';
import { UserProfileDto } from '@/api/dtos/user-profile.dto';
import { UserDto } from '@/api/dtos/user.dto';
import { ForumDto } from '@/api/dtos/forum.dto';
import {FullPost} from "@/api/types/post/full-post";
import {SimpleUser} from "@/api/types/common/simple-user";
import {SimpleForum} from "@/api/types/forum/simple-forum";
import {SimplePost} from "@/api/types/common/simple-post";
import { Comment } from "@/api/types/post/comment";
import {getInStoreUsageOfRealData} from "@/api/utils";
import {getCommentsReplies, getFeed, getPost} from "@/api/mock/functions";

export interface CreatePostDto {
  title : string;
  content: string;
  subforum_id: string;
}

export interface Like {
  like_id: string;
  user_id: string;
  username: string;
  post_id: string;
  created_at: string;
}

export interface CreateCommentDto {
  content: string;
  parent_comment_id?: string | null;
}

export interface CommentServerDto {
  comment_id: string;
  post_id: string;
  author_id: string;
  author_username: string;
  parent_comment_id: string | null;
  content: string;
  created_at: string;
  updated_at: string;
}

/**
 * Convertit les commentaires plats du serveur en structure hiérarchisée
 */
function buildHierarchicalComments(flatComments: CommentServerDto[]): Comment[] {
  const commentMap = new Map<string, Comment>();
  
  // Créer tous les commentaires
  flatComments.forEach(dto => {
    commentMap.set(dto.comment_id, {
      commentId: dto.comment_id as any,
      author: {
        id: dto.author_id,
        displayName: dto.author_username,
        profilePictureUrl: "https://picsum.photos/200",
      } as SimpleUser,
      content: dto.content,
      subComments: [],
      createdAt: new Date(dto.created_at),
      updatedAt: new Date(dto.updated_at),
    });
  });

  const rootComments: Comment[] = [];

  // Organiser la hiérarchie
  flatComments.forEach(dto => {
    const comment = commentMap.get(dto.comment_id)!;
    if (dto.parent_comment_id) {
      const parentComment = commentMap.get(dto.parent_comment_id);
      if (parentComment) {
        parentComment.subComments.push(comment);
      }
    } else {
      rootComments.push(comment);
    }
  });

  return rootComments;
}

interface PostServerDto {
    post_id: string;
    author_id: string;
    author_username: string;
    subforum_id: string;
    title: string;
    content: string;
    content_signature: string;
    likes_count: number;
    comments_count: number;
    created_at: string;
    updated_at: string;
}

async function postServerDtoToFullPost(dto: PostServerDto): Promise<FullPost> {
    const post = new FullPost();
    post.post = new SimplePost();
    post.post.id = dto.post_id;
    post.post.title = dto.title;
    post.post.content = dto.content;
    post.post.createdAt = new Date(dto.created_at);
    post.post.updatedAt = new Date(dto.updated_at);
    post.post.likeCount = dto.likes_count;
    post.post.commentCount = dto.comments_count;
    post.post.liked = false;
    if (dto.likes_count > 0) {
      if (await postService.likePost(dto.post_id)) {
        postService.unlikePost(dto.post_id).then(() => post);
      }
      else {
        post.post.liked = true;
      } 

    }

    // Mapping de l'auteur
    const author = new SimpleUser()
    author.id = dto.author_id;
    author.profilePictureUrl = "https://picsum.photos/200"; //FIXME
    author.displayName = dto.author_username;

    post.post.author = author;
    
    // Mapping du forum
    const forum = new SimpleForum();
    forum.id = dto.subforum_id;
    post.post.forum = forum;
    
    // Initialisation des tableaux vides
    post.post.medias = [];
    post.comments = [];
    
    return post;
}

function postServerDtoToSimplePost(dto: PostServerDto): SimplePost {
  const post = new SimplePost();
  post.id = dto.post_id;
  post.title = dto.title;
  post.content = dto.content;
  post.createdAt = new Date(dto.created_at);
  post.updatedAt = new Date(dto.updated_at);

  // Mapping de l'auteur
  const author = new SimpleUser()
  author.id = dto.author_id;
  author.profilePictureUrl = "https://picsum.photos/200"; //FIXME
  author.displayName = dto.author_username;

  post.author = author;

  return post;
}

/**
 * Service pour interagir avec les posts de l'API Social (localhost:8000)
 */
export const postService = {
  /**
   * Crée un nouveau post
   * POST /api/v1/posts/create/
   */
  async createPost(postData: CreatePostDto): Promise<FullPost> {
    try {
      const response = await socialApiClient.post<PostServerDto>('/api/v1/posts/create/', postData);
      return postServerDtoToFullPost(response.data);
    } catch (error: any) {
      console.error('Erreur lors de la création du post:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Récupère les posts à découvrir
   * GET /api/v1/posts/discover/
   */
  async getDiscoverPosts(): Promise<SimplePost[]> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<PostServerDto[]>('/api/v1/posts/discover/');
        return response.data.map(postServerDtoToSimplePost);
      } catch (error: any) {
        console.error('Erreur lors de la récupération des posts discover:', error.response?.data || error.message);
        throw error;
      }
    }
    const posts = getFeed();
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(posts);
      }, 300);
    });
  },

  /**
   * Récupère le feed de posts de l'utilisateur connecté
   * GET /api/v1/posts/feed/
   */
  async getFeedPosts(): Promise<SimplePost[]> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<PostServerDto[]>('/api/v1/posts/feed/');
        return response.data.map(postServerDtoToSimplePost);
      } catch (error: any) {
        console.error('Erreur lors de la récupération du feed:', error.response?.data || error.message);
        throw error;
      }
    }
    const posts = getFeed();
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(posts);
      }, 300);
    });
  },

  /**
   * Récupère un post par son ID
   * GET /api/v1/posts/{post_id}/
   */
  async getPostById(postId: string): Promise<FullPost> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<PostServerDto>(`/api/v1/posts/${postId}/`);
        return postServerDtoToFullPost(response.data);
      } catch (error: any) {
        console.error('Erreur lors de la récupération du post:', error.response?.data || error.message);
        throw error;
      }
    }
    const post = getPost(postId);
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if(post){
          resolve(post);
        }
        reject("Erreur lors de la récupération du post");
      }, 300);
    });
  },

  /**
   * Supprime un post
   * DELETE /api/v1/posts/{post_id}/delete/
   */
  async deletePost(postId: string): Promise<void> {
    try {
      await socialApiClient.delete(`/api/v1/posts/${postId}/delete/`);
    } catch (error: any) {
      console.error('Erreur lors de la suppression du post:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Like un post
   * POST /api/v1/posts/{post_id}/like/
   */
  async likePost(postId: string): Promise<Like | null> {
    try {
      const response = await socialApiClient.post(`/api/v1/posts/${postId}/like/`);
      return response.data as Like;
    } catch (error: any) {
      if (error.response && error.response.status === 400) {
        return null;
      }
      console.error('Erreur lors du like du post:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Récupère les likes d'un post
   * GET /api/v1/posts/{post_id}/likes/
   */
  async getPostLikes(postId: string): Promise<number> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<Like[]>(`/api/v1/posts/${postId}/likes/`);
        return response.data.length;
      } catch (error: any) {
        console.error('Erreur lors de la récupération des likes:', error.response?.data || error.message);
        throw error;
      }
    }
    const post = getPost(postId);
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if(post){
          resolve(post.post.likeCount);
        }
        reject("Erreur lors de la récupération des likes");
      }, 300);
    });
  },

  /**
   * Unlike un post
   * DELETE /api/v1/posts/{post_id}/unlikes/
   */
  async unlikePost(postId: string): Promise<void> {
    try {
      await socialApiClient.delete(`/api/v1/posts/${postId}/unlikes/`);
    } catch (error: any) {
      console.error('Erreur lors du unlike du post:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Récupère les commentaires d'un post
   * GET /api/v1/comments/posts/{post_id}/
   */
  async getPostComments(postId: string): Promise<CommentServerDto[]> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<CommentServerDto[]>(`/api/v1/comments/posts/${postId}/`);
        return response.data;
      } catch (error: any) {
        console.error('Erreur lors de la récupération des commentaires:', error.response?.data || error.message);
        throw error;
      }
    }
    const post = getPost(postId);
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if(post){
          resolve(post.comments);
        }
        reject("Erreur lors de la récupération des commentaires");
      }, 300);
    });
  },

  /**
   * Crée un commentaire sur un post
   * POST /api/v1/comments/posts/{post_id}/create/
   */
  async createComment(postId: string, commentData: CreateCommentDto): Promise<CommentServerDto> {
    try {
      const response = await socialApiClient.post<CommentServerDto>(
        `/api/v1/comments/posts/${postId}/create/`,
        commentData
      );
      return response.data;
    } catch (error: any) {
      console.error('Erreur lors de la création du commentaire:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Supprime un commentaire
   * DELETE /api/v1/comments/{comment_id}/delete/
   */
  async deleteComment(commentId: string): Promise<void> {
    try {
      await socialApiClient.delete(`/api/v1/comments/${commentId}/delete/`);
    } catch (error: any) {
      console.error('Erreur lors de la suppression du commentaire:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Récupère les réponses d'un commentaire
   * GET /api/v1/comments/{comment_id}/replies/
   */
  async getCommentReplies(commentId: string): Promise<CommentServerDto[]> {
    const isUsingRealData = await getInStoreUsageOfRealData();
    if (isUsingRealData === "true") {
      try {
        const response = await socialApiClient.get<CommentServerDto[]>(`/api/v1/comments/${commentId}/replies/`);
        return response.data;
      } catch (error: any) {
        console.error('Erreur lors de la récupération des réponses:', error.response?.data || error.message);
        throw error;
      }
    }
    const comments = getCommentsReplies(commentId);
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if(comments){
          resolve(comments);
        }
        reject("Erreur lors de la récupération des réponses");
      }, 300);
    });
  },

  /**
   * Convertit les commentaires plats du serveur en structure hiérarchisée
   */
  convertFlatCommentsToHierarchical(flatComments: CommentServerDto[]): Comment[] {
    return buildHierarchicalComments(flatComments);
  },

};

