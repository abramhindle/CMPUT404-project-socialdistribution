from django.db import models
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from follow.signals import (
    request_create,
    request_reject,
    request_cancel,
    request_accept,
)


USER_MODEL = get_user_model()


class AlreadyExistsError(IntegrityError):
    pass


class FollowManager(models.Manager):
    def followings(self, user):
        qs = Follow.objects.filter(follower=user).all()
        followings = [_.followee for _ in qs]
        return followings

    def followers(self, user):
        qs = Follow.objects.filter(followee=user).all()
        followers = [_.follower for _ in qs]
        return followers

    def true_friend(self, user):
        followers = self.followers(user)
        followings = set(self.followings(user))
        friends = []
        for follower in followers:
            if follower in followings:
                friends.append(follower)
        return friends

    def request(self, user):
        qs = (Request.objects.select_related("from_user", "to_user").filter(to_user=user).all())
        requests = [_.from_user for _ in qs]
        return requests

    def sent_request(self, user):
        qs = (Request.objects.select_related("from_user", "to_user").filter(from_user=user).all())
        requests = list(qs)
        return requests

    def follow_request(self, from_user, to_user):
        '''create follow request'''
        if from_user == to_user:
            raise ValidationError("User cannot follow themselves.")
            return

        if self.check_follow(from_user, to_user):
            return

        if Request.objects.filter(
                from_user=from_user,
                to_user=to_user).exists():
            raise AlreadyExistsError("User has sent the follow request.")
            return

        request, created = Request.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created is False:
            raise AlreadyExistsError("User has sent the follow request.")
        else:
            request.title = request.__str__()
            request.save()

        request_create.send(sender=request)
        return request

    def unfollow(self, follower, followee):
        try:
            Follow.objects.get(follower=follower, followee=followee).delete()
            return True
        except Follow.DoesNotExist:
            return False

    def check_follow(self, follower: str, followee: str):
        try:
            Follow.objects.get(follower=follower, followee=followee)
            return True
        except Follow.DoesNotExist:
            return False

    def check_true_friend(self, follower, followee):
        if Follow.objects.filter(
            follower=follower,
            followee=followee).exists() and Follow.objects.filter(
                follower=followee,
                followee=follower).exists():
            return True
        else:
            return False


class Follow(models.Model):
    followee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="followee")
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="follower")
    created = models.DateTimeField(auto_now_add=True)
    objects = FollowManager()

    class Meta:
        unique_together = ("followee", "follower")

    def __str__(self):
        return f"{self.followee} is followed by {self.follower}"

    def save(self, *args, **kwargs):
        if self.followee == self.follower:
            raise ValidationError("User cannot follow themselves.")
        try:
            follow_reverse = Follow.objects.get(follower=self.followee, followee=self.follower)
        except Follow.DoesNotExist:
            pass
        super().save(*args, **kwargs)


class Request(models.Model):
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="to_user")
    title = models.CharField(max_length=512, default="")
    created = models.DateTimeField(auto_now_add=True)
    objects = FollowManager()

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user}'s request to follow {self.to_user}"

    def save(self, *args, **kwargs):
        if self.from_user == self.to_user:
            raise ValidationError("User cannot request to follow themselves.")
        try:
            follow_check = Follow.objects.get(follower=self.from_user, followee=self.to_user)
            raise AlreadyExistsError("User have already followed.")
        except Follow.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def accept(self):
        relation, created = Follow.objects.get_or_create(follower=self.from_user, followee=self.to_user)

        if created is False:
            raise AlreadyExistsError(f"{self.from_user} has already followed {self.to_user}")

        request_accept.send(sender=self, from_user=self.from_user, to_user=self.to_user)

        try:
            relation_reverse = Follow.objects.get(follower=self.to_user, followee=self.from_user)
            relation_reverse.save()
            relation.save()
        except Follow.DoesNotExist:
            pass
        self.delete()
        return True

    def reject(self):
        self.delete()
        # request_reject.send(sender=self)
        return True

    def cancel(self):
        request_cancel.send(sender=self)
        self.delete()
        return True
