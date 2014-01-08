# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component.hooks import getSite

from zope import interface

from zope.component import createObject, queryUtility

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.discussion import interfaces
from plone.app.discussion.interfaces import IConversation
from plone.app.discussion.testing import (
    PLONE_APP_DISCUSSION_INTEGRATION_TESTING
)
from plone.app.discussion.interfaces import IDiscussionSettings


def copy_comments(source_object, target_object):
    source_conversation = IConversation(source_object)
    target_conversation = IConversation(target_object)
    for comment in source_conversation.getComments():
        target_conversation.addComment(comment)


def push_to_tmpstorage(obj):
    copy_comments(obj, getSite())


def remove_comments(obj):
    conversation = IConversation(obj)
    # XXX: conversation.getComments does not work here. Needs to be inv.
    for comment in conversation.getThreads():
        del conversation[comment['id']]


def pop_from_tmpstorage(obj):
    copy_comments(getSite(), obj)
    remove_comments(getSite())


class TestTmpstorage(unittest.TestCase):

    layer = PLONE_APP_DISCUSSION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        interface.alsoProvides(
            self.portal.REQUEST, interfaces.IDiscussionLayer)

        self.portal.invokeFactory('Document', 'doc1')
        self.portal.invokeFactory('Document', 'doc2')
        self.portal_discussion = getToolByName(
            self.portal,
            'portal_discussion',
            None,
        )
        # Allow discussion
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings)
        settings.globally_enabled = True

        conversation = IConversation(self.portal.doc1)
        comment = createObject('plone.Comment')
        comment.text = 'Comment text'
        conversation.addComment(comment)

    def test_copy_comments(self):
        copy_comments(self.portal.doc1, self.portal.doc2)

        conversation = IConversation(self.portal.doc2)
        self.assertEqual(len(conversation), 1)
        self.assertEqual(
            conversation.getComments().next().text,
            'Comment text'
        )

    def test_create_tmpstorage(self):
        push_to_tmpstorage(self.portal.doc1)

        conversation = IConversation(self.portal)
        self.assertEqual(len(conversation), 1)

        self.assertEqual(
            conversation.getComments().next().text,
            'Comment text'
        )

    def test_pop_from_tmpstorage(self):
        push_to_tmpstorage(self.portal.doc1)
        pop_from_tmpstorage(self.portal.doc2)

        conversation = IConversation(self.portal.doc2)
        self.assertEqual(len(conversation), 1)

        self.assertEqual(
            conversation.getComments().next().text,
            'Comment text'
        )

    def test_pop_from_tmpstorage_clears_portal(self):
        push_to_tmpstorage(self.portal.doc1)
        pop_from_tmpstorage(self.portal.doc2)

        conversation = IConversation(self.portal)
        self.assertEqual(len(conversation), 0)
