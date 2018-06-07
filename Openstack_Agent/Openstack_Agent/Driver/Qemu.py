import subprocess
import json


class QemuDriver():
    def __init__(self, workload_name):
        self.workload_name = workload_name

    def check_ping_to_host(self, host_ip):
        cmd = ['virsh',
               'qemu-agent-command',
               self.workload_name,
               '{"execute":"guest-check-ping","arguments":{"content":"' + host_ip + '"}}',
               '--block']
        data_dict = self.convert_data(cmd)
        result = data_dict['return']['code']
        ping_status = ''
        if result == 0:
            ping_status = 'CONNECTED'
        else:
            ping_status = 'DISCONNECTED'
        return ping_status

    def add_nic(self):
        # check network device have no IP address
        cmd_get_nic = ['virsh',
                       'qemu-agent-command',
                       self.workload_name,
                       '{"execute":"guest-network-get-interfaces"}',
                       '--block', ]
        data_dict = self.convert_data(cmd_get_nic)
        list_nic = data_dict['return']
        nic_name = list_nic[len(list_nic)-1]['name']
        cmd_add_nic = ['virsh',
                       'qemu-agent-command',
                       self.workload_name,
                       '--block',
                       '{"execute":"guest-add_nic","arguments":{"content":"' + nic_name + '"}}']
        data_dict = self.convert_data(cmd_add_nic)
        result = 'SUCCESS'
        return result

    def convert_data(self, cmd):
        response = subprocess.run(cmd, stdout=subprocess.PIPE)
        data = response.stdout.decode('utf-8')
        data_dict = json.loads(data[0:-2])
        return data_dict

