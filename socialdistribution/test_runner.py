from django.conf import settings
from django.test.runner import DiscoverRunner


class FastTestRunner(DiscoverRunner):
    # by meshy on StackOverflow at https://stackoverflow.com/a/17066553
    def setup_test_environment(self):
        super(FastTestRunner, self).setup_test_environment()

        # Don't write files
        settings.DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'

        # Bonus: Use a faster password hasher for creating users fast
        settings.PASSWORD_HASHERS = (
            'django.contrib.auth.hashers.MD5PasswordHasher',
        )
