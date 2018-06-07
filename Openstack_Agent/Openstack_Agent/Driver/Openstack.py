from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient.client import Client
from neutronclient.v2_0.client import Client as Neutron_Client

OPENSTACK_CONFIGUE = {
    'os_auth_url': 'http://25.66.88.22:35357/v3',
    'os_project_name': 'admin',
    'os_username': 'admin',
    'os_password': 'abc123',
    'os_project_domain_name': 'Default',
    'os_user_domain_name': 'Default',
    'os_novaclient_version': '2.1',
}


class OpenstackDriver():

    def __init__(self, cloud_config=None):
        cloud_config = OPENSTACK_CONFIGUE
        self.auth_url = cloud_config['os_auth_url']
        self.project_name = cloud_config['os_project_name']
        self.username = cloud_config['os_username']
        self.password = cloud_config['os_password']
        self.user_domain_name = \
            cloud_config['os_project_domain_name']
        self.project_domain_name = \
            cloud_config['os_user_domain_name']
        self.client_version = \
            cloud_config['os_novaclient_version']
        self._setup()

    def _setup(self):
        auth = v3.Password(auth_url=self.auth_url,
                           user_domain_name=self.user_domain_name,
                           username=self.username,
                           password=self.password,
                           project_domain_name=self.project_domain_name,
                           project_name=self.project_name)
        sess = session.Session(auth=auth)
        self.client = Client(self.client_version, session=sess)
        self.neutron_client = Neutron_Client(session=sess)

    def show(self, instance_id):
        server = self.client.servers.get(
            instance_id
        )
        return server

    def list(self):
        servers = self.client.servers.list()
        return servers

    def reboot(self, instance_id):
        """Soft reboot"""
        self.client.servers.reboot(instance_id)
        return True

    def list_nic(self, instance_id):
        """List all Network Interface Controller
        """
        # NOTE: interfaces a list of novaclient.v2.servers.Server
        interfaces = self.client.servers.interface_list(instance_id)
        return interfaces

    def list_ip(self, instance_id):
        """Add all IPs"""
        return dict(self.client.servers.ips(instance_id))

    def add_nic(self, instance_id, net_id):
        """Add a Network Interface Controller"""
        # TODO: upgrade with port_id and fixed_ip in future
        self.client.servers.interface_attach(
            instance_id, None, net_id, None)
        return True

    def shutdown(self, instance_id):
        self.client.servers.stop(instance_id)
        return True

    def start(self, instance_id):
        self.client.servers.start(instance_id)
        return True

    def net_list(self):
        list_net = self.neutron_client.list_networks()
        return list_net

    def choice_network(self, instance_id):
        network_choice = ''
        workload = self.show(instance_id=instance_id)
        network_name_list = []
        for key, value in workload.networks.items():
            network_name_list.append(key)

        list_net_obj = self.neutron_client.list_networks()
        list_network = list_net_obj['networks']
        for network in list_network:
            if network['name'] not in network_name_list:
                network_choice = network['id']
                break
        return network_choice
