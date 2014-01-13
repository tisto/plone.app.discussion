# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone.app.discussion.interfaces import IConversation
from zope.annotation.interfaces import IAnnotations
from zope.component.hooks import getSite


ANNOTATION_KEY = 'plone.app.discussion:conversation'


def push_to_tmpstorage(obj):
    portal = getSite()
    # Copy the conversation from the object to portal (tmpstorage)
    IConversation(obj).__parent__ = portal
    annotations = IAnnotations(portal)
    annotations[ANNOTATION_KEY] = IConversation(obj)
    # Delete the conversation from the object.
    # XXX: I'm not sure if this is the behaviour we want, we might want to
    # remove those lines.
    source_ann = IAnnotations(obj)
    del source_ann[ANNOTATION_KEY]


def pop_from_tmpstorage(obj):
    # Copy the conversation from the portal (tmpstorage) to the object
    annotations = IAnnotations(obj)
    annotations[ANNOTATION_KEY] = IConversation(getSite())
    IConversation(obj).__parent__ = obj
    # Delete the conversation on the portal (tmpstorage)
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
