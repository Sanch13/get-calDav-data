import datetime
from django.db import models


class FirstRoom(models.Model):
    created_at = models.DateField(verbose_name="Дата создания",
                                  default=datetime.date.today)
    hash_value = models.CharField(verbose_name="Хеш данных",
                                  max_length=64,
                                  unique=True)
    data_json = models.JSONField(verbose_name="Данные")

    def __str__(self):
        return f"ID:{self.pk}  - Date:{self.created_at}  hash:{self.hash_value}"


class ThirdRoom(models.Model):
    created_at = models.DateField(verbose_name="Дата создания",
                                  default=datetime.date.today)
    hash_value = models.CharField(verbose_name="Хеш данных",
                                  max_length=64,
                                  unique=True)
    data_json = models.JSONField(verbose_name="Данные")

    def __str__(self):
        return f"ID:{self.pk}  - Date:{self.created_at}  hash:{self.hash_value}"
