from django.db import models


class KnessetPerson(models.Model):
    source_id = models.IntegerField()
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    gender_id = models.IntegerField()
    gender_description = models.CharField(max_length=64)
    email = models.EmailField(blank=True, null=True)
    is_current = models.BooleanField()
    last_update = models.DateTimeField()


class KnessetPosition(models.Model):
    source_id = models.IntegerField()
    description = models.CharField(max_length=256)
    gender_id = models.IntegerField()
    gender_description = models.CharField(max_length=64)
    last_update = models.DateTimeField()


class KnessetPersonToPosition(models.Model):
    source_id = models.IntegerField()
    person_id = models.IntegerField()
    position_id = models.IntegerField()
    knesset_num = models.IntegerField()
    ministry_id = models.IntegerField()
    ministry_name = models.CharField(max_length=256)
    duty_description = models.CharField(max_length=256)
    faction_id = models.IntegerField()
    faction_name = models.CharField(max_length=64)
    gov_num = models.IntegerField()
    committee_id = models.IntegerField()
    committee_name = models.CharField(max_length=64)
    start_update = models.DateTimeField()
    finish_update = models.DateTimeField()
    is_current = models.BooleanField()
    last_update = models.DateTimeField()


class KnessetSiteCode(models.Model):
    source_id = models.IntegerField()
    kns_id = models.IntegerField()
    site_id = models.IntegerField()
