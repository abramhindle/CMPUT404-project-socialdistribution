import "./posts.css"
import { useSelector } from "react-redux";
import { useState, useEffect } from "react";
import { send_api, post_api } from "../../api/post_display_api";
import { get_followers_for_author } from "../../api/follower_api";

export default function ImageUpload() {
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

    const populateFollowers = async () => {
        await get_followers_for_author(user, setFollowers);
    }

    const sendPost = async () => {
        await send_api(followers, posted);
    }

    const submit = async (e) => { 
        console.log("Submitting Image...");

        let data = {
            "title": title,
            "description": description,
            "contentType": contentType,
            "content": body,
            "visibility": visibility,
            "unlisted": unlisted,
            "categories": categories.split(",")
        };

        e.preventDefault();
        console.log(user, "is attempting to post", data);
        await post_api(user, data, setPosted);
    };

    const handleCheckbox = (e) => {
        //console.log(e.target.checked);
        let check = e.target.checked ? true : false;
        setUnlisted(check);
    }

    //vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    // by Melih Ekinci
    // from https://refine.dev/blog/how-to-base64-upload/
    const convertBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const fileReader = new FileReader();
            fileReader.readAsDataURL(file);

            fileReader.onload = () => {
                resolve(fileReader.result);
            };

            fileReader.onerror = (error) => {
                reject(error);
            };
        });
    };

    const uploadImage = async (event) => {
        const file = event.target.files[0];
        console.log(event.target.files[0]);
        setContentType(file.type);
        const base64 = await convertBase64(file);
        document.getElementById("avatar").src = base64;
        setBody(base64);
    };

    useEffect(() => {
        //only runs once
        populateFollowers();
      }, []);

    useEffect(() => {
        //runs when object posted
        sendPost();
      }, [posted]);

    return (
        <div>
            <form encType="multipart/form-data" method="POST">
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
                <textarea
                    placeholder="Description.."
                    name="description"
                    type="text"
                    value={description}
                    required
                    onChange={(e) => setDescription(e.target.value)}
                /><br/>
                {/*vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
                // Adapted from code by Melih Ekinci
                // from https://refine.dev/blog/how-to-base64-upload/ */}
                <input
                className="form-control form-control-lg"
                id="selectAvatar"
                type="file"
                onChange={uploadImage}
                accept="image/*"/>
                <div className="container">
                    <div className="row">
                        <div className="col">
                            <h6>Image Preview:</h6>
                            <img className="posted-image" id="avatar" />
                        </div>
                    </div>
                </div>
                {/**^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ */}
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
                <textarea
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