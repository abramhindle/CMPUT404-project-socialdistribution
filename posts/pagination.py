from social_distance.pagination import PageSizePagination

class CommentsPagination(PageSizePagination):
    def __init__(self):
        super().__init__()
        self.key = 'comments'
        self.type = 'comments'

class PostsPagination(PageSizePagination):
    def __init__(self):
        super().__init__()
        self.type = 'posts'