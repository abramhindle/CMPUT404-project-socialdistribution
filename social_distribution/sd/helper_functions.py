import uuid
from .models import *

def valid_method(request):
    if request.method in ("GET","POST"):
        return True
    return False

def authenticated(request):
    try:
        if(request.session['authenticated']):
            return True
    except KeyError as k:
        return False


def get_current_user(request):
    if authenticated(request):
        uid = request.session['auth-user']
        new_id = uuid.UUID(uid)
        author = Author.objects.get(uuid=new_id)
        return author
    else:
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
    if authenticated(request):
        print("CONSOLE: Authenticated user: "+get_current_user(request).username)
    else:
        print("CONSOLE: Browsing as non-authenticated user.")
        
