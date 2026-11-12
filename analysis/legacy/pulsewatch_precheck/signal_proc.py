"""
Uniform PPG -> (PPG, HR, magHR) channel derivation, applied identically to EVERY
cohort (Pulsewatch, Simband, MIMIC) so HR is a consistent channel and cannot become
a preprocessing/domain artifact. One band-pass + one peak detector for all.
"""
import numpy as np
import torch
from scipy.signal import butter, filtfilt, find_peaks, welch

FS = 50
SEG_LEN = 1500


def bandpass_ppg(ppg, fs=FS, lo=0.5, hi=8.0, order=3):
    x = np.asarray(ppg, dtype=np.float64).ravel()
    if x.size < 20 or not np.isfinite(x).all():
        x = np.nan_to_num(x)
    b, a = butter(order, [lo / (fs / 2), hi / (fs / 2)], btype="band")
    try:
        return filtfilt(b, a, x)
    except Exception:
        return x - np.mean(x)


def _moving_avg(x, w):
    w = max(1, int(w))
    return np.convolve(x, np.ones(w) / w, mode="same")


def detect_ppg_peaks(ppg_filt, fs=FS):
    """Elgendi-2013 two-moving-average adaptive-threshold systolic-peak detector.
    Robust to baseline wander / amplitude drift; rhythm-agnostic (handles AF)."""
    x = np.asarray(ppg_filt, dtype=np.float64)
    if x.std() < 1e-9:
        return np.array([], dtype=int)
    sq = np.clip(x, 0, None) ** 2                     # clip negatives + square
    W1 = max(1, int(round(0.111 * fs)))               # systolic window (~6 @50 Hz)
    W2 = max(1, int(round(0.667 * fs)))               # beat window (~33 @50 Hz)
    thr = _moving_avg(sq, W2) + 0.02 * sq.mean()      # MA_beat + beta*mean
    boi = _moving_avg(sq, W1) > thr                   # blocks of interest
    idx = np.where(boi)[0]
    if idx.size == 0:
        return np.array([], dtype=int)
    groups = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    refr = int(0.30 * fs)                             # <=200 bpm refractory
    peaks = []
    for g in groups:
        if g.size < W1:                               # too narrow -> not a systolic peak
            continue
        p = int(g[np.argmax(x[g])])                   # peak = max of filtered signal in block
        if not peaks or p - peaks[-1] >= refr:
            peaks.append(p)
        elif x[p] > x[peaks[-1]]:                     # merge within refractory, keep taller
            peaks[-1] = p
    return np.array(peaks, dtype=int)


def ppg_sqi(ppg, fs=FS):
    """Morphology signal-quality in [0,1] = mean beat-to-template correlation.
    Rhythm-AGNOSTIC (does not penalize AF): noise destroys pulse morphology even
    when peaks are found; AF pulses keep a consistent shape."""
    filt = bandpass_ppg(_fix(ppg), fs)
    peaks = detect_ppg_peaks(filt, fs)
    if peaks.size < 5:                                # implausibly few beats -> unusable
        return 0.0
    half = int(0.30 * fs)
    beats = [filt[p - half:p + half] for p in peaks if p - half >= 0 and p + half <= filt.size]
    if len(beats) < 4:
        return 0.0
    B = np.array(beats, dtype=np.float64)
    B = (B - B.mean(1, keepdims=True)) / (B.std(1, keepdims=True) + 1e-9)
    tmpl = B.mean(0)
    tmpl = (tmpl - tmpl.mean()) / (tmpl.std() + 1e-9)
    corrs = (B * tmpl).mean(1)                        # Pearson r per beat (both z-scored)
    return float(np.clip(np.nanmean(corrs), 0.0, 1.0))


