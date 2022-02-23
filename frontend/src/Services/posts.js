import axios from "axios";
import api from "../API/api";
export function getInbox(authorID) {
    return new Promise( (resolve, reject) => {
        const feedData=[
            {
                "type":"post",
                "title":"A post title about a post about web dev",
                "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
                "origin":"http://whereitcamefrom.com/posts/zzzzz",
                "description":"This post discusses stuff -- brief",
                "contentType":"text/plain",
                "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
                "author":{
                    "type":"author",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Lara Croft",
                    "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "github": "http://github.com/laracroft",
                    "profileImage": "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png", 
                },
                "categories":["web","tutorial"],
                "count": 1023,
                "comments":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
                "published":"2016-03-09T13:07:04+00:00",
                "visibility":"PUBLIC",
                "unlisted":false
            },
            {
                "type":"post",
                "title":"New title",
                "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
                "origin":"http://whereitcamefrom.com/posts/zzzzz",
                "description":"This post discusses stuff -- brief",
                "contentType":"text/plain",
                "content":" and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
                "author":{
                    "type":"author",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Sara Croft",
                    "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "github": "http://github.com/laracroft",
                    "profileImage": "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png", 
                },
                "categories":["web","tutorial"],
                "count": 1023,
                "comments":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
                "published":"2015-03-09T13:07:04+00:00",
                "visibility":"PUBLIC",
                "unlisted":false
            },
            {
                "type":"post",
                "title":"A post title about a post about web dev",
                "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
                "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
                "origin":"http://whereitcamefrom.com/posts/zzzzz",
                "description":"This post discusses stuff -- brief",
                "contentType":"text/plain",
                "content":"",
                "author":{
                    "type":"author",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Lara Croft",
                    "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "github": "http://github.com/laracroft",
                    "profileImage": "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png", 
                },
                "categories":["web","tutorial"],
                "count": 1023,
                "comments":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
                "published":"2016-03-09T13:07:04+00:00",
                "visibility":"PUBLIC",
                "unlisted":false,
                "ImgUrl": "https://images.immediate.co.uk/production/volatile/sites/3/2021/04/Call-of-Duty.jpg-d196774.png",
            },
        ]
        resolve(feedData);
    } );
}


export function createPost(formData){
    axios.post(api.createPost, formData, {headers: {"Authorization": "Token " + localStorage.getItem("token")}})
}

