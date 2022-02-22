from django.test import TestCase, Client
from django.contrib.auth.models import User
from posts.models import Post, Category

POST_DATA = {
    'title': 'A post title about a post about web dev',
    'description': 'This post discusses stuff -- brief',
    'content_type': Post.ContentType.PLAIN,
    'content': 'Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan',
    'categories': 'web, tutorial',
    'visibility': Post.Visibility.PUBLIC,
}


class PostTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        User.objects.create_user(username='bob', password='password')

    def test_new_post_page(self):
        self.client.login(username='bob', password='password')
        res = self.client.get('/posts/new')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('posts/post_form.html')

    def test_new_post_require_login(self):
        res = self.client.get('/posts/new')
        self.assertEqual(res.status_code, 302)

    def test_new_post_require_csrf(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='bob', password='password')
        res = csrf_client.post('/posts/new', data=POST_DATA)
        self.assertEqual(res.status_code, 403)

    def test_new_post(self):
        self.client.login(username='bob', password='password')
        initial_post_count = len(Post.objects.all())
        self.client.post('/posts/new', data=POST_DATA)
        self.assertEqual(len(Post.objects.all()), initial_post_count + 1)

    def test_categories_not_duplicated(self):
        self.client.login(username='bob', password='password')
        Category.objects.create(category='web')
        initial_post_count = len(Post.objects.all())
        self.client.post('/posts/new', data=POST_DATA)
        self.assertEqual(len(Category.objects.all()), 2)
        self.assertEqual(len(Post.objects.all()), initial_post_count + 1)
