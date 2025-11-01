import yaml
import webbrowser
import urllib.parse
import requests

# 1. YAML betöltése
with open('google-ads.yaml', 'r') as f:
    config = yaml.safe_load(f)

client_id = config['client_id']
client_secret = config['client_secret']

# 2. OAuth2 URL kézzel
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
scope = 'https://www.googleapis.com/auth/adwords'
auth_url = (
    f'https://accounts.google.com/o/oauth2/v2/auth?'
    f'client_id={urllib.parse.quote(client_id)}&'
    f'redirect_uri={urllib.parse.quote(redirect_uri)}&'
    f'response_type=code&'
    f'scope={urllib.parse.quote(scope)}&'
    f'access_type=offline&prompt=consent'
)

print('NYISD MEG EZT A LINKET A BÖNGÉSZŐBEN:')
print(auth_url)
webbrowser.open(auth_url)

code = input('Másold be a kódot (4/0A...): ').strip()

# 3. Token lekérése
token_url = 'https://oauth2.googleapis.com/token'
data = {
    'code': code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
}

response = requests.post(token_url, data=data).json()

if 'refresh_token' not in response:
    print('Hiba:', response)
else:
    config['refresh_token'] = response['refresh_token']
    with open('google-ads.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    print('SIKER! refresh_token elmentve!')
    print('refresh_token:', response['refresh_token'])
