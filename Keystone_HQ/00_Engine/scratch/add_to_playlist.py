import os, sys
SCRIPT_DIR = r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain'
sys.path.insert(0, SCRIPT_DIR)
os.chdir(SCRIPT_DIR)
from youtube_api_manager import YouTubeAPIManager

manager = YouTubeAPIManager(token_file='youtube_token.json')
youtube = manager.youtube

# Find playlist
playlists_response = youtube.playlists().list(
    part='snippet',
    mine=True,
    maxResults=50
).execute()

target_playlist_id = None
for pl in playlists_response.get('items', []):
    if 'Builder' in pl['snippet']['title'] or 'Shorts' in pl['snippet']['title']:
        print(f"Found Playlist: {pl['snippet']['title']} (ID: {pl['id']})")
        target_playlist_id = pl['id']
        break

if not target_playlist_id:
    # Create it
    print("Playlist not found. Creating 'Builder's Blueprint Shorts'")
    pl_response = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {'title': "Builder's Blueprint Shorts", 'description': 'Protocol Shorts'},
            'status': {'privacyStatus': 'public'}
        }
    ).execute()
    target_playlist_id = pl_response['id']

# Add video to playlist
try:
    youtube.playlistItems().insert(
        part='snippet',
        body={
            'snippet': {
                'playlistId': target_playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': 'UBfloJPy3lo'
                }
            }
        }
    ).execute()
    print('Successfully added video to playlist!')
except Exception as e:
    print(f'Error adding to playlist: {e}')
