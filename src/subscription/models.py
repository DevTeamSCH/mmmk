from django.db import models

from account.models import Profile
from reservation.models import Period


class Subscription(models.Model):
    profile = models.ForeignKey(Profile, related_name="subscriptions", on_delete=models.CASCADE)
    period = models.ForeignKey(Period, related_name="subscriptions", on_delete=models.DO_NOTHING)
    confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('profile', 'period')

    def __str__(self):
        return "[{}] {}".format(self.confirmed, self.profile)
