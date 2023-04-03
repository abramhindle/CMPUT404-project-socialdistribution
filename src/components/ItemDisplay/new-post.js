import { useSelector } from "react-redux";
import { useState, useEffect } from "react";
import { send_api, post_api } from "../../api/post_display_api";
import { get_followers_for_author } from "../../api/follower_api";
import "./form.css";

export default function NewPost(props) {
    //Get user info
    const user = useSelector((state) => state.user).id;

    const [edit, setEdit] = useState(false);
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [contentType, setContentType] = useState("text/plain");
    const [body, setBody] = useState("");
    const [visibility, setVisibility] = useState("PUBLIC");
    const [unlisted, setUnlisted] = useState(false);
    const [categories, setCategories] = useState([]);

    const [followers, setFollowers] = useState([]);
    const [posted, setPosted] = useState(null);

    // Check if editing
    if (props.id) {
        setEdit(true);
        setTitle(props.title);
        setDescription(props.description);
        setContentType(props.contentType);
        setBody(props.body);
        setCategories(props.categories);
        setVisibility(props.visibility);
    }

    const populateFollowers = async () => {
        await get_followers_for_author(user, setFollowers);
    }

    const sendPost = async () => {
        await send_api(followers, posted);
    }

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
        await post_api(user, data, setPosted);
        
        //let followers = get_followers_for_author(user, setSucess);
        // console.log("Starting to send ...");
        // send_api(followers, sendLink);
    };

    const handleCheckbox = (e) => {
        //console.log(e.target.checked);
        let check = e.target.checked ? true : false;
        setUnlisted(check);
    }

    useEffect(() => {
        //only runs once
        populateFollowers();
      }, []);

    useEffect(() => {
        //runs when object posted
        sendPost();
      }, [posted]);

    return (
        <div className="form-container">
            <form className="form" encType="multipart/form-data" method="POST">
                <h1>New Text Post</h1>
                <div className="form-group">
                    <label for="contentType">Content Type: </label>
                    <select value={contentType} 
                            name="contentType" 
                            className="dropdown"
                            onChange={(e) => setContentType(e.target.value)}>
                        <option
                            value="text/plain">
                        Plain Text
                        </option>
                        <option
                            value="text/markdown">
                        Markdown
                        </option>
                     </select>
                </div>
                <label>Visibility: </label>
                <select value={visibility} 
                        name="visibility" 
                        className="dropdown"
                        onChange={(e) => setVisibility(e.target.value)}
                >
                    <option
                        value="PUBLIC"
                    >
                    Public
                    </option>
                    <option
                        value="FRIENDS"
                        >
                    Friends Only
                    </option>
                </select>
                <label>  Unlisted</label>
                <input
                    name="unlisted"
                    type="checkbox"
                    defaultChecked={false}
                    onChange={handleCheckbox}
                /><br/>
                <div className="form-group">
                    <input
                        className="form-control"
                        placeholder="Title.."
                        name="title"
                        type="text"
                        value={title}
                        required
                        onChange={(e) => setTitle(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <textarea 
                    className="form-control ta"
                    placeholder="Content.."
                    type="text"
                    rows="4"
                    value={body}
                    required
                    onChange={(e) => setBody(e.target.value)}
                    />
                </div>
                <div className="form-group">
                <textarea
                    className="form-control ta"
                    placeholder="Description.."
                    name="description"
                    type="text"
                    value={description}
                    required
                    onChange={(e) => setDescription(e.target.value)}
                />
                </div>
                <textarea
                    placeholder="Categories.."
                    className="form-control ta"
                    name="categories"
                    type="text"
                    value={categories}
                    required
                    onChange={(e) => setCategories(e.target.value)}
                /><br/>
                <button type="submit" className="btn" onClick={submit}>Submit</button>
            </form>
        </div>

    );
}
