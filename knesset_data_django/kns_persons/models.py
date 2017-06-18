from django.db import models


class KnessetPerson(models.Model):
    source_id = models.IntegerField()
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    gender_id = models.IntegerField()
    gender_description = models.CharField(max_length=64)
    email = models.EmailField(blank=True, null=True)
    is_current = models.CharField(blank=True, null=True, max_length=64)
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
    knesset_num = models.IntegerField(blank=True, null=True)
    ministry_id = models.IntegerField(blank=True, null=True)
    ministry_name = models.CharField(max_length=256)
    duty_description = models.CharField(max_length=256)
    faction_id = models.IntegerField(blank=True, null=True)
    faction_name = models.CharField(max_length=64)
    gov_num = models.IntegerField(blank=True, null=True)
    committee_id = models.IntegerField(blank=True, null=True)
    committee_name = models.CharField(max_length=64)
    start_update = models.DateTimeField(blank=True, null=True)
    finish_update = models.DateTimeField(blank=True, null=True)
    is_current = models.CharField(blank=True, null=True, max_length=64)
    last_update = models.DateTimeField(blank=True, null=True)


class KnessetSiteCode(models.Model):
    source_id = models.IntegerField()
    kns_id = models.IntegerField()
    site_id = models.IntegerField()
