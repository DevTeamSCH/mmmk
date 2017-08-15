from django.db import models

from account.models import Profile
from reservation.models import Period


class Payment(models.Model):
    profile = models.ForeignKey(Profile, related_name="payments", on_delete=models.CASCADE)
    period = models.ForeignKey(Period, related_name="payments", on_delete=models.DO_NOTHING)
    confirmed = models.BooleanField(default=False)

    @staticmethod
    def create(profile, period):
        try:
            Payment.objects.get_or_create(profile=profile, period=period)
        except:
            pass

    def __str__(self):
        return "[%s] %s" % (str(self.confirmed), str(self.profile))
