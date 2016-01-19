from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.noclook.models import NodeHandle
from dynamic_preferences import global_preferences_registry
from apps.noclook import forms, helpers
from django.template.defaultfilters import slugify
import norduniclient as nc

# Use test instance of the neo4j db
nc.neo4jdb = nc.init_db('http://localhost:7475')

# We instanciate a manager for our global preferences
global_preferences = global_preferences_registry.manager()

class NeoTestCase(TestCase):

    def setUp(self):
        # Create user
        user = User.objects.create_user(username='test user', email='test@localhost', password='test')
        user.is_staff = True
        user.save()
        self.user = user
        # Set up client
        self.client = Client()
        self.client.login(username='test user', password='test')
        # Load the default forms
        global_preferences['general__data_domain'] = 'common'
        reload(forms)

    def tearDown(self):
        with nc.neo4jdb.transaction as t:
            t.execute("MATCH (a:Node) OPTIONAL MATCH (a)-[r]-(b) DELETE a, b, r").fetchall()
        super(NeoTestCase, self).tearDown()

    def get_full_url(self, what):
        if isinstance(what, NodeHandle):
            path = what.get_absolute_url()
        else:
            path = what
        return 'http://testserver{}'.format(path)

    def get_ports(self, node):
        return node.get_ports().get("Has",[])

    def get_node(self, name):
        nh = NodeHandle.objects.filter(node_type__type=self.node_type).get(node_name=name)
        node = nh.get_node()
        return nh,node

    def create(self,data):
        url = '/new/{}/'.format(slugify(self.node_type))
        return self.client.post(url, data)