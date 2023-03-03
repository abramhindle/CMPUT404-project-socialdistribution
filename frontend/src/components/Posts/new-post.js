import { useSelector } from "react-redux";
import { useState } from "react";
import { send_api, post_api } from "../../api/post_display_api";
import { get_followers_for_author } from "../../api/follower_api";

export default function NewPost() {
    //Get user info
    const user = useSelector((state) => state.user).id;

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [contentType, setContentType] = useState("text/plain");
    const [body, setBody] = useState("");
    const [visibility, setVisibility] = useState("");
    const [unlisted, setUnlisted] = useState(false);
    const [categories, setCategories] = useState([]);

    const [followers, setFollowers] = useState([]);
    const [posted, setPosted] = useState(null);

    const submit = async (e) => {
        console.log("Submitting ...");
        let data = {"title": title,
        "description": description,
        "contentType": contentType,
        "content": body,
        "visibility": visibility,
        "unlisted": unlisted,
        "categories": categories.split(",")};

        e.preventDefault();
        console.log(user, "is attempting to post", data);
        post_api(user, data, setPosted, setFollowers);
        send_api(followers, posted);
        //let followers = get_followers_for_author(user, setSucess);
        // console.log("Starting to send ...");
        // send_api(followers, sendLink);
    };

    const handleCheckbox = (e) => {
        //console.log(e.target.checked);
        let check = e.target.checked ? true : false;
        setUnlisted(check);
    }

    return (
        <div>
            <form justify-self="center">
                <label>Title</label><br/>
                <input
                    placeholder="Title.."
                    name="title"
                    type="text"
                    value={title}
                    required
                    onChange={(e) => setTitle(e.target.value)}
                /><br/>
                <label>Description</label><br/>
                <input
                    placeholder="Description.."
                    name="description"
                    type="text"
                    value={description}
                    required
                    onChange={(e) => setDescription(e.target.value)}
                /><br/>
                <label>Content Type: </label>
                    <input
                        name="type"
                        type="radio"
                        value="text/plain"
                        required
                        onChange={(e) => setContentType(e.target.value)}/>
                     Plain Text
                    <input
                        name="type"
                        type="radio"
                        value="text/markdown"
                        required
                        onChange={(e) => setContentType(e.target.value)}/>
                     Markdown
                     <br/>
                <label>Body</label><br/>
                    <input
                    placeholder="Content.."
                    name="content"
                    type="text"
                    value={body}
                    required
                    onChange={(e) => setBody(e.target.value)}
                /><br/>
                
                <label>Visibility</label><br/>
                Public
                    <input
                        name="visibility"
                        type="radio"
                        value="PUBLIC"
                        required
                        onChange={(e) => setVisibility(e.target.value)}
                    /><br/>
                Friends Only
                    <input
                            name="visibility"
                            type="radio"
                            value="FRIENDS"
                            required
                            onChange={(e) => setVisibility(e.target.value)}
                        /><br/>
                
                <label>Unlisted</label>
                <input
                    name="unlisted"
                    type="checkbox"
                    defaultChecked={false}
                    onChange={handleCheckbox}
                /><br/>
                <label>Categories</label><br/>
                <input
                    placeholder="Categories.."
                    name="categories"
                    type="text"
                    value={categories}
                    required
                    onChange={(e) => setCategories(e.target.value)}
                /><br/>
                <button type="submit" onClick={submit}>Submit</button>
            </form>
        </div>

    );
}