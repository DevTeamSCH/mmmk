import hashlib

from django.db import models
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User

from reservation.models import Period


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    telephone = models.CharField(max_length=255, verbose_name="Telefon")
    dormitory = models.CharField(max_length=255, null=True, verbose_name="Kollégium")
    room = models.IntegerField(null=True, verbose_name="Szobaszám")
    faculty = models.CharField(max_length=255, null=True, verbose_name="Kar")
    first_reservation = models.BooleanField(default=True)

    @property
    def is_payed(self):
        period = Period.get_active_period()
        try:
            payment = self.payments.get(period=period)
        except:
            return False  # NOTE: mint az is_subscribedq-nel

        return payment is not None and payment.confirmed

    @property
    def is_subscribed(self):
        period = Period.get_active_period()
        try:
            payment = self.payments.get(period=period)
        except:
            return False  # NOTE: problema lehet ha tobszor van bent a fizetes

        return payment is not None

    @property
    def has_band(self):
        return self.user.bands.count() > 0

    @property
    def full_name(self):
        return "%s %s" % (self.user.last_name, self.user.first_name)

    def confirm_payment(self):
        period = Period.get_active_period()
        try:
            payment = self.payments.get(period=period)
            payment.confirmed = True
            payment.save()
        except:
            pass  # NOTE: problema lehet ha tobszor van bent a fizetes

    def subscribe_to_active_period(self):
        from payment.models import Payment

        period = Period.get_active_period()
        if period is None:
            return

        Payment.create(self, period)

    def is_band_id(self, id):
        return any(map(lambda band: band.id == id, self.user.bands.all()))

    def __str__(self):
        return "%s (%s)" % (self.full_name, self.user.username)


class EmailConfirm(models.Model):
    profile = models.OneToOneField(Profile, null=False, on_delete=models.CASCADE)
    activation_code = models.CharField(
        max_length=255,
        verbose_name="Activation hash",
        unique=True,
        null=False
    )
    new_email = models.EmailField(max_length=254, null=False)

    @classmethod
    def create(cls, profile, new_email, request):
        code = "%dkuttykurutty%s" % (profile.user.pk, new_email)
        code = hashlib.md5(code.encode('utf-8')).hexdigest()

        # check if this user already has an email confirmation request
        try:
            obj = EmailConfirm.objects.get(profile=profile)
            obj.new_email = new_email
            obj.activation_code = code
        except EmailConfirm.DoesNotExist:
            obj = cls(profile=profile,
                      new_email=new_email,
                      activation_code=code)

        url = reverse('activate', kwargs={'activation_code': code})
        url = request.build_absolute_uri(url)
        msg = ("Szia!\n"
               "\n"
               "Sikeresen regisztráltál az MMMK weboldalára!\n"
               "Fiókod aktiválásához a lenti linket tudod használni.\n"
               "Mielőtt elkezdenél próbálni,"
               " mindenképpen olvasd el a szabályzatot!\n"
               "Jó próbálást és sikeres félévet kívánunk!\n"
               "\n"
               "A Muzsika Mívelő Mérnökök Klubja\n"
               "\n"
               "Aktiválólink: %s" % url)

        send_mail(
            'mmmk e-mail megerősítés',
            msg,
            settings.SERVER_EMAIL,
            [new_email],
        )

        return obj
