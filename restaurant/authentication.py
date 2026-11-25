from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    Accept ``Authorization: Bearer <token>`` in addition to DRF's default
    ``Authorization: Token <token>``.

    Insomnia's "Bearer Token" auth type sends the ``Bearer`` prefix, so this
    lets the API be tested exactly as described in the project instructions.
    """

    keyword = 'Bearer'
