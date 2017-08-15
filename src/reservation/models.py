from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta, datetime, time
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from band.models import Band

# from mmmk import util

import logging
logger = logging.getLogger(__name__)


class Period(models.Model):
    is_active = models.BooleanField(default=False)  # NOTE: ne allitsd kezzel
    start = models.DateField()
    end = models.DateField()

    @staticmethod
    def get_active_period():

        result = Period.objects.filter(is_active=True)
        if len(result) == 0:
            return None
        elif len(result) > 1:
            pass  # TODO: Nagyon nagy baj van
        else:
            return result[0]

    def activate(self):
        active_period = Period.get_active_period()
        if active_period is not None:
            active_period.deactivate()

        self.is_active = True
        self.save()

    def deactivate(self):
        # TODO: Ezt meg lehet oldani mashogy is.
        from account.models import Profile
        self.is_active = False
        self.save()
        # Mindenkinek meg adjuk az elso foglalas lehetoseget
        Profile.objects.all().update(first_reservation=True)

    @property
    def actual_week_num(self):
        return (date.today() - self.start).days/7

    def get_week(self, num):
        result = self.weeks.filter(number=num)

        if len(result) == 0:
            return None
        elif len(result) > 1:
            pass  # TODO: nagy baj van
        else:
            return result[0]

    @property
    def actual_week(self):
        return self.get_week(self.actual_week_num)

    def __str__(self):
        return self.start.strftime("%Y.%m.%d")


class Week(models.Model):
    is_active = models.BooleanField(default=False)
    number = models.IntegerField()
    period = models.ForeignKey(Period, related_name="weeks", on_delete=models.CASCADE)

    @property
    def start(self):
        delta = timedelta(weeks=self.number)
        return self.period.start + delta

    @property
    def end(self):
        delta = timedelta(weeks=self.number, days=6)
        return self.period.start + delta

    def __str__(self):
        return "%s-%s" % (self.start.strftime("%Y.%m.%d"),
                          self.end.strftime("%Y.%m.%d"))


