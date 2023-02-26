
| Allowed methods        | URI                                                                        | Paginated?              | Description |
| ---------------------- | -------------------------------------------------------------------------- | ----------------------- | ----------- |
| GET                    | ://service/authors/                                                        | ✅                      | Done        |
| GET                    | ://service/authors?page=10&size=5                                          | (example of pagination) | Done        |
| GET, POST              | ://service/authors/{AUTHOR_ID}/                                            |                         | Done        |
| GET                    | ://service/authors/{AUTHOR_ID}/followers                                   |                         |             |
| GET, PUT, DELETE       | ://service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}               |                         |             |
| GET, POST, DELETE, PUT | ://service/authors/{AUTHOR_ID}/posts/{POST_ID}                             |                         | Done        |
| GET, POST              | ://service/authors/{AUTHOR_ID}/posts/                                      | ✅                      | Done        |
| GET, POST              | ://service/authors/{AUTHOR_ID}/posts?page=10&size=5                        | (example of pagination) | Done        |
| GET                    | ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/image                       |                         |             |
| GET, POST              | ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments                    | ✅                      |             |
| POST                   | ://service/authors/{AUTHOR_ID}/inbox/                                      | ✅                      |             |
| GET                    | ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes                       |                         |             |
| GET                    | ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes |                         |             |
| GET                    | ://service/authors/{AUTHOR_ID}/liked                                       |                         |             |
| GET, POST, DELETE      | ://service/authors/{AUTHOR_ID}/inbox                                       |                         |             |
|                        |                                                                            |                         |             |

| Other URI's         | Description |
| ------------------- | ----------- |
| ://admin/           |             |
| ://api-auth/login/  |             |
| ://api-auth/logout/ |             |
| ://api-schema/      |             |
| ://docs/api/        |             |
|                     |             |
  