# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component.hooks import getSite

from zope import interface

from zope.component import createObject, queryUtility

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from plone.app.discussion import interfaces
from plone.app.discussion.interfaces import IConversation
from plone.app.discussion.interfaces import IDiscussionSettings
from Products.Five.browser import BrowserView


def copy_comments(source_object, target_object):
    source_conversation = IConversation(source_object)
    target_conversation = IConversation(target_object)
    for thread_item in source_conversation.getThreads():
        comment = thread_item['comment']
        comment.unindexObject()
        target_conversation.addComment(comment)


def remove_comments(obj):
    conversation = IConversation(obj)
    # XXX: conversation.getComments does not work here. Needs to be inv.
    for thread_item in conversation.getThreads():
        try:
            del conversation[thread_item['comment'].id]
        except:
            import pdb; pdb.set_trace()


def push_to_tmpstorage(obj):
    #remove_comments(getSite())
    copy_comments(obj, getSite())


def pop_from_tmpstorage(obj):
    copy_comments(getSite(), obj)
    #remove_comments(getSite())


class PopFromTmpstorage(BrowserView):

    def __call__(self):
        pop_from_tmpstorage(self.context)
        return "Success"


class PushToTmpstorage(BrowserView):

    def __call__(self):
        push_to_tmpstorage(self.context)
        return "Success"
