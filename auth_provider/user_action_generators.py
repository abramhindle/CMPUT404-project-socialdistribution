from typing import Callable, Optional

from .models import User

# Holds the name, and link of an action
UserAction = Optional[tuple[str, str]]
# Generates a UserAction when called with current_user and target_user
UserActionGenerator = Callable[[User, User], UserAction]

user_action_generators: list[UserActionGenerator] = []


def register(user_action_generator: UserActionGenerator):
    user_action_generators.append(user_action_generator)
