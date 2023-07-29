import yt_dlp


def dl_video_audio(url, filename):
    filename = filename
    yt_opts = {
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '256'
        }],
        'postprocessor_args': [
            '-ar', '16000',
            '-ac', '1' 
        ],
        'format': "bv[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv+ba/b",
        'outtmpl': 'input/' + filename + '.%(ext)s',
        'prefer_ffmpeg' : True,
        'keepvideo': True
    }
    y = yt_dlp.YoutubeDL(yt_opts)
    y.download(url)

# def dlVideo(url, filename):
#     yt_opts = {
#         'format': "bv[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv+ba/b",
#         'outtmpl': filename,

#     }
#     y = yt_dlp.YoutubeDL(yt_opts)
#     y.download(url)
#     return filename
