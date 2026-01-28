import librosa
import numpy as np

def load_audio(path):
    y, sr = librosa.load(path, sr=16000, mono=True)
    print(f"Loaded audio file '{path}' with sample rate {sr} Hz")
    return y, sr

def pitch_autocorr(y, sr, fmin=75, fmax=500):
    frame_len = int(0.03 * sr)
    hop_len = int(0.01 * sr)

    pitches = []

    for i in range(0, len(y) - frame_len, hop_len):
        frame = y[i:i+frame_len]
        frame -= np.mean(frame)

        corr = np.correlate(frame, frame, mode='full')
        corr = corr[len(corr)//2:]

        min_lag = int(sr / fmax)
        max_lag = int(sr / fmin)

        lag = np.argmax(corr[min_lag:max_lag]) + min_lag
        pitch = sr / lag if lag > 0 else 0

        if fmin <= pitch <= fmax:
            pitches.append(pitch)

    if not pitches:
        return 0.0, 0.0

    return float(np.mean(pitches)), float(np.std(pitches))

def speech_rate(y, sr):
    energy = librosa.feature.rms(y=y)[0]
    threshold = np.mean(energy)
    speech_frames = energy > threshold

    duration_min = librosa.get_duration(y=y, sr=sr) / 60
    return np.sum(speech_frames) / max(duration_min, 0.01)

def pause_ratio(y):
    rms = librosa.feature.rms(y=y)[0]
    return float(np.mean(rms < 0.02))

def energy_variability(y):
    rms = librosa.feature.rms(y=y)[0]
    return float(np.std(rms))

def spectral_flux(y):
    stft = np.abs(librosa.stft(y))
    return float(np.mean(np.diff(stft, axis=1)**2))

def confidence_score(rate, pitch_std, pause, energy_var):
    score = 0

    if rate > 120: score += 2
    elif rate > 90: score += 1

    if pitch_std < 40: score += 2
    elif pitch_std < 60: score += 1

    if pause < 0.25: score += 1
    if energy_var < 0.02: score += 1

    return min(score, 5)

def cognitive_load_score(pause, pitch_std, rate):
    score = 0

    if pause > 0.35: score += 2
    elif pause > 0.25: score += 1

    if pitch_std > 70: score += 2
    elif pitch_std > 50: score += 1

    if rate < 80: score += 1

    return min(score, 5)


def analyze_speech(audio_path):
    y, sr = load_audio(audio_path)

    pitch_mean, pitch_std = pitch_autocorr(y, sr)
    rate = speech_rate(y, sr)
    pause = pause_ratio(y)
    energy_var = energy_variability(y)
    flux = spectral_flux(y)

    return {
        "speech_rate_wpm": round(rate, 1),
        "pause_ratio": round(pause, 2),
        "pitch_mean_hz": round(pitch_mean, 1),
        "pitch_variability": round(pitch_std, 1),
        "energy_variability": round(energy_var, 4),
        "spectral_flux": round(flux, 2),
        "confidence_score": confidence_score(rate, pitch_std, pause, energy_var),
        "cognitive_load_score": cognitive_load_score(pause, pitch_std, rate)
    }
    
if __name__ == "__main__":
    ret=analyze_speech("C:\\Users\\BGupta\\Desktop\\InterviewHackathon.wav")
    print(ret)