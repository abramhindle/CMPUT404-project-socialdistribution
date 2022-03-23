import { Author } from "./authors";

export interface Follower {
    id: string, 
    displayName: string, 
    profileImage: string
}

export interface FollowerPage {
    type: string, 
    items: Array<Author>
}
