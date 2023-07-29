import ffmpeg

def getFps(filename):
    probe = ffmpeg.probe(filename)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    fps1 = float(video_info['r_frame_rate'].split('/')[0])
    fps2 = float(video_info['r_frame_rate'].split('/')[1])
    test = fps1 / fps2
    return test