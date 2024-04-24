import src.resources as resources


def config_api_urls(api):
    """
    adds api endpoints to the flask app
    :param api: flask-restful object
    """
    api.add_resource(resources.HealthCheck, "/healthcheck")
    api.add_resource(resources.DepartmentResource, "/departments")
    # api.add_resource(resources.AccountDetails, "/doctors")
    # api.add_resource(resources.AccountDetails, "/patients")
