from api.auth.redis_connection import RedisConnection

class TokenManager:
    def __init__(self):
        # Initialize Redis connection
        self.redis_client = RedisConnection()

    def blacklist_token(self, token):
        with self.redis_client as redis_client:
            redis_client.set(token, 'revoked', ex=1800)  # Blacklist the token for 30 minutes
            print(f'Token {token} has been blacklisted for 30 minutes.')

    def is_token_blacklisted(self, token):
        with self.redis_client as redis_client:
            return redis_client.exists(token) > 0  # Check if token exists