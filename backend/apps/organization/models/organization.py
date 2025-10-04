from django.db import models
from django.urls import reverse
from os import path
from uuid import uuid4
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


def image_path(instance, filename):
    """
    Logo için benzersiz dosya adı üretir: uuid + orijinal uzantı
    """
    dir_path = "organization/logos/"
    name = uuid4().hex
    extension = path.splitext(filename)[-1]  # örn: .png, .jpg
    return path.join(dir_path, name + extension)


class Organization(models.Model):
    class OrgType(models.IntegerChoices):
        SOLE_PROPRIETORSHIP = 0, _("Sole proprietorship")
        HOLDING = 1, _("Holding")
        SME = 2, _("Small and medium-sized enterprises")
        NGO = 3, _("Civil society organization")

    name = models.CharField(max_length=50)
    logo = models.ImageField(
        upload_to=image_path,
        null=True,
        blank=True
    )
    org_type = models.IntegerField(
        choices=OrgType.choices,
        default=OrgType.SOLE_PROPRIETORSHIP
    )
    nation = CountryField(blank_label="(select country)")
    founding_date = models.DateField()
    headcount = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    slug = AutoSlugField(populate_from="name", unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "organization"
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization-detail", kwargs={"slug": self.slug})
