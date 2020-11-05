from django.db import models


class MessageManager(models.Manager):

    def createMessage(self, sender, reciever, subject, message):
        newMessage = self.create(
            sender=sender, reciever=reciever, subject=subject, message=message)
        return newMessage


class Message(models.Model):
    sender = models.EmailField(max_length=254)
    reciever = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    create_date = models.DateField(auto_now_add=True)
    read = models.BooleanField(default=False)  # message not read by default

    objects = MessageManager()

    def __str__(self):
        return self.message
