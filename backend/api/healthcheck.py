from backend import api
from backend.swagger import swagger
from backend.wsgi import remote, messages, message_types


class HealthCheckResponse(messages.Message):
    message = messages.StringField(1)


@api.endpoint(path="healthcheck", title="Health Check")
class HealthCheck(remote.Service):
    @swagger("Health Check")
    @remote.method(message_types.VoidMessage, HealthCheckResponse)
    def get(self):
        return HealthCheckResponse(
            message="ok"
        )
