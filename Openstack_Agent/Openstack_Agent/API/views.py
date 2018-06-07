from django.http import HttpResponse
from Openstack_Agent.Driver.Openstack import OpenstackDriver
import json
import os
from Openstack_Agent.Driver.Qemu import QemuDriver


def workload_list(request):
    if request.method == 'GET':
        openstack_config = {}
        openstack_config['os_auth_url'] = request.GET.get('os_auth_url', None)
        openstack_config['os_project_name'] = request.GET.get('os_project_name', None)
        openstack_config['os_username'] = request.GET.get('os_username', None)
        openstack_config['os_password'] = request.GET.get('os_password', None)
        openstack_config['os_project_domain_name'] = request.GET.get('os_project_domain_name', None)
        openstack_config['os_user_domain_name'] = request.GET.get('os_user_domain_name', None)
        openstack_config['os_novaclient_version'] = request.GET.get('os_novaclient_version', None)
        hostname = request.GET.get('hostname', None)
        openstack_client = OpenstackDriver(cloud_config=openstack_config)
        workload_list_obj = openstack_client.list()
        workload_list = []
        for workload in workload_list_obj:
            if workload._info['OS-EXT-SRV-ATTR:host'] == hostname:
                workload_info = {
                    'name': workload.name,
                    'uuid': workload.id,
                    'status': workload.status,
                }
                network_list = []
                for key, value in workload.networks.items():
                    for ip in value:
                        network_info = {
                            'name': key,
                            'ip': ip,
                        }
                        network_list.append(network_info)
                workload_info['network'] = network_list
                workload_list.append(workload_info)
        result = {
            'list': workload_list
        }
        return HttpResponse(json.dumps(result), content_type='application/json')


def check_ping(request):
    if request.method == 'GET':
        next_hop = request.GET.get('ip', None)
        response = os.system("ping -c 4 " + next_hop)
        if response == 0:
            ping_status = 'CONNECTED'
        else:
            ping_status = 'DISCONNECTED'
        result = {
            'status': ping_status,
        }
        return HttpResponse(json.dumps(result), content_type='application/json')


def check_workload_ping(request):
    if request.method == 'GET':
        openstack_config = {}
        openstack_config['os_auth_url'] = request.GET.get('os_auth_url', None)
        openstack_config['os_project_name'] = request.GET.get('os_project_name', None)
        openstack_config['os_username'] = request.GET.get('os_username', None)
        openstack_config['os_password'] = request.GET.get('os_password', None)
        openstack_config['os_project_domain_name'] = request.GET.get('os_project_domain_name', None)
        openstack_config['os_user_domain_name'] = request.GET.get('os_user_domain_name', None)
        openstack_config['os_novaclient_version'] = request.GET.get('os_novaclient_version', None)
        workload_uuid = request.GET.get('uuid', None)
        host_ip = request.GET.get('host_ip', None)
        openstack_client = OpenstackDriver(cloud_config=openstack_config)
        response = openstack_client.show(instance_id=workload_uuid)
        workload_name = response._info['OS-EXT-SRV-ATTR:instance_name']
        qemu_agent = QemuDriver(workload_name)
        ping_status = qemu_agent.check_ping_to_host(host_ip=host_ip)
        result = {
            'status': ping_status
        }

        return HttpResponse(json.dumps(result), content_type='application/json')


def add_nic(request):
    if request.method == 'POST':
        openstack_config = {}
        openstack_config['os_auth_url'] = request.POST.get('os_auth_url', None)
        openstack_config['os_project_name'] = request.POST.get('os_project_name', None)
        openstack_config['os_username'] = request.POST.get('os_username', None)
        openstack_config['os_password'] = request.POST.get('os_password', None)
        openstack_config['os_project_domain_name'] = request.POST.get('os_project_domain_name', None)
        openstack_config['os_user_domain_name'] = request.POST.get('os_user_domain_name', None)
        openstack_config['os_novaclient_version'] = request.POST.get('os_novaclient_version', None)
        workload_uuid = request.POST.get('uuid', None)
        openstack_client = OpenstackDriver(cloud_config=openstack_config)
        network_id = openstack_client.choice_network(instance_id=workload_uuid)
        openstack_client.add_nic(instance_id=workload_uuid, net_id=network_id)
        response = openstack_client.show(instance_id=workload_uuid)
        workload_name = response._info['OS-EXT-SRV-ATTR:instance_name']
        qemu_agent = QemuDriver(workload_name)
        status = qemu_agent.add_nic()
        result = {
            'status': status,
        }

        return HttpResponse(json.dumps(result), content_type='application/json')
