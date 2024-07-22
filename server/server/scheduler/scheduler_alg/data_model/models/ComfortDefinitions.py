from django.db import models
from .Dataset import Dataset


class ComfortDefinition(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    ap_id = models.PositiveSmallIntegerField(null=False)
    dev_id = models.PositiveSmallIntegerField(null=False)
    h0 = models.PositiveSmallIntegerField(default=0, null=False)
    h1 = models.PositiveSmallIntegerField(default=0, null=False)
    h2 = models.PositiveSmallIntegerField(default=0, null=False)
    h3 = models.PositiveSmallIntegerField(default=0, null=False)
    h4 = models.PositiveSmallIntegerField(default=0, null=False)
    h5 = models.PositiveSmallIntegerField(default=0, null=False)
    h6 = models.PositiveSmallIntegerField(default=0, null=False)
    h7 = models.PositiveSmallIntegerField(default=0, null=False)
    h8 = models.PositiveSmallIntegerField(default=0, null=False)
    h9 = models.PositiveSmallIntegerField(default=0, null=False)
    h10 = models.PositiveSmallIntegerField(default=0, null=False)
    h11 = models.PositiveSmallIntegerField(default=0, null=False)
    h12 = models.PositiveSmallIntegerField(default=0, null=False)
    h13 = models.PositiveSmallIntegerField(default=0, null=False)
    h14 = models.PositiveSmallIntegerField(default=0, null=False)
    h15 = models.PositiveSmallIntegerField(default=0, null=False)
    h16 = models.PositiveSmallIntegerField(default=0, null=False)
    h17 = models.PositiveSmallIntegerField(default=0, null=False)
    h18 = models.PositiveSmallIntegerField(default=0, null=False)
    h19 = models.PositiveSmallIntegerField(default=0, null=False)
    h20 = models.PositiveSmallIntegerField(default=0, null=False)
    h21 = models.PositiveSmallIntegerField(default=0, null=False)
    h22 = models.PositiveSmallIntegerField(default=0, null=False)
    h23 = models.PositiveSmallIntegerField(default=0, null=False)
    dataset = models.ForeignKey(Dataset, null=True, on_delete=models.CASCADE)

    def __init__(self, id=0, ap_id=0, dev_id=0, h0=2, h1=2, h2=2, h3=2, h4=2, h5=2, h6=2, h7=2, h8=2, h9=2, h10=2,
                 h11=2, h12=2, h13=2, h14=2, h15=2, h16=2, h17=2, h18=2, h19=2, h20=2, h21=2, h22=2, h23=2, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        if id != -1:
            self.id = id
        self.ap_id = ap_id
        self.dev_id = dev_id
        self.h0 = h0
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.h4 = h4
        self.h5 = h5
        self.h6 = h6
        self.h7 = h7
        self.h8 = h8
        self.h9 = h9
        self.h10 = h10
        self.h11 = h11
        self.h12 = h12
        self.h13 = h13
        self.h14 = h14
        self.h15 = h15
        self.h16 = h16
        self.h17 = h17
        self.h18 = h18
        self.h19 = h19
        self.h20 = h20
        self.h21 = h21
        self.h22 = h22
        self.h23 = h23

    def __str__(self):
        return str(self.ap_id) + ":" + str(self.dev_id)