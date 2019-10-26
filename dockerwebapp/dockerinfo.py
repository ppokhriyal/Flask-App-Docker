import docker


#Connect to Docker Socket
client = docker.DockerClient(base_url='unix://var/run/docker.sock')
dockerinfo = client.version()
