from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from deployment_flow import etl_api_gcs_bq 

docker_block = DockerContainer.load("zoom")

docker_dep = Deployment.build_from_flow(
    flow=etl_api_gcs_bq,
    name='docker-flow',
    infrastructure=docker_block
)

if __name__=='__main__':
    docker_dep.apply()