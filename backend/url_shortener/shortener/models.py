from django.db import models


# Create your models here.
class Url(models.Model):
    id = models.AutoField(primary_key=True)
    main_link = models.CharField(null=False, blank=False)
    short_link = models.CharField(null=False, blank=True)
    last_accessed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.main_link}"
