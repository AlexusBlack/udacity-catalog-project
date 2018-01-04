import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from flask import Blueprint, url_for, session, redirect, flash, request, render_template
from security import credentials_to_dict

CLIENT_SECRETS_FILE = 'client_secret_701113834116-726adijgkns945m5l467eu6gu02lb18b.apps.googleusercontent.com.json'
SCOPES = ['profile']

auth_system = Blueprint('auth_system', __name__, template_folder='templates')

@auth_system.route('/login', methods = ['GET'])
def login_route():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('auth_system.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)

@auth_system.route('/logout', methods = ['GET'])
def logout_route():
    if 'credentials' in session:
        del session['credentials']
    flash('You logged out')
    return redirect(url_for('index_route'))

@auth_system.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('auth_system.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    # requesting use info
    service = googleapiclient.discovery.build('people', 'v1', credentials=credentials)
    result = service.people().get(resourceName='people/me', personFields='names,photos').execute()

    user_id = result['resourceName']
    user_name = result['names'][0]['displayName']
    user_photo = url_for('static', filename='images/no-profile-photo.svg')
    if len(result['photos']) > 0:
        user_photo = result['photos'][0]['url']

    session['user_id'] = user_id
    session['user_name'] = user_name
    session['user_photo'] = user_photo

    return redirect(url_for('index_route'))