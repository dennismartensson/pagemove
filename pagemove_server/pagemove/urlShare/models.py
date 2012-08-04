import binascii

from django.db import models
from django.conf import settings

from APNSWrapper import APNSNotificationWrapper, APNSNotification


class User(models.Model):
    twitter_id = models.TextField(unique=True)

    def __unicode__(self):
        return self.twitter_id

    def broad_cast(self, alert):
        for device in self.device_set.all():
            device.send_notification(alert)


class Device(models.Model):
    user = models.ForeignKey(User)
    device_id = models.TextField(unique=True)

    def send_notification(self, alert):
         #deviceToken = 'e328c75878c5b9566080482cb7bc56015b59faf69c8363325326314cadcdda9b'
        deviceTokenUnHex = binascii.unhexlify(self.device_id)
        wrapper = APNSNotificationWrapper(settings.PROJECT_ROOT + '/NotificationCombined.pem', False)
        message = APNSNotification()
        message.token(deviceTokenUnHex)
        message.alert(alert.encode("utf-8"))
        message.badge(0)
        message.sound('default')
        wrapper.append(message)
        wrapper.notify()


class URL(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField()
    date_created = models.DateTimeField(auto_now=True)

    def broad_cast(self):
        self.user.broad_cast(self.url)
