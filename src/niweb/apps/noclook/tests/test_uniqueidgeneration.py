# -*- coding: utf-8 -*-
"""
Created on 2014-06-26 1:40 PM

@author: lundberg
"""

from django.test import TestCase
from django.db import connection, transaction, IntegrityError
from django.contrib.auth.models import User
from apps.noclook.models import UniqueIdGenerator, UniqueId
from apps.noclook import helpers as h


class UniqueIdGeneration(TestCase):

    #@transaction.autocommit
    def setUp(self):
        # Set up a user
        self.username = 'TestUser'
        self.password = 'password'
        self.user, created = User.objects.get_or_create(username=self.username,
            password=self.password)
        # Set up an ID generator
        self.id_generator, created = UniqueIdGenerator.objects.get_or_create(
            name='Test ID Generator',
            base_id_length=6,
            zfill=True,
            prefix='TEST-',
            creator=self.user
        )
        # Set up an ID collection
        #try:
        # sqlite3
#        connection.cursor().execute("""
#            CREATE TABLE "tests_testuniqueid" (
#                "id" integer NOT NULL PRIMARY KEY,
#                "unique_id" varchar(256) NOT NULL UNIQUE,
#                "reserved" bool NOT NULL,
#                "reserve_message" varchar(512),
#                "reserver_id" integer REFERENCES "auth_user" ("id"),
#                "created" datetime NOT NULL
#            );
#            """)
        # postgresql
        connection.cursor().execute("""
                CREATE TABLE "tests_testuniqueid" (
                    "id" serial NOT NULL PRIMARY KEY,
                    "unique_id" varchar(256) NOT NULL UNIQUE,
                    "reserved" boolean NOT NULL,
                    "reserve_message" varchar(512),
                    "reserver_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
                    "created" timestamp with time zone NOT NULL
                );
                """)
        #except DatabaseError as e:
            # Table already created
            #print e
            #pass

        class TestUniqueId(UniqueId):
            def __unicode__(self):
                return unicode('Test: %s' % self.unique_id)
        self.id_collection = TestUniqueId

    def test_id_generation(self):
        new_id = self.id_generator.get_id()
        self.assertEqual(new_id, self.id_generator.last_id)
        unique_id = self.id_collection.objects.create(unique_id=new_id)
        self.assertEqual(unique_id.unique_id, new_id)

    def test_helper_functions_basics(self):
        new_id = self.id_generator.get_id()
        return_value = h.register_unique_id(self.id_collection, new_id)
        self.assertEqual(return_value, True)
        next_id = self.id_generator.next_id
        new_id = h.get_collection_unique_id(self.id_generator, self.id_collection)
        self.assertEqual(new_id, next_id)

    def test_reserve_range(self):
        h.bulk_reserve_id_range(1, 100, self.id_generator, self.id_collection, 'Reserve message', self.user)
        num_objects = self.id_collection.objects.count()
        self.assertEqual(num_objects, 100)
        new_id = h.get_collection_unique_id(self.id_generator, self.id_collection)
        self.assertEqual(new_id, 'TEST-000101')

    def test_reserve_sequence(self):
        h.reserve_id_sequence(100, self.id_generator, self.id_collection, 'Reserve message', self.user)
        num_objects = self.id_collection.objects.count()
        self.assertEqual(num_objects, 100)
        new_id = h.get_collection_unique_id(self.id_generator, self.id_collection)
        self.assertEqual(new_id, 'TEST-000101')


    def test_get_unique_id_jump(self):
        h.bulk_reserve_id_range(1, 99, self.id_generator, self.id_collection, 'Reserve message', self.user)
        self.assertEqual(self.id_generator.next_id, 'TEST-000001')
        new_id = h.get_collection_unique_id(self.id_generator, self.id_collection)
        self.assertEqual(new_id, 'TEST-000100')
        h.bulk_reserve_id_range(101, 150, self.id_generator, self.id_collection, 'Reserve message', self.user)
        seq = h.reserve_id_sequence(100, self.id_generator, self.id_collection, 'Reserve message', self.user)
        self.assertEqual(len(seq), 100)
        new_id = h.get_collection_unique_id(self.id_generator, self.id_collection)
        self.assertEqual(new_id, 'TEST-000201')

    def test_register_reserved_id(self):
        h.bulk_reserve_id_range(1, 99, self.id_generator, self.id_collection, 'Reserve message', self.user)
        result = h.register_unique_id(self.id_collection, 'TEST-000001')
        self.assertTrue(result)

    def test_register_unreserved_id(self):
        result = h.register_unique_id(self.id_collection, 'TEST-000001')
        self.assertTrue(result)

    def test_register_used_id(self):
        result = h.register_unique_id(self.id_collection, 'TEST-000001')
        self.assertTrue(result)
        try:
            sid = transaction.savepoint()
            h.register_unique_id(self.id_collection, 'TEST-000001')
            transaction.savepoint_commit(sid)
        except IntegrityError as e:
            transaction.savepoint_rollback(sid)
            self.assertIsInstance(e, IntegrityError)

    def test_is_free_unique_id(self):
        result = h.is_free_unique_id(self.id_collection, 'TEST-000001')
        self.assertTrue(result)
        h.register_unique_id(self.id_collection, 'TEST-000001')
        result = h.is_free_unique_id(self.id_collection, 'TEST-000001')
        self.assertFalse(result)
