from userapp.models import Notifications


def makeNotificationFormat(created_by, notification_info, created_who):
    return f'<span class="fw-bold">{created_by}</span> {notification_info} <span class="fw-bold">{created_who}</span>'


def createNotifications(title, notification_info, created_by, created_who):
    created_by_generate = created_by.get_full_name() if created_by else "From Website"
    html_text_info = makeNotificationFormat(created_by_generate, notification_info, created_who)
    notification = Notifications.objects.create(title=title, info=html_text_info, created_by=created_by)
    notification.save()
    return notification


def getCurrentUser():
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            return request.user
            break
    else:
        request = None


def ProductNotification(Product_name):
    user = getCurrentUser()
    title = f"Product Created ({Product_name})"
    notification_info = " added a new product,"
    createNotifications(title=title, notification_info=notification_info,
                        created_by=user, created_who=Product_name)


def CustomerNotifications_OnCreate(name):
    user = getCurrentUser()
    title = f"Customer Created ({name})"
    notification_info = " Created a new customer "
    createNotifications(title=title, notification_info=notification_info,
                        created_by=user, created_who=name)


def CustomerNotifications_OnUpdate(name):
    user = getCurrentUser()
    title = f"Customer Updated ({name})"
    notification_info = " Updated information for"
    createNotifications(title=title, notification_info=notification_info,
                        created_by=user, created_who=name)


# def NotificationForCustomer(sender, instance, created, *args, **kwargs):
#     name = instance.name
#     mobile = instance.mobile
#     current_user = {}
#     import inspect
#     for frame_record in inspect.stack():
#         if frame_record[3] == 'get_response':
#             request = frame_record[0].f_locals['request']
#             current_user['user'] = request.user
#             break
#     else:
#         request = None

#     user = current_user['user']

#     if created:
#         title = f"Customer Created ({instance.name})"
#         notification_info = " Created a new customer "
#         createNotifications(title=title, notification_info=notification_info,
#                             created_by=user, created_who=instance.name)

#     else:
#         title = f"Customer Updated ({instance.name})"
#         notification_info = "Updated information for "
#         createNotifications(title=title, notification_info=notification_info,
#                             created_by=user, created_who=instance.name)


# post_save.connect(NotificationForCustomer, sender=Customer)
