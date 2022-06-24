from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import F, Q


# Функция отправки сообщений о добавленных комментариях
def send_message_from_comment(sender, **kwargs):
    comment = kwargs.get('instance')
    sender_user = comment.user
    car_comments = comment.car.comments_set.all()
    # Выбираем всех пользователей, которые отправляли сообщения, кроме текущего отправителя - sender_user
    users_for_mail = User.objects.filter(comments__in=car_comments).exclude(pk=sender_user.pk).distinct()
    mailing_list = set()
    for user in users_for_mail:
        mailing_list.add(user.email)

    print(mailing_list)
    text_mail = f'К статье, которую вы прокомментировали, пользователь {sender_user.first_name} {sender_user.last_name}' \
                f' оставил следующий комментарий:\n\n{comment.content}\n\n' \
                f'Перейти к обсуждению: http://127.0.0.1:8000{comment.car.get_absolute_url()}'
    subject = f'Новый комментарий к записи о {comment.car}'

    send_mail(subject=subject, message=text_mail, from_email='infohakhak@yandex.ru',  recipient_list=tuple(mailing_list))
