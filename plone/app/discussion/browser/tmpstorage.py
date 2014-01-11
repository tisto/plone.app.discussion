# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone.app.discussion.interfaces import IConversation
from zope.component.hooks import getSite


ANNOTATION_KEY = 'plone.app.discussion:conversation'


def push_to_tmpstorage(obj):
    from zope.annotation.interfaces import IAnnotations
    portal = getSite()
    IConversation(obj).__parent__ = portal
    annotations = IAnnotations(portal)
    annotations[ANNOTATION_KEY] = IConversation(obj)
    #
    source_ann = IAnnotations(obj)
    del source_ann[ANNOTATION_KEY]


def pop_from_tmpstorage(obj):
    from zope.annotation.interfaces import IAnnotations
    annotations = IAnnotations(obj)
    annotations[ANNOTATION_KEY] = IConversation(getSite())
    IConversation(obj).__parent__ = obj

    portal_ann = IAnnotations(getSite())
    del portal_ann[ANNOTATION_KEY]


class PopFromTmpstorage(BrowserView):

    def __call__(self):
        pop_from_tmpstorage(self.context)
        return "Success"


class PushToTmpstorage(BrowserView):

    def __call__(self):
        push_to_tmpstorage(self.context)
        return "Success"
