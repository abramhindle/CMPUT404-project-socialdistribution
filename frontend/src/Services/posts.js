import axios from "axios";
import api from "../API/api";
import { post, get } from "./requests";

export function getInbox(authorID) {
    return get(authorID + "inbox/");
}

export function createPost(data, userID){
    return post(userID + "posts/", data);
}

