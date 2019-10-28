import docker
from cpuinfo import get_cpu_info
from psutil import virtual_memory


#System Information
#Get CPU information
cpu = get_cpu_info()
#Get Memory Information
mem = virtual_memory()
ram = mem.total / 1024 / 1024 / 1024


#Connect to Docker Socket
apiclient = docker.APIClient(base_url='unix://var/run/docker.sock')
client = docker.from_env()

#APIClient Informations [Low Level API]
dockerinfo = apiclient.version()
container_count = len(apiclient.containers(all=True))
image_count = len(apiclient.images(all=True))
docker_container = apiclient.containers(all=True)
docker_image = apiclient.images(all=True)
docker_volume = apiclient.volumes()

#High Level API
volume_count = len(client.volumes.list())