class Reservation(models.Model):
    # TODO: Atgondolni ezt a modellt meg egyszer
    TYPES = ('user', 'band', 'unique')

    is_conditional = models.BooleanField(default=False)
    allower = models.ForeignKey(User, null=True, related_name="assigned_reservations", on_delete=models.SET_NULL)
    day_num = models.IntegerField(validators=[MaxValueValidator(6), MinValueValidator(0)])
    hour_num = models.IntegerField(validators=[MaxValueValidator(23), MinValueValidator(0)])
    # a user es a band egymast kizaroak ha egyik sincs akkor egyedi foglalas
    user = models.ForeignKey(User, null=True, related_name="reservations", on_delete=models.CASCADE)
    band = models.ForeignKey(Band, null=True, related_name="reservations", on_delete=models.CASCADE)
    unique_message = models.CharField(max_length=255, null=True, blank=False)
    week = models.ForeignKey(Week, related_name="reservations", on_delete=models.CASCADE)

    # @property
    # def day(self):
    #    return util.WEEKDAYS[self.day_num]

    @property
    def hour(self):  # ebbe a formaban mar lehet hogy inkabb a view-ba tartozna
        return "%d:00" % self.hour_num

    @property
    def reserver_name(self):
        if self.user is not None:
            return self.user.profile.full_name
        if self.band is not None:
            return self.band.name
        if self.unique_message is not None:
            return self.unique_message

        # TODO: ha ide eljut akkor nagy baj van

    @property
    def type(self):
        if self.user is not None:
            return "user"
        if self.band is not None:
            return "band"
        if self.unique_message is not None:
            return "unique"

        # TODO: ha ide eljut akkor nagy baj van

    @property
    def reserver_id(self):
        if self.user is not None:
            return self.user.id
        if self.band is not None:
            return self.band.id

        # TODO: ha ide eljut akkor nagy baj van

    def delete_with_user(self, user):
        # TODO: visszamaneoleg ne lehessen torolni
        user_id = self.user.id if self.user is not None else None

        res_time = (datetime.combine(self.week.start, time()) +
                    timedelta(days=self.day_num, hours=self.hour_num))

        if res_time < datetime.now():
            raise ValidationError("Múltbeli foglalást nem törölhetsz.")

        if (user.id == user_id or user.has_perm("mmmk.foglalas_barki_neveben")
           or self.is_conditional or self.band.is_member(user)):

            self.delete()

    def to_dict(self):  # NOTE: ha valakinek jut eszebe jobb nev, akkor irja at
        return {"reserver_name": self.reserver_name,
                "reserver_id": self.reserver_id,
                "reservation_type": self.type,
                "allower_name": (self.allower.profile.full_name
                                 if self.allower is not None
                                 else "nincs beengedő"),
                "allower_id": (self.allower.id
                               if self.allower is not None else ""),
                "is_conditional": self.is_conditional,
                "day": self.day if self.day_num is not None else None,
                "id": self.id,
                }

    def clean(self):

        cond1 = self.user is not None and self.unique_message is not None
        cond2 = self.user is not None
        cond3 = self.band is not None

        i = len(list(filter(None, (cond1, cond2, cond3))))

        if i != 1:
            raise ValidationError("Rossz tulajdonos konfiguraáció.")

        if self.week is None:
            raise ValidationError("A foglalás nem tartozik egyik héthez sem.")

        if not self.week.is_active:
            raise ValidationError("Csak aktív hétre foglalhatsz.")

        res_time = (datetime.combine(self.week.start, time()) +
                    timedelta(days=self.day_num, hours=self.hour_num))

        if res_time < datetime.now():
            raise ValidationError("Múltbeli időpontra nem foglalhatsz.")

        start_time = (datetime.combine(self.week.start, time()) +
                      timedelta(hours=8))
        end_time = (datetime.combine(self.week.end, time()) +
                    timedelta(hours=24))
        if res_time < start_time or res_time > end_time:
            raise ValidationError("Az adott időpontra nem foglalhatsz.")

        if any(map(lambda r: (r.day_num == self.day_num and
                              r.hour_num == self.hour_num),
                   self.week.reservations.exclude(id=self.id))):

            raise ValidationError("Ez az időpont mar foglalt.")

    @staticmethod
    def get_default_dict():
        res = Reservation(unique_message="Szabad").to_dict()
        period = Period.get_active_period()
        if period is None:
            return res
        week = period.actual_week
        if week is not None:
            res["week"] = week.number

        return res

    def __str__(self):
        return str(datetime.combine(self.week.start, time()) +
                   timedelta(days=self.day_num, hours=self.hour_num))


class RoomMessage(models.Model):
    week = models.ForeignKey(Week, related_name="messages", on_delete=models.CASCADE)
    time = models.DateTimeField()


class StaticReservation(models.Model):

    day = models.IntegerField()
    time = models.TimeField()
    # a user es a band egymast kizaroak, es valamelyiknek lenni kell
    user = models.ForeignKey(User, null=True, related_name="static_reservations", on_delete=models.CASCADE)
    band = models.ForeignKey(Band, null=True, related_name="static_reservations", on_delete=models.CASCADE)


class GlobalPermissionManager(models.Manager):
    def get_query_set(self):
        return super(GlobalPermissionManager, self).get_query_set().filter(
            content_type__name='global_permission')


class DummyModelForGlobalPermission(models.Model):
    pass


class GlobalPermission(Permission):
    """A global permission, not attached to a model"""

    objects = GlobalPermissionManager()

    class Meta:
        proxy = True
        verbose_name = "global_permission"

    def save(self, *args, **kwargs):
        self.content_type = ContentType.objects.get_for_model(
            DummyModelForGlobalPermission)
        super(GlobalPermission, self).save(*args)
