from django.shortcuts import render
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from .models import Message
import traceback


def writeMessage(request):
    """
    request -  a post request - with the information:
                                email of sender
                                email of reciever
                                subject
                                message
    return - a JSON of the messages that has been added with status- 200 if it was successful
    """
    if(request.method == 'GET'):
        return JsonResponse({'error_message': "use the POST method"}, status=500)
    try:
        sender = request.POST['sender']
        reciever = request.POST['reciever']
        subject = request.POST['subject']
        message = request.POST['message']

        newMessage = Message.objects.createMessage(
            sender, reciever, subject, message)

        newMessage.save()

    except(KeyError):
        traceback.print_exc()
        errorMessage = """didn't write the message correctly -
        {sender: email of sender,
        reciever: email of reciever,
        subject: subject of the message,
        message: the message that you want to send}"""
        return JsonResponse({'error_message': errorMessage}, status=500)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error_message': "could not create or save the message to the database"}, status=500)

    else:
        data = {'message_id': newMessage.id,
                'sender': newMessage.sender,
                'reciever': newMessage.reciever,
                'subject': newMessage.subject,
                'message': newMessage.message,
                'read': newMessage.read,
                'create_date': newMessage.create_date}

        return JsonResponse({'data': data}, status=200)


def getAllMessages(request):
    """
    request - a GET request - with the user email (user is a sender or reciever)
    return - on error - a JSON of an error message
             on success - a JSON of all the messages of a specific user
    """
    if(request.method == 'POST'):
        return JsonResponse({'error_message': "use the GET method"}, status=500)
    try:
        user = request.GET['email']
        messages = list(Message.objects.filter(
            Q(sender=user) | Q(reciever=user)).values())

    except(KeyError):
        errorMessage = "key is not written correctly - use email as key"
        return JsonResponse({'error_message': errorMessage}, status=500)
    else:
        return JsonResponse({'messages': messages}, status=200)


def getUnreadMessages(request):
    """
    request - a GET request - with the user email (user is a sender or reciever)
    return - on error - a JSON of an error message
             on success - a JSON of all the unread messages of a specific user
    """
    if(request.method == 'POST'):
        return JsonResponse({'error_message': "use the GET method"}, status=500)
    try:
        user = request.GET['email']
        unreadMessages = list(Message.objects.filter(
            Q(sender=user) | Q(reciever=user), read=False).values())
    except(KeyError):
        errorMessage = "key is not written correctly- use email as key"
        return JsonResponse({'error_message': errorMessage}, status=500)
    else:
        return JsonResponse({'unreadMessages': unreadMessages}, status=200)


def readMessage(request):
    """
    request - a POST request - id of a message
    return - on error - a JSON of an error message
             on success - a JSON of the message
    the function will get the message and update the read field to True
    """
    if(request.method == 'GET'):
        return JsonResponse({'error_message': "use the POST method"}, status=500)
    try:
        messageId = request.POST['message_id']
        message_qs = Message.objects.filter(pk=messageId)
        if(message_qs):
            serializer = serializers.serialize('json', message_qs)
            message_qs[0].read = True
            message_qs[0].save()
        else:
            return JsonResponse({'error_message': "There is no message with that id - "+messageId}, status=500)
    except(KeyError):
        return JsonResponse({'error_message': "key is not written correctly"}, status=500)
    except Exception as e:
        return JsonResponse({'error_message': "could not save the message to the database"}, status=500)
    else:
        return JsonResponse({'message': serializer}, status=200)


def deleteMessage(request):
    """
    request - a POST request - id of a message
    return - on error - a JSON of an error message
             on success - a JSON of a successful delete
    The function will get a message id and will delete it from the database
    """
    if (request.method == 'GET'):
        return JsonResponse({'error_message': "use the POST method"}, status=500)
    else:
        try:
            messageId = request.POST['message_id']
            message_qs = Message.objects.filter(pk=messageId)
            if(message_qs):
                serializer = serializers.serialize('json', message_qs)
                message_qs.delete()
            else:
                return JsonResponse({'error_message': "there is no message with that id"}, status=500)

        except(KeyError):
            return JsonResponse({'error_message': "keys are not written correctly"}, status=500)
        except Exception as e:
            return JsonResponse({'error_message': "could not delete the message from the database"}, status=500)

        else:
            return JsonResponse({'success_message': "The message has been deleted successfully"}, status=200)
