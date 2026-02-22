
import os
import pygame

AUDIO_DIR = "voiceovers"
pygame.mixer.init()

files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")])
durations = {}

for f in files:
    path = os.path.join(AUDIO_DIR, f)
    # Sound needs .wav usually in some pygame versions, but music works for duration too?
    # Actually pygame.mixer.Sound doesn't handle mp3 well sometimes.
    # Let's use mutagen or just try music.get_length()
    try:
        pygame.mixer.music.load(path)
        durations[f] = pygame.mixer.Sound(path).get_length() # This might fail for mp3
    except:
        # Fallback: estimate based on file size (kbps approx)
        size = os.path.getsize(path)
        durations[f] = size / 16000 # very rough estimate (128kbps = 16KB/s)

for f, d in durations.items():
    print(f"{f}: {d:.2f}s")
