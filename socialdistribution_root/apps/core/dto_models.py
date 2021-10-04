# The purpose of this file is to contain "data transfer object" models.
# These are models designed to be used outside of a database context.
# These models do not have to be stored in a database, though they may 
# represent a model which is stored in the datbase. 
# 
# For example, a dto model might have additional fields that are used for 
# logic but do not have to be stored in the databse, or they may have fields
# that are deserialized versions of fields that are stored in a dabase.

from socialdistribution_root.apps.core.models import User

class UserDto(User):
    # The host this user is associated with. A null host
    # is treated as this servers default host
    host = None