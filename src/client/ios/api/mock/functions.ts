import {db, users} from "@/api/mock/db";
import * as domain from "node:domain";

const myUser = db.users[1];

export const getChats = function () {
    return db.chats;
}

export const getChat = function (id: number) {
    return db.fullChats.find(chat => chat.chat.id == id);
}

export const getFeed = function () {
    return db.posts;
}

export const getPost = function (id: string) {
    return db.fullPosts.find(post => post.post.id == id);
}

export const getCommentsReplies = function(commentId: string) {
    return db.commentsByPostId.filter(comment => comment.parent_comment_id === commentId);
}

export const getForYouPage = function () {
    return db.forYou;
}

export const getLeaderboard = function () {
    return db.users.sort((a, b) => {
        return a.voteCount - b.voteCount
    })
}

export const getNews = function () {
    return db.posts;
}

export const getFavorites = function () {
    return db.users;
}

export const getDomains = function () {
    return db.domains;
}

export const getForums = function (id: number) {
    return db.forums.filter(forum => forum.domains.find(domain => domain.id == id));
}

export const searchInForums = function (query: string) {
    return db.forums.filter(forum => forum.description.includes(query) || forum.title.includes(query));
}

export const discoverUsers = function () {
    return db.profiles;
}

export const getForum = function (id: number) {
    return db.fullForums.find(forum => forum.forum.id == id);
}

export const getMyForums = function () {
    return db.forums;
}

export const getMyProfile = function () {
    return db.profiles.find(profile => profile.user.id == 2);
}

export const getMyVotes = function () {
    return db.myVotes;
}

export const getProfile = function (id: number) {
    return db.profiles.find(profile => profile.user.id == id);
}

export const getSettings = function () {
    return db.settings;
}