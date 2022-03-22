export interface Author {
    type: string, 
    id: string, 
    url: string, 
    host: string, 
    displayName: string, 
    github: string, 
    profileImage: string
}

export interface AuthorPage {
    type: string, 
    items: Array<Author>
}

