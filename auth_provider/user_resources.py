user_resources: list[tuple[str, str]] = []


def register(resource_name: str, link_to_user_resource: str):
    user_resources.append((resource_name, link_to_user_resource))
