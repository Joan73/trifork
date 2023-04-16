USER_IDS = (
    'jponte98@gmail.com',
    'trifork@emails.homerun.co'
)

SECRET = 'trifork_secret'

ENCODING_ALGORITHM = 'HS256'

# Authorization header
AUTHORIZATION_HEADER = 'Authorization'
AUTHORIZATION_METHOD = 'bearer'

# Token-related constants in seconds
TOKEN_LIFETIME = 60000
TOKEN_EXPIRATION_LEEWAY = 10

# DDoS throttling safeguard in seconds
DDOS_THROTTLE = 5

JWT_DECODE_OPTIONS = {
    'require': ['user_id', 'exp', 'iat'], 
    'verify': ['exp', 'iat']
}