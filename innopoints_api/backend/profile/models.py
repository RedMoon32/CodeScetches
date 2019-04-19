from django.db import models
from Tasks.models import Application


class UserProfile(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    @property
    def applications(self):
        return Application.objects.filter(volunteer=self)

    @property
    def xp(self):
        total = sum(application.xp_points for application in self.applications.filter(status=Application.FNS))
        return total

    @property
    def points(self):
        total = sum(application.inno_points for application in self.applications.filter(status=Application.FNS))
        return total

    @property
    def rank(self):
        return 0

    def __str__(self):
        return self.name + ' ' + self.surname
