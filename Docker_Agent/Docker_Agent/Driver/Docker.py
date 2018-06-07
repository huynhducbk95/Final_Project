import docker


class DockerDriver():
    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    def list(self):
        container_list = self.client.containers.list()
        return container_list

    def inspect(self, container_id):
        container_info = self.client.containers.get(container_id)
        return container_info

    def exec_ping_command(self, container_id, host_ip):
        cmd = 'ping -c 3 ' + host_ip
        container = self.client.containers.get(container_id)
        response = container.exec_run(cmd=cmd)
        if response.exit_code == 0:
            status = 'CONNECTED'
        else:
            status = 'DISCONNECTED'
        return status

    def add_nic(self, container_id, network_name, network_ip):
        network = self.client.networks.list(names=[network_name,])[0]
        network.disconnect(container=container_id)
        network.connect(container=container_id, ipv4_address=network_ip)
        return 'SUCCESS'
