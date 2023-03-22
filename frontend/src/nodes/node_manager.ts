import API from "./api";
import {Author, CommentListItem, ListItem, Post, Comment, Like, InboxListItem} from "../index";


class NodeManager  {
    private nodes: {
        [key: string]: API;
    }

    constructor(nodes: { [key: string]: API }) {
        this.nodes = nodes;
    }

    public addNode(node: { [key: string]: API }): void {
        this.nodes = {...this.nodes, ...node};
    }

    public removeNode(nodeId: string): void {
        delete this.nodes[nodeId];
    }

    public getNodes(): {[key: string]:API} {
        return this.nodes;
    }

    public async checkAuthorExists(authorId: string): Promise<boolean> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                if (await node.getAuthor(authorId)) {
                    return true;
                }
            }
        }
        return false;
    }

    public async getAuthor(authorId: string, nodeId:string = 'all'): Promise<Author | undefined> {
        if (nodeId === 'all') {
            for (const node of Object.values(this.nodes)) {
                const author = await node.getAuthor(authorId);
                if (author) {
                    return author;
                }
            }
            return undefined;
        } else {
            return await this.nodes[nodeId].getAuthor(authorId);
        }
    }

    public async createAuthor(author:Author) {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.createAuthor(author);
            }
        }
        throw new Error("No local node found");
    }

    public async getAuthors(page:number = 0, size:number = 25, nodeId:string | 'all'):Promise<ListItem<Author>> {
        if (nodeId === 'all') {
            let authors: Author[] = [];
            for (const node of Object.values(this.nodes)) {
                const results = await node.getAuthors(page, size);
                authors = authors.concat(results.items);
            }
            return {
                type: "authors",
                items: authors
            }
        } else {
            return await this.nodes[nodeId].getAuthors(page, size);
        }
    }

    public async updateAuthor(authorId: string): Promise<Author> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.updateAuthor(authorId);
            }
        }
        throw new Error("No local node found");
    }

    public async getFollowers(authorId: string, nodeId:string = 'all'): Promise<ListItem<Author>> {
        if (nodeId === 'all') {
            let authors: Author[] = [];
            for (const node of Object.values(this.nodes)) {
                const results = await node.getFollowers(authorId);
                authors = authors.concat(results.items);
            }
            return {
                type: "authors",
                items: authors
            }
        } else {
            return await this.nodes[nodeId].getFollowers(authorId);
        }
    }

    public async addFollower(authorId: string, foreignAuthorId: string): Promise<void> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.addFollower(authorId, foreignAuthorId);
            }
        }
        throw new Error("No local node found");
    }

    public async checkFollower(authorId: string, foreignAuthorId: string): Promise<boolean> {
        for (const node of Object.values(this.nodes)) {
            const result = await node.checkFollower(authorId, foreignAuthorId);
            if (result) {
                return true;
            }
        }
        return false;
    }

    public async removeFollower(authorId: string, foreignAuthorId: string): Promise<void> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.removeFollower(authorId, foreignAuthorId);
            }
        }
        throw new Error("No local node found");
    }

    public async sendFollowRequest(authorTo:Author, authorFrom:Author):Promise<void> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.sendFollowRequest(authorTo, authorFrom);
            }
        }
        throw new Error("No local node found");
    }

    public async getPost(authorId:string, postId: string, nodeId:string = 'all'): Promise<Post | undefined> {
        if (nodeId === 'all') {
            for (const node of Object.values(this.nodes)) {
                const post = await node.getPost(authorId, postId);
                if (post) {
                    return post;
                }
            }
            return undefined;
        } else {
            return await this.nodes[nodeId].getPost(authorId, postId);
        }
    }

    public async getPosts(authorId:string, page:number = 0, size:number = 25, nodeId:string = 'all'): Promise<ListItem<Post>> {
        if (nodeId === 'all') {
            let posts: Post[] = [];
            for (const node of Object.values(this.nodes)) {
                const results = await node.getPosts(authorId, page, size);
                posts = posts.concat(results.items);
            }
            return {
                type: "posts",
                items: posts
            }
        } else {
            return await this.nodes[nodeId].getPosts(authorId, page, size);
        }
    }

    public async createPost(authorId: string, post: Post): Promise<Post> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.createPost(authorId, post);
            }
        }
        throw new Error("No local node found");
    }

    public async updatePost(authorId: string, postId: string, post: Post): Promise<Post> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.updatePost(postId, post);
            }
        }
        throw new Error("No local node found");
    }

    public async deletePost(authorId: string, postId: string): Promise<void> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.deletePost(authorId, postId);
            }
        }
        throw new Error("No local node found");
    }

    public async getComments(authorId:string, postId: string, page:number = 0, size:number = 25, nodeId:string = 'all'): Promise<CommentListItem> {
        if (nodeId === 'all') {
            let comments: Comment[] = [];
            let post =''
            let id = ''
            for (const node of Object.values(this.nodes)) {
                const results = await node.getComments(authorId, postId, page, size);
                post = results.post;
                id = results.id;
                comments = comments.concat(results.comments);
            }
            return {
                type: "comments",
                comments: comments,
                page: page,
                post: post,
                size: size,
                id: id
            }
        } else {
            return await this.nodes[nodeId].getComments(authorId, postId, page, size);
        }
    }

    public async createComment(authorId: string, postId: string, comment: Comment): Promise<Comment> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.createComment(authorId, postId, comment);
            }
        }
        throw new Error("No local node found");
    }

    public async createLike(authorId: string, post:Post, authorFrom:Author): Promise<void> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.createLike(authorId, post, authorFrom);
            }
        }
        throw new Error("No local node found");
    }

    public async createCommentLike(authorId: string, comment:Comment, authorFrom:Author):Promise<void> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.createCommentLike(authorId, comment, authorFrom);
            }
        }
        throw new Error("No local node found");
    }

    public async getLiked(authorId:string, nodeId:string = 'all'): Promise<ListItem<Like>> {
        if (nodeId === 'all') {
            let likes: Like[] = [];
            for (const node of Object.values(this.nodes)) {
                const results = await node.getLiked(authorId);
                likes = likes.concat(results.items);
            }
            return {
                type: "likes",
                items: likes
            }
        } else {
            return await this.nodes[nodeId].getLiked(authorId);
        }
    }

    public async getInbox(authorId: string): Promise<InboxListItem> {
        for (const node of Object.values(this.nodes)) {
            if (node.getNodeType() === "local") {
                return await node.getInbox(authorId);
            }
        }
        throw new Error("No local node found");
    }

    

}

export default NodeManager;