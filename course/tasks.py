# Create your tasks here
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from school.function import getnowlessontime
from course.models import Lesson, Coursehomework, Studentcourse
from course.constant import LESSON_STATUS_NOW, LESSON_STATUS_END, COURSE_HOMEWORK_TYPE_NOSUBMIT
from wechat.client import wechat_client
from django.conf import settings
from django.db.models import Q, F
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger(__name__)


@shared_task(name='auto_stop_lesson')
def auto_stop_lesson(before):
    nowlessontime = getnowlessontime()
    week = nowlessontime['week']
    day = nowlessontime['day']
    time = nowlessontime['time']
    term = nowlessontime['term']
    qs = {
        'today': Q(week=week, day=day, time__lt=time + 1 - F('length')),
        # 上课时间 + 课程长度 - 1 < 现在时间   =>  上课时间 < 现在时间 + 1 - 课程长度
        'week': Q(week=week, day__lt=day),
        'term': Q(week__lt=week)
    }
    qbefore = {
        'today': qs['today'],  # stop lessons in today
        'week': qs['today'] | qs['week'],  # stop lessons in this week
        'all': qs['today'] | qs['term'] | qs['week']  # stop lesson in this term
    }
    unstoplessons = Lesson.objects.filter(term=term).filter(qbefore[before])
    count = unstoplessons.filter(status=LESSON_STATUS_NOW).update(status=LESSON_STATUS_END)
    if count:
        logger.info('autostop %d lessons this %s' % (count, before))
    return count


@shared_task(name='send_homework_notification')
def send_homework_notification(homeworkid):
    homework = Coursehomework.objects.get(pk=homeworkid)
    course = homework.course
    studentcourses = Studentcourse.objects.select_related("student__user").filter(course=course).all()
    userid = []
    for sc in studentcourses:
        if sc.student.user and sc.student.user.openid:
            userid.append(sc.student.user.openid)
    if homework.type == COURSE_HOMEWORK_TYPE_NOSUBMIT:
        description = "%s\n点击查看详情" % (homework.title)
    else:
        description = "%s\n点击提交或查看详情，电脑提交请访问%s" % (homework.title, settings.DOMAIN)
    article = {
        "title": "[%s]新作业!" % (course.title),
        "description": description,
        "url": "%s%s" % (settings.DOMAIN, reverse('course:homework', args=[course.id]) + '?homeworkid=%d' % homeworkid),
        "image": "%s/static/img/homework.png"
    }
    wechat_client.message.send_articles(agent_id=settings.AGENTID, user_ids=userid, articles=[article])
