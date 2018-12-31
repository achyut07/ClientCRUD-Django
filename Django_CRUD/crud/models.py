from django.db import models


# Create your models here.

class ClientList(models.Model):
    client_name = models.CharField(max_length=150)
    client_company = models.CharField(max_length=150)
    company_location = models.CharField(max_length=50, blank=False)
    company_logo = models.ImageField(upload_to = 'media/img/', default = 'media/no-image.png',blank=True,null=True)
    contactno = models.CharField(max_length=20, blank=False)
    project_name = models.CharField(max_length=100, blank=False)
    tools = models.CharField(max_length=100, blank=False)
    offer_date = models.CharField(max_length=150)
    deadline =  models.CharField(max_length=150)

    def __str__(self):
        return self.client_name

