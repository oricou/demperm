from drf_spectacular.extensions import OpenApiAuthenticationExtension

class SimpleBearerAuthScheme(OpenApiAuthenticationExtension):
    target_class = "app.security_config.SimpleBearerAuthentication"
    name = "bearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