def derive_hr(peaks, n=SEG_LEN, fs=FS):
    """Instantaneous HR (60/RR) piecewise-held to length n, clamped [30,220]."""
    out = np.zeros(n, dtype=np.float64)
    peaks = np.asarray(peaks, dtype=int)
    if peaks.size < 2:
        return out
    hr = np.clip(60.0 / (np.diff(peaks) / fs), 30, 220)     # len = #peaks-1
    for i in range(hr.size):
        out[peaks[i]:peaks[i + 1]] = hr[i]
    out[:peaks[0]] = hr[0]
    out[peaks[-1]:] = hr[-1]
    return out


def _minmax(x):
    lo, hi = x.min(), x.max()
    return (x - lo) / ((hi - lo) if hi > lo else (hi - lo + 1e-10))


def _fix(ppg, n=SEG_LEN):
    ppg = np.asarray(ppg, dtype=np.float64).ravel()
    if ppg.size == n:
        return ppg
    return ppg[:n] if ppg.size > n else np.concatenate([ppg, np.zeros(n - ppg.size)])


def make_channels(ppg_1500, fs=FS):
    """Return (ppg, hr, maghr) tensors each (1,1500). Uniform across all cohorts."""
    ppg = _fix(ppg_1500)
    filt = bandpass_ppg(ppg, fs)
    peaks = detect_ppg_peaks(filt, fs)
    hr = derive_hr(peaks, SEG_LEN, fs)

    ppg_n = _minmax(filt)
    hr30 = (hr - 30.0) / 190.0
    maghr = _minmax(hr) if hr.max() > hr.min() else np.zeros_like(hr)

    def t(x):
        return torch.from_numpy(np.ascontiguousarray(x, dtype=np.float32)).reshape(1, SEG_LEN)
    return t(ppg_n), t(hr30), t(maghr)


def acc_channel(acc, uid):
    """Authors' 4th input channel (my_dataloader `1D_PPG_HR_ACC_rescaleHR`): raw ACC ->
    FIXED 0-20 m/s^2 min-max -> [0,1]. Simband (UID starts '6') is x9.8 first (g -> m/s^2),
    exactly as the original loader. Returns (1,1500)."""
    a = np.asarray(acc, dtype=np.float32).ravel()
    if a.size != SEG_LEN:
        a = a[:SEG_LEN] if a.size > SEG_LEN else np.concatenate([a, np.zeros(SEG_LEN - a.size, np.float32)])
    if str(uid)[0] == "6":
        a = a * 9.8
    a = np.clip(a / 20.0, 0.0, 1.0)
    return torch.from_numpy(np.ascontiguousarray(a, dtype=np.float32)).reshape(1, SEG_LEN)


def rr_irregularity(ppg_1500, fs=FS):
    """RMSSD-like RR irregularity (ms) — a physiologic AF proxy (AF => higher)."""
    peaks = detect_ppg_peaks(bandpass_ppg(_fix(ppg_1500), fs), fs)
    if peaks.size < 3:
        return float("nan")
    rr = np.diff(peaks) / fs * 1000.0
    return float(np.sqrt(np.mean(np.diff(rr) ** 2)))


GFEAT_DIM = 6


def _robust_bandpass(x, fs=FS, lo=0.5, hi=4.0):
    b, a = butter(3, [lo / (fs / 2), hi / (fs / 2)], btype="band")
    try:
        return filtfilt(b, a, x)
    except Exception:
        return x - np.mean(x)


