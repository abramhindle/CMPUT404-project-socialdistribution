import { createContext } from "react"

export const UserContext = createContext({
  user: {
    username: null,
    author: {
      authorID: null,
      displayName: null,
      host: null,
      github: null,
      profileImage: null,
    }
  }, 
  setUser: () => {}
});

// user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
//     authorID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
//     displayName = models.CharField(max_length=32)
//     host = models.URLField()
//     github = models.URLField(null=True, blank=True)
//     profileImage = models.URLField(null=True, blank=True)