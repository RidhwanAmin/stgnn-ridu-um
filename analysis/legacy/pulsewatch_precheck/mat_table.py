"""Pure-Python reader for the Aligned-ECG MATLAB `table` objects.

The released `*_final_align_output_LinearInterp.mat` store a MATLAB `table`
(MCOS-serialized) that scipy/h5py/pymatreader cannot decode, and MATLAB batch
is unavailable here (license hang). This module parses the MAT5 subsystem
(`__function_workspace__`) directly and extracts the fields we need.

Validated against the 30 UID-102 probe tables: patch id, hour, monotonically
increasing start/end, slice lengths ~6976-7480 (~28-30 s @ 250 Hz), flags all 0.

Table columns (from PulsewatchAlignment/func/my_func_gen_ECG_start_end_point.m,
plus later T_12..T_14): T_1_ECG_patch_name (e.g. '102A'), T_2_ECG_one_hr_idx,
T_3_ECG_start_idx, T_4_ECG_end_idx (1-based), T_8_ECG_contain_empty,
T_9_pad_zero_front, T_10_pad_zero_end, T_11_fs_ECG.
"""
from __future__ import annotations

import io
import re
import struct

import numpy as np
import scipy.io as sio

_NUMPY = {1: np.int8, 2: np.uint8, 3: np.int16, 4: np.uint16, 5: np.int32,
          6: np.uint32, 7: np.float32, 9: np.float64, 12: np.int64, 13: np.uint64}
# Patch id like '102A' (clinical, UID+patch letter) or possibly '400' (AF trial,
# no letter). Matched against short char leaves; the 36-char PPG filename etc.
# never fullmatch. Verified against real AF subjects during validation.
_PATCH_RE = re.compile(r"\d{3}[A-Za-z]{0,2}")


def _read_element(b: bytes, o: int):
    """Return (data_type, nbytes, data, next_offset) for a MAT5 element."""
    (v,) = struct.unpack_from("<I", b, o)
    if (v >> 16) != 0:                       # small element format
        dt = v & 0xFFFF
        nb = (v >> 16) & 0xFFFF
        return dt, nb, b[o + 4 : o + 4 + nb], o + 8
    dt = v
    (nb,) = struct.unpack_from("<I", b, o + 4)
    do = o + 8
    pad = (8 - (nb % 8)) % 8
    return dt, nb, b[do : do + nb], do + nb + pad


def _leaves(ss: bytes) -> list[tuple[int, int, bytes]]:
    """Depth-first list of non-miMATRIX leaf elements in storage order."""
    out: list[tuple[int, int, bytes]] = []

    def walk(o: int, end: int):
        while o < end - 3:
            dt, nb, data, nxt = _read_element(ss, o)
            if nxt <= o or nxt > end + 8:
                break
            if dt == 14:                      # miMATRIX: skip flags/dims/name, recurse
                p = o + 8
                for _ in range(3):
                    _, _, _, p = _read_element(ss, p)
                walk(p, nxt)
            else:
                out.append((dt, nb, data))
            o = nxt

    walk(8, len(ss))                          # subsystem body starts after 8-byte prefix
    return out


def read_aligned_mat(path) -> dict:
    """Parse one Aligned .mat -> dict(patch_id, hour, start, end,
    contain_empty, pad_front, pad_end, fs_ecg). patch_id is None if the table
    has no patch (treat as no-ECG)."""
    raw = open(path, "rb").read()
    d = sio.loadmat(io.BytesIO(raw))
    fw = d.get("__function_workspace__")
    if fw is None:
        return {"patch_id": None}
    ss = np.asarray(fw).tobytes()
    leaves = _leaves(ss)

    decoded = []
    for dt, nb, data in leaves:
        if dt == 16 and nb > 0:               # utf8 char
            try:
                decoded.append(("s", data.split(b"\x00")[0].decode("utf8")))
            except UnicodeDecodeError:
                decoded.append(("s", ""))
        elif dt in _NUMPY:
            decoded.append(("n", np.frombuffer(data[:nb], dtype=_NUMPY[dt])))
        else:
            decoded.append(("?", None))

    # T_1 patch id: first char leaf matching NNN + patch letter(s), e.g. '102A'
    pidx = None
    patch_id = None
    for i, (k, v) in enumerate(decoded):
        if k == "s" and v and _PATCH_RE.fullmatch(v):
            pidx = i
            patch_id = v
            break
    if pidx is None:
        return {"patch_id": None}

    # The next three float64 scalars after the patch id are T_2/T_3/T_4.
    nums = []
    for k, v in decoded[pidx + 1:]:
        if k == "n" and v.dtype == np.float64 and v.size == 1:
            nums.append(float(v[0]))
            if len(nums) == 3:
                break
    hour, start, end = (nums + [None, None, None])[:3]

    # The first three uint8 scalars after the patch id are T_8/T_9/T_10 flags.
    flags = []
    for k, v in decoded[pidx + 1:]:
        if k == "n" and v.dtype == np.uint8 and v.size == 1:
            flags.append(int(v[0]))
            if len(flags) == 3:
                break
    flags += [0] * (3 - len(flags))

    def _clean_int(x):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return None
        return int(round(x))

    return {
        "patch_id": patch_id,
        "hour": _clean_int(hour),
        "start": _clean_int(start),
        "end": _clean_int(end),
        "contain_empty": bool(flags[0]),
        "pad_front": bool(flags[1]),
        "pad_end": bool(flags[2]),
        "fs_ecg": 250,
    }