def global_rhythm_features(ppg, fs=FS):
    """Device-invariant, PEAK-INDEPENDENT rhythm-regularity descriptors in ~[0,1].

    A regular rhythm is periodic (strong autocorrelation, peaked spectrum); AF is
    irregular (weak autocorrelation, flat/high-entropy spectrum). These measure rhythm
    regularity GLOBALLY (no reliance on individual peak locations), so they survive the
    noisy-device beat-detection failure that corrupts the beat-graph on wrist-PPG, and
    they carry the SAME AF<->NSR relationship across devices (validated: AF-vs-NSR AUROC
    0.95-0.996 on Simband / clinical / 4xx). Returns GFEAT_DIM floats."""
    x = bandpass_ppg(_fix(ppg), fs)
    if x.std() < 1e-9:
        return np.zeros(GFEAT_DIM, dtype=np.float32)

    xz = (x - x.mean()) / (x.std() + 1e-9)
    ac = np.correlate(xz, xz, "full")[len(xz) - 1:]
    ac = ac / (ac[0] + 1e-9)
    lo_lag, hi_lag = int(0.33 * fs), int(1.5 * fs)            # 40-180 bpm
    seg = ac[lo_lag:hi_lag]
    if seg.size:
        peak_lag = lo_lag + int(np.argmax(seg))
        autocorr_periodicity = float(np.clip(ac[peak_lag], 0.0, 1.0))
        h = 2 * peak_lag
        autocorr_harmonic = float(np.clip(ac[h], 0.0, 1.0)) if h < ac.size else 0.0
    else:
        autocorr_periodicity = autocorr_harmonic = 0.0

    fq, P = welch(x, fs=fs, nperseg=min(256, x.size))
    P = P + 1e-12
    Pn = P / P.sum()
    spectral_entropy = float(-np.sum(Pn * np.log(Pn)) / np.log(len(Pn)))
    band = (fq >= 0.7) & (fq <= 3.5)                          # HR band 42-210 bpm
    hr_peak_ratio = float(P[band].max() / P[band].sum()) if band.any() and P[band].sum() > 0 else 0.0
    spectral_centroid = float(np.sum(fq * Pn) / (fs / 2.0))   # normalized to Nyquist

    pk = detect_ppg_peaks(_robust_bandpass(_fix(ppg), fs), fs)
    if pk.size > 2:
        rr = np.diff(pk) / fs * 1000.0
        rr_irreg = float(np.clip(np.sqrt(np.mean(np.diff(rr) ** 2)) / 500.0, 0.0, 1.0))
    else:
        rr_irreg = 0.0

    return np.array([autocorr_periodicity, autocorr_harmonic, spectral_entropy,
                     hr_peak_ratio, spectral_centroid, rr_irreg], dtype=np.float32)


N_ACC_FEAT = 3


def per_node_acc_features(acc, peaks, fs=FS):
    """3 DEVICE-INVARIANT per-beat motion features from the ACC window over each beat's RR
    interval, all WITHIN-SEGMENT normalized (absolute ACC scale is device-variant -- different
    accelerometer scaling/placement -- so absolute features would fail cross-device exactly like
    morphology did). Per-beat motion energy = std of ACC over the beat's territory (between the
    midpoints to its neighbours), which removes the ~1g DC offset and measures movement.
      [0] energy ratio = beat energy / segment mean beat energy
      [1] z-score      = (beat energy - segment mean) / segment std
      [2] high-motion  = 1.0 if beat energy > segment 80th percentile else 0.0
    Returns (K, 3) float32; ALL ZEROS when ACC is dead/constant (e.g. the MIMIC placeholder),
    so a missing/flat accelerometer contributes no information rather than noise."""
    acc = _fix(acc).astype(np.float64).ravel()
    K = len(peaks)
    if K == 0:
        return np.zeros((0, N_ACC_FEAT), dtype=np.float32)
    n = acc.size
    energy = np.empty(K, dtype=np.float64)
    for k in range(K):
        lo = 0 if k == 0 else (int(peaks[k - 1]) + int(peaks[k])) // 2
        hi = n if k == K - 1 else (int(peaks[k]) + int(peaks[k + 1])) // 2
        lo = max(0, min(lo, n - 2)); hi = max(lo + 2, min(hi, n))
        energy[k] = acc[lo:hi].std()
    m = float(energy.mean())
    if m < 1e-9:                                   # dead / constant ACC -> neutral (no motion info)
        return np.zeros((K, N_ACC_FEAT), dtype=np.float32)
    ratio = energy / m
    z = (energy - m) / (energy.std() + 1e-9)
    flag = (energy > np.percentile(energy, 80)).astype(np.float64)
    return np.stack([ratio, z, flag], axis=1).astype(np.float32)
