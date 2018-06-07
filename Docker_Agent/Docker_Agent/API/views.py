from django.http import HttpResponse
from Docker_Agent.Driver.Docker import DockerDriver
import json
import os


def workload_list(request):
    if request.method == 'GET':
        docker_client = DockerDriver()
        workload_list_obj = docker_client.list()
        workload_list = []
        for workload in workload_list_obj:
            workload_info = {
                'name': workload.name,
                'uuid': workload.id,
                'status': workload.status,
            }
            network_list = []
            for key, value in workload.attrs['NetworkSettings']['Networks'].items():
                network_info = {
                    'name': key,
                    'ip': value['IPAddress']
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
        workload_uuid = request.GET.get('uuid', None)
        host_ip = request.GET.get('host_ip', None)
        docker_client = DockerDriver()
        ping_status = docker_client.exec_ping_command(container_id=workload_uuid, host_ip=host_ip)
        result = {
            'status': ping_status
        }

        return HttpResponse(json.dumps(result), content_type='application/json')


def add_nic(request):
    if request.method == 'GET':
        workload_uuid = request.GET.get('uuid', None)
        network_ip = request.GET.get('ip', None)
        network_name = request.GET.get('network_name', None)
        docker_client = DockerDriver()
        status = docker_client.add_nic(container_id=workload_uuid,
                                       network_name=network_name,
                                       network_ip=network_ip)
        result = {
            'status': status
        }

        return HttpResponse(json.dumps(result), content_type='application/json')
