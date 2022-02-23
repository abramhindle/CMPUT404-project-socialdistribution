import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import CreatePost from './createPost/CreatePost';
import ProfileSection from './profile/profileSection';
import Paper from '@mui/material/Paper';
import FeedCard from './mainFeed/FeedCard';
import IconButton from '@mui/material/IconButton';
import LogoutIcon from '@mui/icons-material/Logout';
import axios from 'axios';
import Grid from '@mui/material/Grid';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../../redux/profileSlice';

const drawerWidth = 450;

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
        "commentsSrc":{
            "type":"comments",
            "page":1,
            "size":5,
            "post":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
            "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
            "comments":[
                {
                    "type":"comment",
                    "author":{
                        "type":"author",
                        "github": "http://github.com/gjohnson",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                    },
                    "comment":"Sick Olde English",
                    "contentType":"text/markdown",
                    "published":"2015-03-09T13:07:04+00:00",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                },
                {
                    "type":"comment",
                    "author":{
                        "type":"author",
                        "github": "http://github.com/gjohnson",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                    },
                    "comment":"Sick Olde English",
                    "contentType":"text/markdown",
                    "published":"2015-03-09T13:07:04+00:00",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                }
            ]
        },
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
        "commentsSrc":{
            "type":"comments",
            "page":1,
            "size":5,
            "post":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
            "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
            "comments":[
                {
                    "type":"comment",
                    "author":{
                        "type":"author",
                        "github": "http://github.com/gjohnson",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                    },
                    "comment":"Sick Olde English",
                    "contentType":"text/markdown",
                    "published":"2015-03-09T13:07:04+00:00",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                }
            ]
        },
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
        "commentsSrc":{
            "type":"comments",
            "page":1,
            "size":5,
            "post":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
            "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
            "comments":[
                {
                    "type":"comment",
                    "author":{
                        "type":"author",
                        "github": "http://github.com/gjohnson",
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                    },
                    "comment":"Sick Olde English",
                    "contentType":"text/markdown",
                    "published":"2015-03-09T13:07:04+00:00",
                    "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
                }
            ]
        },
        "published":"2016-03-09T13:07:04+00:00",
        "visibility":"PUBLIC",
        "unlisted":false,
        "ImgUrl": "https://images.immediate.co.uk/production/volatile/sites/3/2021/04/Call-of-Duty.jpg-d196774.png",
    },
]

export default function HomePage() {

    /* Redux Dispatcher */
    const dispatch = useDispatch();

    /* A State Hook For Storing The Window Width */
    const [windowWidth, setWindowWidth] = React.useState(window.innerWidth)

    /* We Use This To Listen To Changes In The Window Size */
    React.useEffect( () => { 
        const windowResizeCallback = () => { setWindowWidth(window.innerWidth) };
        window.addEventListener('resize', windowResizeCallback);
        return () => { window.removeEventListener('resize', windowResizeCallback) };
     });

    /* Hook For Navigating To The Home Page */
    const navigate = useNavigate();
    const goToLogin = () => navigate("/login/")

    /* Logout Functionality */
    const onLogout = () => {
      axios.post("/api/authors/logout/", {}, {headers: {"Authorization": "Token " + localStorage.getItem("token")}})
        .then( _ => {
            dispatch(logout());
            goToLogin();
         } )
        .catch( err => console.log(err) );
    }
    

  return (
    <Box sx={{ display: 'flex', paddingTop: "50px" }}>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar sx={{ flexWrap: 'wrap' }}>
            <Typography variant="h5" noWrap component="div"> Social Distribution </Typography>
            <IconButton
                onClick={onLogout}
                id="account-icon"
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                color="inherit"
                sx={{marginLeft: "auto"}} >
                <LogoutIcon sx={{ fontSize: "36px" }}/>
            </IconButton>
            </Toolbar>
            
        </AppBar>
        <Drawer
            sx={{ width: drawerWidth, flexShrink: 0, '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box', }, }}
            variant="permanent"
            anchor="left" >
        <Toolbar />
        <Divider />
        <ProfileSection /> 
        </Drawer>
            <Box component="main" sx={{ flexGrow: 1, p: 0, marginTop: "15px", width: (windowWidth - drawerWidth) + "px"}}>
                <CreatePost></CreatePost>
                <Paper sx={{p:0}}>
                {feedData.map((feedData) => (
                      <Grid item xs={12}>
                          <FeedCard feedData={feedData} fullWidth={true} />
                      </Grid>
                      ))}
                </Paper>
            </Box>
    </Box>
  );
}