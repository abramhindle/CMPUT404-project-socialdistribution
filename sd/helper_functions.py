import uuid
from .models import *
from django.db.models import Q

def valid_method(request):
    if request.method in ("GET","POST"):
        return True
    return False

def authenticated(request):
    try:
        return request.session['authenticated'] == True
    except KeyError as k:
        return False

def get_current_user(request):
    try:
        uid = request.session['auth-user']
        new_id = uuid.UUID(uid)
        return Author.objects.get(uuid=new_id)
    except:
        return None

def paginated_result(objects, request, keyword, **result):
    page_num = int(request.GET.get('page', 0))
    size = int(request.GET.get('size', 10))
    first_result = size*page_num
    count = objects.count()
    if count <= first_result:
        first_result = 0
        page_num = 0
    last_result = first_result + size

    result["count"] = count
    result["size"] = size
    result["previous"] = page_num - 1 if page_num >= 1 else None
    result["next"] = page_num + 1 if objects.count() >= last_result else None
    result[keyword] = list(objects[first_result:last_result])
    return result

def print_state(request):
    user = get_current_user(request)
    if user:
        print("CONSOLE: Authenticated user: "+user.username)
    else:
        print("CONSOLE: Browsing as non-authenticated user.")

def get_relationship(user, target):
    f1 = Friend.objects.filter(Q(author=user.uuid) & Q(friend=target.uuid))
    f2 = Friend.objects.filter(Q(author=target.uuid) & Q(friend=user.uuid))
    fr1 = FriendRequest.objects.filter(Q(to_author=user.uuid) & Q(from_author=target.uuid))
    fr2 = FriendRequest.objects.filter(Q(to_author=target.uuid) & Q(from_author=user.uuid))
    friends = f1|f2
    if friends:
        # if the two users are friends, delete any friend requests between the two of them, if any. working with the logic that an existing Friend objects trumps any friendrequest data
        if(fr1|fr2):
            (fr1|fr2).delete()
        return 1, None #friends
    if fr1:
        return 2, fr1 #target follows user
    if fr2:
        return 3, fr2 #user follows target
    return 4,None #no relationship
