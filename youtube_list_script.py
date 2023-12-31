# import tkinter as tk
# from tkinter import filedialog
# from googleapiclient.discovery import build
# from youtube_transcript_api import YouTubeTranscriptApi
# import re
# import openpyxl

# # YouTube API 키와 채널 ID
api_key = 'AIzaSyCXDwNUAeUIHbyk_CEmH1nQ_BAaJ-lniVQ'
channel_id = 'UCHEWCYP9MbA9RSUiMPvqK9A'


# # YouTube 동영상 목록 가져오기
# def fetch_videos():
#     youtube = build('youtube', 'v3', developerKey=api_key)
#     channel_response = youtube.channels().list(id=channel_id, part='contentDetails').execute()
#     uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#     videos = []
#     next_page_token = None
#     while True:
#         playlistitems_response = youtube.playlistItems().list(
#             playlistId=uploads_playlist_id,
#             part='snippet',
#             maxResults=50,
#             pageToken=next_page_token
#         ).execute()
#         videos += playlistitems_response['items']
#         next_page_token = playlistitems_response.get('nextPageToken')
#         if next_page_token is None:
#             break
#     return [(f'https://www.youtube.com/watch?v={v["snippet"]["resourceId"]["videoId"]}') for v in videos]

# # YouTube URL에서 비디오 ID 추출
# def extract_video_id(youtube_url):
#     match = re.search(r"v=([^&]+)", youtube_url) or re.search(r"youtu\.be/([^?]+)", youtube_url)
#     return match.group(1) if match else None

# # YouTube 자막 가져오기
# def get_youtube_transcript(video_id):
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
#         transcript_text = '\n'.join([t['text'] for t in transcript])
#         return transcript_text
#     except Exception as e:
#         return str(e)

# # 엑셀 파일에 저장
# def save_to_excel(data, file_path):
#     workbook = openpyxl.Workbook()
#     sheet = workbook.active
#     sheet.title = 'YouTube Transcripts'
#     sheet.append(['Video URL', 'Transcript'])
#     for url, transcript in data:
#         sheet.append([url, transcript])
#     workbook.save(file_path)

# # 프로세스 제어 및 GUI 업데이트
# def process_and_save():
#     videos = fetch_videos()
#     data = []
#     for i, url in enumerate(videos, start=1):
#         transcript = get_youtube_transcript(extract_video_id(url))
#         data.append((url, transcript))
#         print(f"{i}번째 작업중")
#     output_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
#     if output_file_path:
#         save_to_excel(data, output_file_path)

# # Tkinter GUI 설정
# app = tk.Tk()
# app.title("YouTube Video and Transcript Fetcher")

# process_button = tk.Button(app, text="Fetch Videos and Transcripts", command=process_and_save)
# process_button.pack(pady=20)

# app.mainloop()


import tkinter as tk
from tkinter import filedialog
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import re
import openpyxl

# # YouTube API 키와 채널 ID
# api_key = 'YOUR_API_KEY'
# channel_id = 'YOUR_CHANNEL_ID'

# YouTube 동영상 목록 가져오기
def fetch_videos():
    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_response = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos = []
    next_page_token = None
    while True:
        playlistitems_response = youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part='snippet',
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        videos += playlistitems_response['items']
        next_page_token = playlistitems_response.get('nextPageToken')
        if next_page_token is None:
            break
    return [(v['snippet']['title'], f'https://www.youtube.com/watch?v={v["snippet"]["resourceId"]["videoId"]}', v['snippet']['publishedAt']) for v in videos]

# YouTube URL에서 비디오 ID 추출
def extract_video_id(youtube_url):
    match = re.search(r"v=([^&]+)", youtube_url) or re.search(r"youtu\.be/([^?]+)", youtube_url)
    return match.group(1) if match else None

# YouTube 자막 가져오기
def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        transcript_text = '\n'.join([t['text'] for t in transcript])
        return transcript_text
    except Exception as e:
        return str(e)

# 엑셀 파일에 저장
def save_to_excel(data, file_path):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'YouTube Videos and Transcripts'
    sheet.append(['Title', 'Video URL', 'Published Date', 'Transcript'])
    for title, url, date, transcript in data:
        sheet.append([title, url, date, transcript])
    workbook.save(file_path)

# 프로세스 제어 및 GUI 업데이트
def process_and_save():
    videos = fetch_videos()
    total_number = len(videos)
    data = []
    i=0
    for title, url, date in videos:
        
        transcript = get_youtube_transcript(extract_video_id(url))
        data.append((title, url, date, transcript))
        print(f'{total_number} 중 {i} {date} 작업 중입니다. 오정훈님')
        i+=1
    output_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if output_file_path:
        save_to_excel(data, output_file_path)

# Tkinter GUI 설정
app = tk.Tk()
app.title("YouTube Video and Transcript Fetcher")

process_button = tk.Button(app, text="Fetch Videos and Transcripts", command=process_and_save)
process_button.pack(pady=20)

app.mainloop()
