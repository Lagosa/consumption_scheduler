from django.db import models
from .Dataset import Dataset


class DeviceDetail(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    ap_id = models.PositiveSmallIntegerField(null=False)
    dev_id = models.PositiveSmallIntegerField(null=False)
    name = models.CharField(max_length=20)
    consumption = models.FloatField(null=False)
    is_deferrable = models.PositiveSmallIntegerField(default=1, null=False)
    min_usage_hours = models.PositiveSmallIntegerField(default=0, null=False)
    dataset = models.ForeignKey(Dataset, null=True, on_delete=models.CASCADE)

    def __init__(self, id=0, ap_id=0, dev_id=0, name="", consumption=0.0, is_deferrable=0, min_usage_hours=0, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        if id != -1:
            self.id = id
        self.ap_id = ap_id
        self.dev_id = dev_id
        self.name = name
        self.consumption = consumption
        self.is_deferrable = is_deferrable
        self.min_usage_hours = min_usage_hours

    def __str__(self):
        return str(self.ap_id) + ":" + str(self.dev_id)