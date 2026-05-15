#!/usr/bin/env python3
"""
ULTRA MARIO 2D BROS - NES Authentic Edition

SMB1-style pygame game with 8 worlds x 4 levels.
Sprites + SFX + OST pre-baked at load. OST: YouTube rips in music/ (auto) or built-in Kondo loops. SFX: 2A03-style.
"""

import sys
import math
import random
import array
import base64
import io
import os

import pygame

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_MUSIC_DIR = os.path.join(_SCRIPT_DIR, 'music')

SCREEN_W, SCREEN_H = 768, 720
TILE = 48
FPS = 60

GRAVITY = 0.75
MAX_FALL = 14.0
PLAYER_ACC = 0.45
PLAYER_FRIC = 0.86
PLAYER_MAX_WALK = 4.5
PLAYER_MAX_RUN = 7.5
JUMP_FORCE = -14.5
BOUNCE_FORCE = -9.0
ENEMY_SPEED = 1.8
FIREBALL_SPEED = 8.0

LEVEL_WIDTH_TILES = 224
LEVEL_HEIGHT_TILES = 15

C_SKY = (92, 148, 252)
C_SKY_NIGHT = (12, 12, 56)
C_SKY_UNDER = (0, 0, 0)
C_SKY_CASTLE = (0, 0, 0)
C_SKY_ATHLETIC = (92, 148, 252)
C_BRICK = (200, 76, 12)
C_BRICK_DARK = (128, 40, 0)
C_BRICK_UNDER = (104, 136, 252)
C_BRICK_UNDER_D = (60, 88, 200)
C_QUESTION = (252, 152, 56)
C_QUESTION_HIT = (188, 120, 60)
C_GROUND_GREEN = (0, 168, 0)
C_PIPE_BASE = (184, 248, 24)
C_PIPE_DARK = (0, 168, 0)
C_PIPE_SHADE = (0, 120, 0)
C_MARIO_RED = (248, 56, 0)
C_MARIO_SKIN = (255, 204, 150)
C_MARIO_BROWN = (136, 112, 0)
C_GOOMBA = (228, 92, 16)
C_KOOPA_GREEN = (0, 168, 0)
C_COIN_GOLD = (252, 216, 168)
C_COIN_SHADOW = (168, 112, 0)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_HUD = (255, 255, 255)
C_CASTLE_GRAY = (188, 188, 188)
C_CASTLE_DARK = (116, 116, 116)
C_FIREBALL = (248, 56, 0)
C_LAVA = (228, 56, 0)
C_LAVA_BRIGHT = (252, 160, 68)
C_BRIDGE = (172, 124, 0)
C_BOWSER_GREEN = (0, 120, 0)
C_BOWSER_BELLY = (252, 216, 168)
C_AXE_GRAY = (188, 188, 188)
C_TREE_BROWN = (136, 80, 0)

CONTENTS_COIN = 'coin'
CONTENTS_MUSHROOM = 'mushroom'
CONTENTS_FIRE = 'fire'
CONTENTS_1UP = '1up'

# --- SMB1 ROM music (embedded; no external smb1_music_rom.py) ---
_SMB_NTSC = 1789773.0
_SMB_MUSIC_SR = 44100

_SMB_FREQ_TBL = bytes([
	0x00, 0x88, 0x00, 0x2f, 0x00, 0x00, 0x02, 0xa6, 0x02, 0x80, 0x02, 0x5c, 0x02, 0x3a,
	0x02, 0x1a, 0x01, 0xdf, 0x01, 0xc4, 0x01, 0xab, 0x01, 0x93, 0x01, 0x7c, 0x01, 0x67,
	0x01, 0x53, 0x01, 0x40, 0x01, 0x2e, 0x01, 0x1d, 0x01, 0x0d, 0x00, 0xfe, 0x00, 0xef,
	0x00, 0xe2, 0x00, 0xd5, 0x00, 0xc9, 0x00, 0xbe, 0x00, 0xb3, 0x00, 0xa9, 0x00, 0xa0,
	0x00, 0x97, 0x00, 0x8e, 0x00, 0x86, 0x00, 0x77, 0x00, 0x7e, 0x00, 0x71, 0x00, 0x54,
	0x00, 0x64, 0x00, 0x5f, 0x00, 0x59, 0x00, 0x50, 0x00, 0x47, 0x00, 0x43, 0x00, 0x3b,
	0x00, 0x35, 0x00, 0x2a, 0x00, 0x23, 0x04, 0x75, 0x03, 0x57, 0x02, 0xf9, 0x02, 0xcf,
	0x01, 0xfc, 0x00, 0x6a,
])
_SMB_LEN_TBL = bytes([
	0x05, 0x0a, 0x14, 0x28, 0x50, 0x1e, 0x3c, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x18, 0x30, 0x0c,
	0x03, 0x06, 0x0c, 0x18, 0x30, 0x12, 0x24, 0x08, 0x36, 0x03, 0x09, 0x06, 0x12, 0x1b, 0x24, 0x0c,
	0x24, 0x02, 0x06, 0x04, 0x0c, 0x12, 0x18, 0x08, 0x12, 0x01, 0x03, 0x02, 0x06, 0x09, 0x0c, 0x04,
])
_SMB_DUTY_FROM_HI = (0.125, 0.25, 0.5, 0.75)
_SMB_ROM = {
	'CastleMusData': bytes([
		0x80, 0x22, 0x28, 0x22, 0x26, 0x22, 0x24, 0x22, 0x26, 0x22, 0x28, 0x22, 0x2a, 0x22, 0x28, 0x22, 0x26,
		0x22, 0x28, 0x22, 0x26, 0x22, 0x24, 0x22, 0x26, 0x22, 0x28, 0x22, 0x2a, 0x22, 0x28, 0x22, 0x26,
		0x20, 0x26, 0x20, 0x24, 0x20, 0x26, 0x20, 0x28, 0x20, 0x26, 0x20, 0x28, 0x20, 0x26, 0x20, 0x24,
		0x20, 0x26, 0x20, 0x24, 0x20, 0x26, 0x20, 0x28, 0x20, 0x26, 0x20, 0x28, 0x20, 0x26, 0x20, 0x24,
		0x28, 0x30, 0x28, 0x32, 0x28, 0x30, 0x28, 0x2e, 0x28, 0x30, 0x28, 0x2e, 0x28, 0x2c, 0x28, 0x2e,
		0x28, 0x30, 0x28, 0x32, 0x28, 0x30, 0x28, 0x2e, 0x28, 0x30, 0x28, 0x2e, 0x28, 0x2c, 0x28, 0x2e, 0x00,
		0x04, 0x70, 0x6e, 0x6c, 0x6e, 0x70, 0x72, 0x70, 0x6e, 0x70, 0x6e, 0x6c, 0x6e, 0x70, 0x72, 0x70, 0x6e,
		0x6e, 0x6c, 0x6e, 0x70, 0x6e, 0x70, 0x6e, 0x6c, 0x6e, 0x6c, 0x6e, 0x70, 0x6e, 0x70, 0x6e, 0x6c,
		0x76, 0x78, 0x76, 0x74, 0x76, 0x74, 0x72, 0x74, 0x76, 0x78, 0x76, 0x74, 0x76, 0x74, 0x72, 0x74,
		0x84, 0x1a, 0x83, 0x18, 0x20, 0x84, 0x1e, 0x83, 0x1c, 0x28, 0x26, 0x1c, 0x1a, 0x1c,
	]),
	'UndergroundMusData': bytes([
		0x82, 0x14, 0x2c, 0x62, 0x26, 0x10, 0x28, 0x80, 0x04,
		0x82, 0x14, 0x2c, 0x62, 0x26, 0x10, 0x28, 0x80, 0x04,
		0x82, 0x08, 0x1e, 0x5e, 0x18, 0x60, 0x1a, 0x80, 0x04,
		0x82, 0x08, 0x1e, 0x5e, 0x18, 0x60, 0x1a, 0x86, 0x04,
		0x83, 0x1a, 0x18, 0x16, 0x84, 0x14, 0x1a, 0x18, 0x0e, 0x0c,
		0x16, 0x83, 0x14, 0x20, 0x1e, 0x1c, 0x28, 0x26, 0x87,
		0x24, 0x1a, 0x12, 0x10, 0x62, 0x0e, 0x80, 0x04, 0x04, 0x00,
	]),
	'GroundM_P1Data': bytes([
		0x85, 0x2c, 0x22, 0x1c, 0x84, 0x26, 0x2a, 0x82, 0x28, 0x26, 0x04,
		0x87, 0x22, 0x34, 0x3a, 0x82, 0x40, 0x04, 0x36, 0x84, 0x3a, 0x34,
		0x82, 0x2c, 0x30, 0x85, 0x2a, 0x00,
		0x5d, 0x55, 0x4d, 0x15, 0x19, 0x96, 0x15, 0xd5, 0xe3, 0xeb,
		0x2d, 0xa6, 0x2b, 0x27, 0x9c, 0x9e, 0x59,
		0x85, 0x22, 0x1c, 0x14, 0x84, 0x1e, 0x22, 0x82, 0x20, 0x1e, 0x04, 0x87,
		0x1c, 0x2c, 0x34, 0x82, 0x36, 0x04, 0x30, 0x34, 0x04, 0x2c, 0x04, 0x26, 0x2a, 0x85, 0x22,
		0x21, 0xd0, 0xc4, 0xd0, 0x31, 0xd0, 0xc4, 0xd0, 0x00,
	]),
	'GroundMLdInData': bytes([
		0x82, 0x34, 0x84, 0x34, 0x34, 0x82, 0x2c, 0x84, 0x34, 0x86, 0x3a, 0x04, 0x00,
		0xa0, 0x21, 0x21, 0xa0, 0x21, 0x2b, 0x05, 0xa3,
		0x82, 0x18, 0x84, 0x18, 0x18, 0x82, 0x18, 0x18, 0x04, 0x86, 0x3a, 0x22,
		0x31, 0x90, 0x31, 0x90, 0x31, 0x71, 0x31, 0x90, 0x90, 0x90, 0x00,
	]),
}
_SMB_MUSIC_HEADERS = {
	'castle': (0x00, 0x62, 0x93, 0x00, 'CastleMusData'),
	'under': (0x18, 0x00, 0x00, 0x00, 'UndergroundMusData'),
	'ground_p1': (0x18, 0x1c, 0x2d, 0xb8, 'GroundM_P1Data'),
	'ground_leadin': (0x18, 0x0d, 0x15, 0x21, 'GroundMLdInData'),
}
_SMB_GROUND_ORDER = ['ground_leadin', 'ground_p1', 'ground_p1']


def _smb_note_hz(note_idx):
	if note_idx <= 0 or note_idx >= len(_SMB_FREQ_TBL) - 1:
		return None
	hi, lo = _SMB_FREQ_TBL[note_idx], _SMB_FREQ_TBL[note_idx + 1]
	if lo == 0:
		return None
	period = ((hi & 0x07) << 8) | lo
	return _SMB_NTSC / (16 * (period + 1))


def _smb_note_duty(note_idx):
	if note_idx <= 0 or note_idx >= len(_SMB_FREQ_TBL) - 1:
		return 0.125
	return _SMB_DUTY_FROM_HI[(_SMB_FREQ_TBL[note_idx] >> 5) & 0x03]


def _smb_length_frames(length_byte, len_ofs, adder=0):
	idx = (length_byte & 0x07) + len_ofs + adder
	if idx >= len(_SMB_LEN_TBL):
		idx = min(len_ofs, len(_SMB_LEN_TBL) - 1)
	return _SMB_LEN_TBL[idx]


def _smb_sq1_length(byte_val, len_ofs, adder=0):
	original = byte_val & 0xFF
	carry = original & 1
	a = original
	for _ in range(3):
		new_carry = (a >> 7) & 1
		a = ((a << 1) | carry) & 0xFF
		carry = new_carry
	return _smb_length_frames(a, len_ofs, adder)


def _smb_decode_uncompressed(data, len_ofs):
	events, pending_len = [], None
	for b in data:
		if b == 0:
			break
		if b & 0x80:
			pending_len = _smb_length_frames(b, len_ofs)
			continue
		ln = pending_len if pending_len is not None else _SMB_LEN_TBL[min(len_ofs, len(_SMB_LEN_TBL) - 1)]
		pending_len = None
		events.append((_smb_note_hz(b), _smb_note_duty(b), ln))
	return events


def _smb_decode_compressed(data, len_ofs):
	events = []
	for b in data:
		if b == 0:
			break
		note = b & 0x3E
		events.append((_smb_note_hz(note), _smb_note_duty(note), _smb_sq1_length(b, len_ofs)))
	return events


def _smb_decode_noise(data, len_ofs):
	events = []
	for b in data:
		if b == 0:
			break
		events.append(((b >> 4) & 0x03, _smb_sq1_length(b, len_ofs)))
	return events


def _smb_slice_channels(blob, tri_ofs, sq1_ofs, noise_ofs):
	end_sq2 = blob.find(b'\x00')
	if end_sq2 < 0:
		end_sq2 = len(blob)
	sq2 = blob[:end_sq2]
	sq1 = blob[sq1_ofs:tri_ofs] if sq1_ofs and tri_ofs and sq1_ofs < tri_ofs else b''
	if tri_ofs and noise_ofs and noise_ofs > tri_ofs:
		tri = blob[tri_ofs:noise_ofs]
	elif tri_ofs:
		tri = blob[tri_ofs:]
	else:
		tri = b''
	noise = b''
	if noise_ofs and noise_ofs < len(blob):
		end = blob.find(b'\x00', noise_ofs)
		noise = blob[noise_ofs:end if end >= 0 else len(blob)]
	return sq2, sq1, tri, noise


def _smb_decode_header(header_key):
	len_ofs, sq1_ofs, tri_ofs, noise_ofs, data_key = _SMB_MUSIC_HEADERS[header_key]
	blob = _SMB_ROM[data_key]
	sq2_raw, sq1_raw, tri_raw, noise_raw = _smb_slice_channels(blob, tri_ofs, sq1_ofs, noise_ofs)
	if header_key == 'under':
		tri_raw, sq1_raw, noise_raw = sq2_raw, b'', b''
	return (
		_smb_decode_uncompressed(sq2_raw, len_ofs),
		_smb_decode_compressed(sq1_raw, len_ofs) if sq1_raw else [],
		_smb_decode_uncompressed(tri_raw, len_ofs) if tri_raw else [],
		_smb_decode_noise(noise_raw, len_ofs) if noise_raw else [],
	)


def _smb_concat_events(lists):
	out = []
	for lst in lists:
		out.extend(lst)
	return out


def _smb_expand_voice(events, total_frames):
	seq = []
	for hz, duty, ln in events:
		seq.extend([(hz, duty)] * ln)
	if len(seq) < total_frames:
		seq.extend([(None, 0.125)] * (total_frames - len(seq)))
	return seq[:total_frames]


def _smb_apu_pulse(phase, duty):
	return 1.0 if phase < duty else -1.0


def _smb_apu_triangle(phase):
	p = phase % 1.0
	if p < 0.25:
		return -1.0 + 4.0 * p
	if p < 0.75:
		return 1.0 - 4.0 * (p - 0.25)
	return -1.0 + 4.0 * (p - 0.75)


def _smb_render_track(sq2_events, sq1_events, tri_events, noise_events=None, sr=_SMB_MUSIC_SR):
	def _voice_len(ev):
		return sum(ln for *_, ln in ev) if ev else 0

	rng = random.Random(0x534D4231)
	total_frames = max(_voice_len(sq2_events), _voice_len(sq1_events), _voice_len(tri_events), 1)
	if noise_events:
		total_frames = max(total_frames, sum(ln for _, ln in noise_events))
	sq2 = _smb_expand_voice(sq2_events, total_frames)
	sq1 = _smb_expand_voice(sq1_events, total_frames)
	tri = _smb_expand_voice(tri_events, total_frames)
	noise = None
	if noise_events:
		noise = []
		for beat, ln in noise_events:
			noise.extend([beat] * ln)
		if len(noise) < total_frames:
			noise.extend([0] * (total_frames - len(noise)))
		noise = noise[:total_frames]
	spf = max(1, sr // FPS)
	mono = array.array('f')
	phases = {'sq2': 0.0, 'sq1': 0.0, 'tri': 0.0}
	prev = {'sq2': None, 'sq1': None, 'tri': None}
	for frame in range(total_frames):
		hz2, duty2 = sq2[frame]
		hz1, duty1 = sq1[frame]
		hzt, dutyt = tri[frame]
		if hz2 != prev['sq2']:
			phases['sq2'] = 0.0
			prev['sq2'] = hz2
		if hz1 != prev['sq1']:
			phases['sq1'] = 0.0
			prev['sq1'] = hz1
		if hzt != prev['tri']:
			phases['tri'] = 0.0
			prev['tri'] = hzt
		beat = noise[frame] if noise else 0
		for _ in range(spf):
			mix = 0.0
			if hz2:
				phases['sq2'] += hz2 / sr
				if phases['sq2'] >= 1.0:
					phases['sq2'] -= 1.0
				mix += _smb_apu_pulse(phases['sq2'], duty2) * 0.36
			if hz1:
				phases['sq1'] += hz1 / sr
				if phases['sq1'] >= 1.0:
					phases['sq1'] -= 1.0
				mix += _smb_apu_pulse(phases['sq1'], duty1) * 0.24
			if hzt:
				phases['tri'] += hzt / sr
				if phases['tri'] >= 1.0:
					phases['tri'] -= 1.0
				mix += _smb_apu_triangle(phases['tri']) * 0.28
			if beat:
				amp = 0.08 if beat == 1 else (0.12 if beat == 2 else 0.06)
				mix += (rng.random() * 2.0 - 1.0) * amp
			mono.append(max(-1.0, min(1.0, mix)))
	out = array.array('h')
	for s in mono:
		out.append(max(-32767, min(32767, int(s * 28000))))
	stereo = array.array('h')
	for s in out:
		stereo.extend((s, s))
	return pygame.mixer.Sound(buffer=stereo.tobytes())


def _smb_build_track(track_id):
	if track_id == 'over':
		sq2, sq1, tri, nz = [], [], [], []
		for key in _SMB_GROUND_ORDER:
			p, h, t, n = _smb_decode_header(key)
			sq2.append(p)
			sq1.append(h)
			tri.append(t)
			nz.append(n)
		return _smb_render_track(_smb_concat_events(sq2), _smb_concat_events(sq1), _smb_concat_events(tri), _smb_concat_events(nz))
	hdr = 'castle' if track_id == 'castle' else 'under'
	sq2, sq1, tri, _nz = _smb_decode_header(hdr)
	return _smb_render_track(sq2, sq1, tri, None)


# Koji Kondo SMB1 (100 BPM, 16ths) — fallback when music/ has no rips (matches common YT uploads)
_NOTE_FREQS = {
	'A3': 220.00, 'Bb3': 233.08, 'B3': 246.94, 'C4': 261.63, 'D4': 293.66, 'E4': 329.63,
	'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'Bb4': 466.16, 'B4': 493.88,
	'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00,
}
_KONDO_OVER = [
	('E5', 1), ('-', 1), ('E5', 1), ('-', 3), ('E5', 1), ('-', 1), ('C5', 1), ('-', 1), ('E5', 1), ('-', 3),
	('G5', 1), ('-', 7), ('G4', 1), ('-', 7),
	('C5', 1), ('-', 3), ('G4', 1), ('-', 3), ('E4', 1), ('-', 3),
	('A4', 1), ('-', 1), ('B4', 1), ('-', 1), ('Bb4', 1), ('-', 1), ('A4', 1), ('-', 3),
	('G4', 1), ('-', 1), ('E5', 1), ('-', 1), ('G5', 1), ('-', 1), ('A5', 1), ('-', 3),
	('F5', 1), ('-', 1), ('G5', 1), ('-', 1), ('E5', 1), ('-', 3), ('C5', 1), ('-', 1),
	('D5', 1), ('-', 1), ('B4', 1), ('-', 5),
]
_KONDO_OVER += _KONDO_OVER[14:]
_KONDO_UNDER = [
	('C5', 1), ('C4', 1), ('A4', 1), ('A3', 1), ('Bb4', 1), ('Bb3', 1), ('-', 10),
	('C5', 1), ('C4', 1), ('A4', 1), ('A3', 1), ('Bb4', 1), ('Bb3', 1), ('-', 10),
]
_KONDO_CASTLE = [
	('A4', 1), ('-', 1), ('A4', 1), ('-', 1), ('A4', 1), ('-', 1), ('A4', 1), ('-', 1),
	('F4', 1), ('-', 1), ('F4', 1), ('-', 1), ('F4', 1), ('-', 1), ('F4', 1), ('-', 1),
	('C5', 1), ('-', 1), ('C5', 1), ('-', 1), ('C5', 1), ('-', 1), ('C5', 1), ('-', 1),
	('E5', 1), ('-', 1), ('E5', 1), ('-', 1), ('E5', 1), ('-', 1), ('E5', 1), ('-', 1),
] * 2
_DUTY_12 = 0.125
_DUTY_25 = 0.25
_DUTY_50 = 0.5
_MUSIC_FILE_NAMES = {
	'over': ('over', 'overworld', 'main', 'ground', '1-1', 'world-1-1', 'yt-over'),
	'under': ('under', 'underground', 'under-world', '1-2', 'yt-under'),
	'castle': ('castle', 'bowser', '8-4', 'fortress', 'yt-castle'),
}


def _apu_pulse(phase, duty):
	return 1.0 if (phase % 1.0) < duty else -1.0


def _apu_quantize(x, steps=16):
	t = max(-1.0, min(1.0, x))
	q = round(t * (steps - 1)) / (steps - 1)
	return int(q * 32767 * 0.85)


def _make_kondo_loop(notes, tempo=100, sr=_SMB_MUSIC_SR):
	sixteenth = (60.0 / tempo) / 4.0
	mono = array.array('h')
	phase = 0.0
	for note, length in notes:
		freq = _NOTE_FREQS.get(note, 0)
		dur = max(1, int(sr * sixteenth * length))
		if freq <= 0:
			mono.extend([0] * dur)
			continue
		inc = freq / sr
		for _ in range(dur):
			phase += inc
			if phase >= 1.0:
				phase -= 1.0
			mono.append(_apu_quantize(_apu_pulse(phase, _DUTY_12) * 0.55))
	stereo = array.array('h')
	for s in mono:
		stereo.extend((s, s))
	return pygame.mixer.Sound(buffer=stereo.tobytes())


def _prebake_all_music():
	"""Fast built-in OST (YouTube-style Kondo loops)."""
	loops = {
		'over': _make_kondo_loop(_KONDO_OVER),
		'under': _make_kondo_loop(_KONDO_UNDER),
		'castle': _make_kondo_loop(_KONDO_CASTLE, tempo=112),
	}
	loops['1-1'] = loops['over']
	loops['8-4'] = loops['castle']
	return loops


def _stereo_sound(mono_samples):
	"""Mono int16 samples → interleaved stereo bytes (pygame mixer is 16-bit stereo)."""
	stereo = array.array('h')
	for s in mono_samples:
		stereo.append(int(s))
		stereo.append(int(s))
	return pygame.mixer.Sound(buffer=stereo.tobytes())


class APU:
	def __init__(self):
		self.enabled = True
		self.music_on = True
		self.sample_rate = 44100
		self.initialized = False
		self._current_track = None
		self._music_loops = {}
		self._music_channel = None
		os.makedirs(_MUSIC_DIR, exist_ok=True)
		self.use_files = self._scan_music_files()
		try:
			pygame.mixer.init(self.sample_rate, -16, 2, 1024)
			pygame.mixer.set_reserved(1)
			self.initialized = True
			self._music_channel = pygame.mixer.Channel(0)
		except Exception:
			pass
		self.sounds = {}
		if self.initialized:
			self._prebake_sfx()
			if not self.use_files:
				self._prebake_music()

	def _scan_music_files(self):
		"""Auto ON when music/ contains YouTube-style rips (over.mp3, under.ogg, etc.)."""
		for track in ('over', 'under', 'castle'):
			if self._resolve_music_path(track):
				return True
		return False

	def _resolve_music_path(self, track_id):
		names = _MUSIC_FILE_NAMES.get(track_id, (track_id,))
		for name in names:
			for ext in ('.ogg', '.mp3', '.wav', '.flac', '.m4a'):
				path = os.path.join(_MUSIC_DIR, name + ext)
				if os.path.isfile(path):
					return path
		return None

	def _prebake_sfx(self):
		"""SMB1-style 2A03 SFX (pulse + LFSR noise), baked once."""
		random.seed(0x534D4231)
		self.sounds['jump'] = self._sfx([(0.0, 520), (0.05, 720), (0.10, 900)], 0.18, _DUTY_12)
		self.sounds['jump_big'] = self._sfx([(0.0, 420), (0.05, 640), (0.12, 860), (0.18, 1020)], 0.22, _DUTY_12)
		self.sounds['coin'] = self._sfx([(0.0, 988), (0.04, 1318)], 0.18, _DUTY_50)
		self.sounds['stomp'] = self._sfx([(0.0, 180), (0.05, 90)], 0.10, _DUTY_25)
		self.sounds['bump'] = self._sfx([(0.0, 260), (0.05, 160)], 0.10, _DUTY_25)
		self.sounds['break'] = self._sfx_noise(0.15, 0.24, short=True)
		self.sounds['powerup'] = self._sfx([(0.0, 523), (0.05, 659), (0.10, 784), (0.15, 1047), (0.20, 1318)], 0.30, _DUTY_25)
		self.sounds['die'] = self._sfx([(0.0, 196), (0.10, 233), (0.20, 165), (0.30, 98)], 0.80, _DUTY_12)
		self.sounds['fireball'] = self._sfx([(0.0, 880), (0.04, 440)], 0.10, _DUTY_25)
		self.sounds['flagpole'] = self._sfx([(0.0, 659), (0.06, 523), (0.12, 440), (0.20, 587), (0.28, 523)], 0.50, _DUTY_25)
		self.sounds['shrink'] = self._sfx([(0.0, 500), (0.15, 150)], 0.40, _DUTY_12)
		self.sounds['1up'] = self._sfx([(0.0, 1318), (0.06, 1568), (0.12, 1976), (0.18, 2637)], 0.32, _DUTY_50)
		self.sounds['bowser_fall'] = self._sfx([(0.0, 200), (0.15, 120), (0.30, 80), (0.50, 50)], 0.70, _DUTY_12)
		self.sounds['warning'] = self._sfx([(0.0, 988)], 0.10, _DUTY_50)

	def _prebake_music(self):
		self._music_loops = _prebake_all_music()

	def _music_file_path(self, track_id):
		if not self.use_files:
			return None
		return self._resolve_music_path(track_id)

	def _sfx(self, freq_list, duration, duty=_DUTY_12, vol=0.22):
		n = int(self.sample_rate * duration)
		buf = array.array('h', [0] * n)
		phase = 0.0
		for i in range(n):
			t = i / self.sample_rate
			f = freq_list[0][1]
			for st, fr in freq_list:
				if t >= st:
					f = fr
			phase += f / self.sample_rate
			phase %= 1.0
			v = _apu_pulse(phase, duty) * vol
			env = 1.0
			if t < 0.01:
				env = t / 0.01
			if t > duration - 0.05:
				env = max(0.0, (duration - t) / 0.05)
			buf[i] = _apu_quantize(v * env)
		return _stereo_sound(buf)

	def _sfx_noise(self, duration, vol=0.2, freq=8000, short=False):
		n = int(self.sample_rate * duration)
		buf = array.array('h', [0] * n)
		reg = 1
		period = max(2, int(self.sample_rate / freq))
		timer = 0
		for i in range(n):
			timer -= 1
			if timer <= 0:
				timer = period
				b0 = reg & 1
				tap = (reg >> (6 if short else 1)) & 1
				reg = (reg >> 1) | ((b0 ^ tap) << 14)
				reg &= 0x7FFF
			bit = reg & 1
			v = vol if bit == 0 else -vol
			t = i / self.sample_rate
			env = 1.0
			if t < 0.005:
				env = t / 0.005
			if t > duration - 0.05:
				env = max(0.0, (duration - t) / 0.05)
			buf[i] = _apu_quantize(v * env)
		return _stereo_sound(buf)

	def stop_music(self):
		if not self.initialized:
			return
		pygame.mixer.music.stop()
		if self._music_channel:
			self._music_channel.stop()
		self._current_track = None

	def toggle_music(self):
		self.music_on = not self.music_on
		if not self.music_on:
			self.stop_music()
		return self.music_on

	def toggle_music_files(self):
		"""Toggle YouTube/file OST (music/over.*). Off = built-in Kondo loops."""
		self.use_files = not self.use_files
		self._current_track = None
		if self.use_files:
			self._music_loops = {}
		elif self.initialized and not self._music_loops:
			self._prebake_music()
		return self.use_files

	def _track_for_level(self, level_type):
		if level_type == 'castle':
			return 'castle'
		if level_type == 'underground':
			return 'under'
		return 'over'

	def update_music(self, level_type='overworld', game_state='menu'):
		if not self.initialized or not self.enabled or not self.music_on:
			self.stop_music()
			return
		if game_state != 'playing':
			self.stop_music()
			return
		track = self._track_for_level(level_type)
		if track == self._current_track:
			return
		self.stop_music()
		self._current_track = track
		path = self._music_file_path(track)
		if path:
			try:
				pygame.mixer.music.load(path)
				pygame.mixer.music.set_volume(0.48)
				pygame.mixer.music.play(-1)
				return
			except Exception:
				pass
		if not self._music_loops:
			self._prebake_music()
		snd = self._music_loops.get(track)
		if snd and self._music_channel:
			snd.set_volume(0.48)
			self._music_channel.play(snd, loops=-1)

	def play(self, name):
		if self.enabled and self.initialized and name in self.sounds:
			ch = pygame.mixer.find_channel(True)
			if ch and ch != self._music_channel:
				self.sounds[name].set_volume(0.5)
				ch.play(self.sounds[name])


# SMB1 Mario spritesheet (16x16 small / 16x32 big), transparent PNG — embedded from assets/
_SMB1_SHEET_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAG4AAABqCAYAAABdymTtAAAFBUlEQVR4nO2dS27bMBCGySBAfJ920d4lF6jRRbKqj+Dssih8gt6lWfRAzkrFOKFB03zMkENKSv4PCJzo8Xs4JEVK1EyMAQCMw6Z2HL+ZKdy2eUkfDx0z1D82J3b3903TWkvbxOLQ6eef29jGZ3fyozW/7g9m/2DM3f3hTfzrlt2qoNPPP1c79w9mIpGnP9uTmCP8uyQOHdPVPze5WgXLJdrj6DOsdWoJPrvn/BgHHdPVP0nx6d/harZzPkkwzkGnj39srjU8vFwOoqVe9ll0tPRazr9NiaWmr1zxUTob5r2Tlj0lLV8vp9VqT3KM83EtwsFx1gidjeCGV8se/9Lmj0ehVsnxWvZcGOaMI3Gqff/u3t8/t87E1Ai1WuwJ9Xwt9+O0cnqt/rmqUf9gGhzDRzLUCsJjUob11tkwNUKd15+XMzeJTkisXJzzWv1zUzWjERSst44VaGjquJ5Cl0T6IUfTJ20rjYHc7xXPKkPj3O/+9Tq1XarDIXfuXtkOrl5YOXRsbFvJnpRWyZ5biWDuuNoZFEdbS3cv0Co5Pba/9rYiVukpG2u/AwAAPiHp6fM0XV1zLa30CYFOH//YnNjT49vu3fNpm1gcOmP8cyZ8CuA/DWCLQKern69qk06++304PV2gT0f4d+kGETqmq3+wAr5Soj2OPsNajz3fywlDx3T1D1bAV7qyz3qv8vW7rXrh86PqaOm1nH/DebPWn76G60Ylo3rrGCZa9jgtjl5Pe5JjnI9rEZJ7ixE6VnCPo2VPal0v1Cr1Hi17Lgxzxp3uK96J7Z9bZ6pcAW+xJ9Tztc4IV8Br7CmugIeXI2oFNSvXPXQsUyPUMV9+XOyT6FzpRsrFOq/RP1gBb1gBp55Cl0T6IUfTp2Ss7LoCHr7jUdou1eGQO/eobAdXL/aOSO37J7nzUvZkV8AlsyxJISXkzj0KdSVaJafH9tfeVsQqPWVj7XcAAAAAa6Fq1kMgkF/fPxLY02cE8vf1j5Ts7QCBAPwx/pFSjE1DIP/W9vZPDXh1YaWwokERyN/XPzWIn2Svebl/6ToSRA9lzwNxRSuCji7ZMS734DMW/gqdOv90n5yEweW1QKcdy7l2uxjl2KXSP2YNOlMwHoUTCX+yURqftMql2uNK71+EEZSp45emY5UcqGVP90ul35p843xHcIxbgo7NVB71FNovrWCtcnGpeudEcs7SdPx9Lfdb2vaoPqvkflExKebCdFLB89Lg+F72dHnkRQVrTVrmNDSeKOwqdVJZDloyRLTY06XiNFJWlI6TOGzfaI+2LX6DbNFSXdZZGhr5QHaKOUrmotjjRrZgqc5uZmdrlQsAAAAAAAAAAAAAAAAAAAB8WHixA0isPcQ/EpAQ+3EZCcPVQWLtMf6RUkw/i8Ta2+4Jw2tAROpKQULsBSQMrwERqR81ItWf6rp0tTWtCDq6ZMe4XLLqWDpa6NT5p/vkJEz2XAt02mFHXFLLiV0qpZGkc+tMwXgUTiT8yYYkIrWlXEMjUsOg9NpI0tE6dlBEKtee7pdKvzX5xkkjLpegYzOVRz2lJiJVq1xcPnVE6mvD/dbcEalsoVS+jpaM5nPrHN81/GTWrf9np8Wero+8yJDWwjkNjUJtKnVSjm5NKKNVLpWK00gh3/JPgrTtOSrbkuutvTILrS4iVSM//0bxfwbMRbHHjWzBUp3NzM7WKhcAAAAAAAAAAAAAAAAAAIAp8h/srPnKr2s8EAAAAABJRU5ErkJggg=="
)

class SMB1SpriteBank:
    """NES SMB1 Mario — all frames pre-baked (scaled + flipped) at load; draw is blit-only."""

    _SMALL_FRAMES = ('idle', 'walk1', 'walk2', 'walk3', 'jump', 'skid')
    _BIG_FRAMES = ('idle', 'walk1', 'walk2', 'jump', 'skid')
    _SCALE = TILE // 16

    def __init__(self):
        if pygame.display.get_surface() is None:
            pygame.display.set_mode((8, 8), pygame.HIDDEN)
        raw = base64.standard_b64decode(_SMB1_SHEET_B64)
        sheet = pygame.image.load(io.BytesIO(raw)).convert_alpha()
        self._baked = {}
        self._y_offset = {False: 0, True: TILE * 2}  # filled per sprite height below
        for big, fire, names, y0, fh in (
            (False, False, self._SMALL_FRAMES, 2, 16),
            (False, True, self._SMALL_FRAMES, 20, 16),
            (True, False, self._BIG_FRAMES, 38, 32),
            (True, True, self._BIG_FRAMES, 72, 32),
        ):
            for i, name in enumerate(names):
                x0 = 2 + i * 18
                src = sheet.subsurface(pygame.Rect(x0, y0, 16, fh)).copy()
                w = max(1, src.get_width() * self._SCALE)
                h = max(1, src.get_height() * self._SCALE)
                scaled_r = pygame.transform.scale(src, (w, h))
                scaled_l = pygame.transform.flip(scaled_r, True, False)
                self._baked[(big, fire, name, 1)] = scaled_r
                self._baked[(big, fire, name, -1)] = scaled_l
                if big:
                    self._y_offset[True] = TILE * 2 - h
                else:
                    self._y_offset[False] = 0

    def _anim_name(self, state, frame, big):
        if state == 'jump':
            return 'jump'
        if state == 'skid':
            return 'skid'
        if state == 'walk':
            names = self._BIG_FRAMES if big else self._SMALL_FRAMES
            walks = [n for n in names if n.startswith('walk')]
            return walks[int(frame) % len(walks)]
        return 'idle'

    def get(self, state, frame, big, fire, facing):
        name = self._anim_name(state, frame, big)
        key = (big, fire, name, facing)
        sprite = self._baked.get(key)
        if sprite is None:
            sprite = self._baked[(big, fire, 'idle', facing)]
        return sprite, self._y_offset[big]


_SMB1_SPRITES = None

def _smb1_sprites():
    global _SMB1_SPRITES
    if _SMB1_SPRITES is None:
        _SMB1_SPRITES = SMB1SpriteBank()
    return _SMB1_SPRITES

def draw_mario(surf, x, y, state, frame, facing, big=False, fire=False):
    sprite, y_off = _smb1_sprites().get(state, frame, big, fire, facing)
    surf.blit(sprite, (int(x) + 6, int(y) + y_off))

def draw_goomba(surf, x, y, frame):
    rx, ry = int(x), int(y)
    step = int(frame * 0.2) % 2
    pygame.draw.ellipse(surf, C_GOOMBA, (rx + 2, ry + 8, TILE - 4, TILE - 10))
    pygame.draw.rect(surf, C_BLACK, (rx + 6, ry + 12, 10, 3))
    pygame.draw.rect(surf, C_BLACK, (rx + 24, ry + 12, 10, 3))
    pygame.draw.rect(surf, C_WHITE, (rx + 8, ry + 14, 8, 10))
    pygame.draw.rect(surf, C_WHITE, (rx + 24, ry + 14, 8, 10))
    pygame.draw.rect(surf, C_BLACK, (rx + 10, ry + 18, 4, 4))
    pygame.draw.rect(surf, C_BLACK, (rx + 26, ry + 18, 4, 4))
    if step == 0:
        pygame.draw.rect(surf, C_BLACK, (rx + 2, ry + 36, 14, 10))
        pygame.draw.rect(surf, C_BLACK, (rx + 24, ry + 36, 14, 10))
    else:
        pygame.draw.rect(surf, C_BLACK, (rx + 6, ry + 38, 14, 8))
        pygame.draw.rect(surf, C_BLACK, (rx + 20, ry + 38, 14, 8))

def draw_koopa(surf, x, y, frame, facing):
    rx, ry = int(x), int(y)
    step = int(frame * 0.2) % 2
    flip = facing < 0
    head_x = rx + 4 if flip else rx + 24
    pygame.draw.rect(surf, C_KOOPA_GREEN, (head_x, ry, 12, 12))
    pygame.draw.rect(surf, C_WHITE, (head_x + 2, ry + 2, 6, 6))
    pygame.draw.rect(surf, C_BLACK, (head_x + 4, ry + 4, 3, 3))
    pygame.draw.rect(surf, C_KOOPA_GREEN, (rx + 8, ry + 12, 24, 26))
    pygame.draw.rect(surf, C_WHITE, (rx + 10, ry + 14, 20, 22), 2)
    lx = rx + 8 if step else rx + 4
    pygame.draw.rect(surf, C_KOOPA_GREEN, (lx, ry + 34, 8, 10))
    pygame.draw.rect(surf, C_KOOPA_GREEN, (lx + 16, ry + 34, 8, 10))

def draw_bowser(surf, x, y, frame):
    rx, ry = int(x), int(y)
    pygame.draw.rect(surf, C_BOWSER_GREEN, (rx, ry + 10, 56, 50))
    pygame.draw.rect(surf, C_BOWSER_GREEN, (rx + 8, ry, 40, 16))
    for i in range(4):
        sx = rx + 12 + i * 10
        pygame.draw.polygon(surf, C_WHITE, [(sx, ry), (sx + 5, ry - 8), (sx + 10, ry)])
    pygame.draw.rect(surf, C_BOWSER_BELLY, (rx + 6, ry + 20, 24, 30))
    pygame.draw.rect(surf, C_BOWSER_GREEN, (rx + 40, ry + 4, 24, 24))
    pygame.draw.rect(surf, C_WHITE, (rx + 48, ry + 8, 8, 8))
    pygame.draw.rect(surf, C_MARIO_RED, (rx + 52, ry + 10, 4, 4))
    pygame.draw.polygon(surf, C_WHITE, [(rx + 44, ry + 4), (rx + 40, ry - 8), (rx + 48, ry + 4)])
    pygame.draw.polygon(surf, C_WHITE, [(rx + 56, ry + 4), (rx + 60, ry - 8), (rx + 64, ry + 4)])
    if int(frame * 0.05) % 2:
        pygame.draw.rect(surf, C_MARIO_RED, (rx + 52, ry + 20, 12, 6))
    step = int(frame * 0.1) % 2
    lx = rx + 4 if step else rx + 8
    pygame.draw.rect(surf, C_BOWSER_GREEN, (lx, ry + 56, 14, 12))
    pygame.draw.rect(surf, C_BOWSER_GREEN, (lx + 24, ry + 56, 14, 12))
    pygame.draw.rect(surf, C_BOWSER_GREEN, (rx - 8, ry + 40, 14, 8))
    pygame.draw.polygon(surf, C_BOWSER_GREEN, [(rx - 8, ry + 40), (rx - 16, ry + 36), (rx - 8, ry + 48)])

def draw_block(surf, x, y, type_name, frame=0, underground=False):
    brick_c = C_BRICK_UNDER if underground else C_BRICK
    brick_d = C_BRICK_UNDER_D if underground else C_BRICK_DARK
    if type_name == 'ground':
        pygame.draw.rect(surf, brick_c, (x, y, TILE, TILE))
        pygame.draw.rect(surf, brick_d, (x, y, TILE, TILE), 2)
        pygame.draw.line(surf, brick_d, (x, y + TILE // 2), (x + TILE, y + TILE // 2), 2)
        pygame.draw.line(surf, brick_d, (x + TILE // 2, y), (x + TILE // 2, y + TILE), 2)
    elif type_name == 'brick':
        pygame.draw.rect(surf, brick_c, (x, y, TILE, TILE))
        pygame.draw.rect(surf, brick_d, (x, y, TILE, TILE), 2)
        pygame.draw.line(surf, brick_d, (x, y + TILE // 2), (x + TILE, y + TILE // 2), 3)
        pygame.draw.line(surf, brick_d, (x + TILE // 2, y), (x + TILE // 2, y + TILE // 2), 3)
        pygame.draw.line(surf, brick_d, (x + TILE // 4, y + TILE // 2), (x + TILE // 4, y + TILE), 3)
        pygame.draw.line(surf, brick_d, (x + 3 * TILE // 4, y + TILE // 2), (x + 3 * TILE // 4, y + TILE), 3)
    elif type_name == 'q_block':
        color = C_QUESTION_HIT if frame == -1 else C_QUESTION
        pygame.draw.rect(surf, color, (x, y, TILE, TILE))
        pygame.draw.rect(surf, C_BLACK, (x, y, TILE, TILE), 2)
        if frame != -1:
            pygame.draw.rect(surf, (200, 100, 0), (x + 4, y + 4, 4, 4))
            pygame.draw.rect(surf, (200, 100, 0), (x + 36, y + 4, 4, 4))
            pygame.draw.rect(surf, (200, 100, 0), (x + 4, y + 36, 4, 4))
            pygame.draw.rect(surf, (200, 100, 0), (x + 36, y + 36, 4, 4))
            qm_y = y + 10 + int(math.sin(frame * 0.15) * 2)
            pygame.draw.rect(surf, (255, 230, 200), (x + 16, qm_y, 12, 4))
            pygame.draw.rect(surf, (255, 230, 200), (x + 24, qm_y + 4, 4, 8))
            pygame.draw.rect(surf, (255, 230, 200), (x + 16, qm_y + 12, 12, 4))
            pygame.draw.rect(surf, (255, 230, 200), (x + 16, qm_y + 16, 4, 4))
            pygame.draw.rect(surf, (255, 230, 200), (x + 20, qm_y + 24, 4, 4))
    elif type_name == 'hard':
        pygame.draw.rect(surf, C_CASTLE_GRAY, (x, y, TILE, TILE))
        pygame.draw.rect(surf, C_CASTLE_DARK, (x, y, TILE, TILE), 3)
        pygame.draw.line(surf, C_CASTLE_DARK, (x, y + TILE // 2), (x + TILE, y + TILE // 2), 2)
        pygame.draw.line(surf, C_CASTLE_DARK, (x + TILE // 2, y), (x + TILE // 2, y + TILE), 2)

def draw_pipe(surf, x, y, w, h):
    lip_h = 12
    body_x = x + 4
    body_w = w - 8
    pygame.draw.rect(surf, C_PIPE_BASE, (body_x, y + lip_h, body_w, h - lip_h))
    pygame.draw.rect(surf, C_PIPE_DARK, (body_x, y + lip_h, 6, h - lip_h))
    pygame.draw.rect(surf, C_PIPE_SHADE, (body_x + body_w - 6, y + lip_h, 6, h - lip_h))
    pygame.draw.rect(surf, (210, 255, 80), (body_x + body_w // 2 - 2, y + lip_h, 4, h - lip_h))
    pygame.draw.rect(surf, C_PIPE_BASE, (x, y, w, lip_h))
    pygame.draw.rect(surf, C_PIPE_DARK, (x, y, w, lip_h), 3)
    pygame.draw.rect(surf, (210, 255, 80), (x + w // 2 - 2, y, 4, lip_h))

def draw_scenery(surf, x, y, type_name):
    if type_name == 'bush':
        pygame.draw.ellipse(surf, C_GROUND_GREEN, (x, y, 60, 20))
        pygame.draw.ellipse(surf, C_GROUND_GREEN, (x + 20, y - 10, 40, 20))
        pygame.draw.ellipse(surf, C_GROUND_GREEN, (x + 40, y, 60, 20))
    elif type_name == 'cloud':
        pygame.draw.ellipse(surf, C_WHITE, (x, y, 50, 30))
        pygame.draw.ellipse(surf, C_WHITE, (x + 25, y - 10, 40, 30))
        pygame.draw.ellipse(surf, C_WHITE, (x + 45, y, 50, 30))
    elif type_name == 'hill':
        pts = [(x, y + 60), (x + 40, y), (x + 80, y + 60)]
        pygame.draw.polygon(surf, C_GROUND_GREEN, pts)
        pygame.draw.polygon(surf, (0, 140, 0), pts, 3)
    elif type_name == 'mushroom_tree':
        pygame.draw.rect(surf, C_TREE_BROWN, (x + 20, y, 8, 40))
        pygame.draw.ellipse(surf, C_MARIO_RED, (x, y - 16, 48, 24))
        pygame.draw.ellipse(surf, C_WHITE, (x + 8, y - 10, 10, 10))
        pygame.draw.ellipse(surf, C_WHITE, (x + 28, y - 10, 10, 10))

def draw_castle(surf, x, y):
    pygame.draw.rect(surf, C_CASTLE_GRAY, (x, y, 150, 150))
    pygame.draw.rect(surf, C_CASTLE_DARK, (x + 60, y + 80, 30, 70))
    pygame.draw.circle(surf, C_CASTLE_DARK, (x + 75, y + 80), 15)
    for i in range(5):
        pygame.draw.rect(surf, C_CASTLE_GRAY, (x + i * 30, y - 20, 15, 20))

def draw_flagpole(surf, x, ground_y):
    pole_x = x + TILE // 2 - 2
    top_y = ground_y - TILE * 8
    pygame.draw.rect(surf, C_WHITE, (pole_x, top_y, 4, ground_y - top_y))
    pygame.draw.circle(surf, C_COIN_GOLD, (pole_x + 2, top_y), 8)
    flag_pts = [(pole_x, top_y + 16), (pole_x - 28, top_y + 30), (pole_x, top_y + 44)]
    pygame.draw.polygon(surf, C_GROUND_GREEN, flag_pts)

def draw_axe(surf, x, y, frame):
    bob = int(math.sin(frame * 0.15) * 3)
    pygame.draw.rect(surf, C_BRIDGE, (x + 12, y + 10 + bob, 6, 24))
    pygame.draw.polygon(
        surf,
        C_AXE_GRAY,
        [(x + 4, y + bob), (x + 18, y + 4 + bob), (x + 18, y + 16 + bob), (x + 4, y + 20 + bob)],
    )
    pygame.draw.line(surf, C_WHITE, (x + 4, y + 2 + bob), (x + 4, y + 18 + bob), 2)

class LevelData:
    def __init__(self, world, level):
        self.world = world
        self.level = level
        self.tiles = [[0] * LEVEL_WIDTH_TILES for _ in range(LEVEL_HEIGHT_TILES)]
        self.enemies = []
        self.blocks = {}
        self.decor = []
        self.pipes = []
        self.bowser = None
        self.axe_x = 0
        self.bridge_tiles = []
        self.lava_ranges = []
        self.has_flag = True
        self.flag_x = (LEVEL_WIDTH_TILES - 12) * TILE
        self.castle_x = (LEVEL_WIDTH_TILES - 5) * TILE

        if level == 1:
            self.level_type = 'overworld'
        elif level == 2:
            self.level_type = 'underground'
        elif level == 3:
            self.level_type = 'athletic'
        else:
            self.level_type = 'castle'

        self.underground = self.level_type in ('underground', 'castle')
        self.difficulty = world
        self.time = max(250, 400 - (world - 1) * 15)
        self.generate()

    def generate(self):
        random.seed(self.world * 100 + self.level * 7 + 42)
        if self.level_type == 'overworld':
            self._gen_overworld()
        elif self.level_type == 'underground':
            self._gen_underground()
        elif self.level_type == 'athletic':
            self._gen_athletic()
        else:
            self._gen_castle()

    def _ground_row(self):
        return LEVEL_HEIGHT_TILES - 2

    def _fill_ground(self, start=0, end=None):
        gy = self._ground_row()
        if end is None:
            end = LEVEL_WIDTH_TILES
        for x in range(start, min(end, LEVEL_WIDTH_TILES)):
            self.tiles[gy][x] = 1
            self.tiles[gy + 1][x] = 1

    def _place_pipe(self, px, gy):
        if px + 1 >= LEVEL_WIDTH_TILES:
            return False
        if self.tiles[gy][px] != 1 or self.tiles[gy][px + 1] != 1:
            return False
        top = gy - 2
        for r in range(top, gy):
            if r < 0 or self.tiles[r][px] != 0 or self.tiles[r][px + 1] != 0:
                return False
        self.pipes.append((px, top, 2))
        for r in range(top, gy):
            self.tiles[r][px] = 9
            self.tiles[r][px + 1] = 9
        return True

    def _place_gap(self, gx, gw, gy):
        for i in range(gw):
            if 0 <= gx + i < LEVEL_WIDTH_TILES:
                self.tiles[gy][gx + i] = 0
                self.tiles[gy + 1][gx + i] = 0

    def _place_q_block(self, x, y, content=CONTENTS_COIN):
        if 0 <= x < LEVEL_WIDTH_TILES and 0 <= y < LEVEL_HEIGHT_TILES:
            self.tiles[y][x] = 3
            self.blocks[(x, y)] = content

    def _place_brick(self, x, y):
        if 0 <= x < LEVEL_WIDTH_TILES and 0 <= y < LEVEL_HEIGHT_TILES:
            self.tiles[y][x] = 2

    def _place_hard(self, x, y):
        if 0 <= x < LEVEL_WIDTH_TILES and 0 <= y < LEVEL_HEIGHT_TILES:
            self.tiles[y][x] = 4

    def _add_enemy(self, x, y, etype='goomba'):
        spd = ENEMY_SPEED + (self.difficulty - 1) * 0.15
        self.enemies.append(
            {'type': etype, 'x': x * TILE, 'y': y * TILE, 'vx': -spd, 'vy': 0, 'alive': True, 'frame': 0, 'facing': -1}
        )

    def _add_scenery(self, gy):
        step = 5
        while step < LEVEL_WIDTH_TILES:
            if random.random() < 0.5:
                self.decor.append(('cloud', step * TILE, random.randint(40, 140)))
            if random.random() < 0.4:
                self.decor.append(('bush', step * TILE, (gy - 1) * TILE + 24))
            if random.random() < 0.25:
                self.decor.append(('hill', step * TILE, (gy - 1) * TILE - 10))
            step += random.randint(8, 14)

    def _gen_overworld(self):
        gy = self._ground_row()
        self._fill_ground(0, LEVEL_WIDTH_TILES - 10)
        self._fill_ground(LEVEL_WIDTH_TILES - 8)

        num_gaps = min(2 + self.difficulty, 8)
        gap_x = 30
        for _ in range(num_gaps):
            gap_x += random.randint(12, max(14, 35 - self.difficulty * 2))
            if gap_x > LEVEL_WIDTH_TILES - 45:
                break
            gw = random.randint(2, min(2 + self.difficulty // 3, 4))
            self._place_gap(gap_x, gw, gy)
            gap_x += gw + 5

        px = 28
        while px < LEVEL_WIDTH_TILES - 45:
            px += random.randint(14, 28)
            self._place_pipe(px, gy)

        self._gen_block_formations(gy)
        self._gen_enemies_ground(gy)
        self._add_scenery(gy)

    def _gen_underground(self):
        gy = self._ground_row()
        self._fill_ground()

        ceil_y = 2
        for x in range(LEVEL_WIDTH_TILES):
            self.tiles[ceil_y][x] = 1
            self.tiles[ceil_y - 1][x] = 1
            if x < 8 or x > LEVEL_WIDTH_TILES - 12:
                self.tiles[ceil_y + 1][x] = 1

        if self.difficulty >= 3:
            for sx in range(40, LEVEL_WIDTH_TILES - 50, random.randint(35, 60)):
                sw = random.randint(4, 8)
                for x in range(sx, min(sx + sw, LEVEL_WIDTH_TILES)):
                    self.tiles[ceil_y][x] = 0
                    self.tiles[ceil_y - 1][x] = 0

        for section in range(3 + self.difficulty):
            cx = random.randint(15 + section * 20, 25 + section * 25)
            if cx >= LEVEL_WIDTH_TILES - 30:
                break
            cy = gy - random.randint(2, 4)
            cw = random.randint(4, 8)
            for i in range(cw):
                if cx + i < LEVEL_WIDTH_TILES:
                    self._place_q_block(cx + i, cy, CONTENTS_COIN)

        for section in range(2 + self.difficulty // 2):
            bx = random.randint(20 + section * 30, 40 + section * 30)
            if bx >= LEVEL_WIDTH_TILES - 30:
                break
            bw = random.randint(3, 7)
            by = gy - random.randint(3, 5)
            for i in range(bw):
                self._place_brick(bx + i, by)

        gx = 40
        for _ in range(self.difficulty // 2):
            gx += random.randint(25, 45)
            if gx > LEVEL_WIDTH_TILES - 40:
                break
            self._place_gap(gx, 2, gy)

        if self.difficulty >= 2:
            ppx = 50
            while ppx < LEVEL_WIDTH_TILES - 50:
                ppx += random.randint(30, 50)
                self._place_pipe(ppx, gy)

        self._place_q_block(random.randint(20, 60), gy - 4, CONTENTS_MUSHROOM)
        self._gen_enemies_ground(gy)

    def _gen_athletic(self):
        gy = self._ground_row()
        self._fill_ground(0, 16)
        px = 16
        while px < LEVEL_WIDTH_TILES - 20:
            pw = random.randint(max(3, 7 - self.difficulty // 2), 8)
            target_y = random.randint(max(4, gy - 5 - self.difficulty // 2), gy - 1)
            for i in range(pw):
                if px + i < LEVEL_WIDTH_TILES:
                    self.tiles[target_y][px + i] = 1
            if random.random() < 0.4 + self.difficulty * 0.05:
                etype = 'koopa' if random.random() < 0.4 else 'goomba'
                self._add_enemy(px + pw // 2, target_y - 1, etype)
            if random.random() < 0.3:
                content = CONTENTS_MUSHROOM if random.random() < 0.2 else CONTENTS_COIN
                self._place_q_block(px + pw // 2, target_y - 3, content)
            gap_lo = max(2, 3 - self.difficulty // 4)
            gap_hi = max(gap_lo + 1, min(5, 2 + self.difficulty // 3 + 1))
            px += pw + random.randint(gap_lo, gap_hi)

        for x in range(LEVEL_WIDTH_TILES - 16, LEVEL_WIDTH_TILES):
            self.tiles[gy][x] = 1
            self.tiles[gy + 1][x] = 1

        for x in range(8, LEVEL_WIDTH_TILES, 16):
            if random.random() < 0.3:
                self.decor.append(('mushroom_tree', x * TILE, random.randint(200, 450)))
            if random.random() < 0.5:
                self.decor.append(('cloud', x * TILE, random.randint(30, 120)))

    def _gen_castle(self):
        gy = self._ground_row()
        self.has_flag = False
        for x in range(LEVEL_WIDTH_TILES):
            self.tiles[gy][x] = 4
            self.tiles[gy + 1][x] = 4
            self.tiles[0][x] = 4
            self.tiles[1][x] = 4

        pit_x = 20
        for _ in range(2 + self.difficulty):
            pit_x += random.randint(10, max(12, 30 - self.difficulty * 2))
            if pit_x > LEVEL_WIDTH_TILES - 60:
                break
            pw = random.randint(2, min(2 + self.difficulty // 2, 5))
            self._place_gap(pit_x, pw, gy)
            self.lava_ranges.append((pit_x, pit_x + pw))
            pit_x += pw + 5

        for section in range(4 + self.difficulty):
            sx = random.randint(15 + section * 20, 30 + section * 20)
            if sx >= LEVEL_WIDTH_TILES - 65:
                break
            py = gy - random.randint(2, 5)
            ppw = random.randint(2, 5)
            for i in range(ppw):
                self._place_hard(sx + i, py)

        for section in range(2 + self.difficulty // 3):
            bx = random.randint(25 + section * 35, 50 + section * 35)
            if bx >= LEVEL_WIDTH_TILES - 65:
                break
            by = gy - random.randint(3, 4)
            content = CONTENTS_MUSHROOM if section == 0 else CONTENTS_COIN
            self._place_q_block(bx, by, content)
            self._place_brick(bx - 1, by)
            self._place_brick(bx + 1, by)

        for i in range(3 + self.difficulty):
            ex = random.randint(20 + i * 15, 30 + i * 18)
            if ex >= LEVEL_WIDTH_TILES - 65:
                break
            if self.tiles[gy][ex] != 0:
                etype = 'koopa' if random.random() < 0.3 + self.difficulty * 0.05 else 'goomba'
                self._add_enemy(ex, gy - 1, etype)

        bridge_start = LEVEL_WIDTH_TILES - 30
        bridge_end = LEVEL_WIDTH_TILES - 18
        bridge_y = gy - 2
        for x in range(bridge_start - 2, bridge_end + 5):
            if 0 <= x < LEVEL_WIDTH_TILES:
                self.tiles[gy][x] = 0
                self.tiles[gy + 1][x] = 0
        self.lava_ranges.append((bridge_start - 2, bridge_end + 5))

        for x in range(bridge_start, bridge_end):
            if 0 <= x < LEVEL_WIDTH_TILES:
                self.tiles[bridge_y][x] = 5
                self.bridge_tiles.append((x, bridge_y))
        self.axe_x = bridge_end * TILE

        bowser_hp = min(1 + (self.difficulty - 1) // 2, 5)
        self.bowser = {
            'x': float((bridge_start + 4) * TILE),
            'y': float((bridge_y - 2) * TILE),
            'vx': -1.5 - self.difficulty * 0.2,
            'vy': 0,
            'alive': True,
            'hp': bowser_hp,
            'frame': 0,
            'fire_timer': 0,
            'fireballs': [],
            'left_bound': bridge_start * TILE,
            'right_bound': (bridge_end - 2) * TILE,
        }

        for x in range(bridge_start - 6, bridge_start):
            if 0 <= x < LEVEL_WIDTH_TILES:
                self.tiles[bridge_y + 2][x] = 4

        for x in range(0, bridge_start - 2):
            if self.tiles[gy][x] == 0:
                self.tiles[gy][x] = 4
                self.tiles[gy + 1][x] = 4

    def _gen_block_formations(self, gy):
        x = 16
        while x < LEVEL_WIDTH_TILES - 35:
            x += random.randint(6, max(8, 18 - self.difficulty))
            if self.tiles[gy][x] == 0:
                continue
            roll = random.random()
            by = gy - random.randint(3, 4)
            if roll < 0.06:
                self._place_brick(x, by)
                self._place_q_block(x + 1, by, CONTENTS_MUSHROOM)
                self._place_brick(x + 2, by)
                x += 3
            elif roll < 0.14:
                content = CONTENTS_1UP if random.random() < 0.1 else CONTENTS_COIN
                self._place_q_block(x, by, content)
            elif roll < 0.20:
                bw = random.randint(3, 6)
                for i in range(bw):
                    self._place_brick(x + i, by)
                if random.random() < 0.3:
                    self._place_q_block(x + bw // 2, by, CONTENTS_COIN)
                x += bw
            elif roll < 0.25:
                sh = random.randint(2, min(3 + self.difficulty // 3, 6))
                for row in range(sh):
                    for col in range(row + 1):
                        bx = x + col
                        byr = gy - 1 - row
                        if 0 <= byr < LEVEL_HEIGHT_TILES and bx < LEVEL_WIDTH_TILES:
                            self.tiles[byr][bx] = 1
                x += sh + 2

    def _gen_enemies_ground(self, gy):
        spacing = max(8, 16 - self.difficulty)
        for x in range(22, LEVEL_WIDTH_TILES - 35, spacing):
            if random.random() < 0.35 + self.difficulty * 0.04:
                if self.tiles[gy][x] not in (1, 4):
                    continue
                if self.tiles[gy - 1][x] != 0:
                    continue
                etype = 'goomba' if random.random() < max(0.5, 0.9 - self.difficulty * 0.05) else 'koopa'
                self._add_enemy(x, gy - 1, etype)
                if self.difficulty >= 4 and random.random() < 0.3:
                    if x + 2 < LEVEL_WIDTH_TILES and self.tiles[gy - 1][x + 2] == 0:
                        self._add_enemy(x + 2, gy - 1, etype)

class Player:
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = 0.0, 0.0
        self.w = TILE - 12
        self.big = False
        self.fire = False
        self.on_ground = False
        self.facing = 1
        self.dead = False
        self.lives = 3
        self.coins = 0
        self.score = 0
        self.state = 'idle'
        self.frame = 0.0
        self.invincible = 0
        self.coyote_timer = 0
        self.fireballs = []
        self.grow_timer = 0
        self.reached_flag = False

    @property
    def h(self):
        return TILE * 2 if self.big else TILE

    @property
    def rect(self):
        return pygame.Rect(self.x + 6, self.y, self.w, self.h)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption('ULTRA MARIO - SMB1 STYLE')
        self.clock = pygame.time.Clock()
        self.audio = APU()
        self.font = pygame.font.Font(None, 36)
        self.hud_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)
        self.state = 'menu'
        self.world = 1
        self.level = 1
        self.frame_count = 0
        self.particles = []
        self.death_timer = 0
        self.level_timer = 400
        self.timer_tick = 0
        self.clear_timer = 0
        self.transition_timer = 0
        self.player = None
        self.level_data = None
        self.cam_x = 0
        self.saved_big = False
        self.saved_fire = False
        self.saved_lives = 3
        self.saved_coins = 0
        self.saved_score = 0
        self.reset_level()

    def reset_level(self):
        self.level_data = LevelData(self.world, self.level)
        gy = LEVEL_HEIGHT_TILES - 2
        spawn_y = (gy - 1) * TILE
        if self.level_data.level_type == 'athletic':
            for x in range(4, 16):
                for y in range(LEVEL_HEIGHT_TILES):
                    if self.level_data.tiles[y][x] == 1:
                        spawn_y = (y - 1) * TILE
                        break
        self.player = Player(100, spawn_y)
        self.player.big = self.saved_big
        self.player.fire = self.saved_fire
        self.player.lives = self.saved_lives
        self.player.coins = self.saved_coins
        self.player.score = self.saved_score
        if self.player.big:
            self.player.y -= TILE
        self.cam_x = 0
        self.particles = []
        self.death_timer = 0
        self.clear_timer = 0
        self.level_timer = self.level_data.time
        self.timer_tick = 0

    def advance_level(self):
        self.saved_big = self.player.big
        self.saved_fire = self.player.fire
        self.saved_lives = self.player.lives
        self.saved_coins = self.player.coins
        self.saved_score = self.player.score
        if self.level < 4:
            self.level += 1
        else:
            self.world += 1
            self.level = 1
        if self.world > 8:
            self.state = 'win'
            return
        self.state = 'transition'
        self.transition_timer = 150

    def run(self):
        while True:
            self.frame_count += 1
            self.clock.tick(FPS)
            self.handle_events()
            if self.state == 'menu':
                self.draw_menu()
                self.audio.update_music(game_state='menu')
            elif self.state == 'transition':
                self.audio.update_music(game_state='transition')
                self.draw_transition()
                self.transition_timer -= 1
                if self.transition_timer <= 0:
                    self.state = 'playing'
                    self.reset_level()
            elif self.state == 'playing':
                self.update_game()
                self.draw_game()
                lt = self.level_data.level_type if self.level_data else 'overworld'
                self.audio.update_music(lt, 'playing')
            elif self.state == 'game_over':
                self.draw_game_over()
                self.audio.update_music(game_state='game_over')
            elif self.state == 'win':
                self.draw_win()
                self.audio.update_music(game_state='win')
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type != pygame.KEYDOWN:
                continue
            if self.state == 'menu':
                if event.key == pygame.K_m:
                    self.audio.toggle_music()
                elif event.key == pygame.K_f:
                    self.audio.toggle_music_files()
                elif event.key == pygame.K_RETURN:
                    self.state = 'transition'
                    self.transition_timer = 120
                    self.world = 1
                    self.level = 1
                    self.saved_big = False
                    self.saved_fire = False
                    self.saved_lives = 3
                    self.saved_coins = 0
                    self.saved_score = 0
                    self.audio.play('coin')
            elif self.state == 'playing':
                if event.key in (pygame.K_z, pygame.K_SPACE):
                    player = self.player
                    if player and not player.dead and (player.on_ground or player.coyote_timer > 0):
                        player.vy = JUMP_FORCE
                        self.audio.play('jump_big' if player.big else 'jump')
                        player.coyote_timer = 0
                        player.on_ground = False
                if event.key == pygame.K_x and self.player and self.player.fire:
                    self.fireball()
                if event.key == pygame.K_ESCAPE:
                    self.state = 'menu'
                elif event.key == pygame.K_m:
                    self.audio.toggle_music()
                elif event.key == pygame.K_f:
                    self.audio.toggle_music_files()
            elif self.state in ('game_over', 'win') and event.key == pygame.K_RETURN:
                self.state = 'menu'

    def fireball(self):
        player = self.player
        if len(player.fireballs) < 2:
            player.fireballs.append(
                {'x': player.x + (player.w if player.facing == 1 else 0), 'y': player.y + 16, 'vx': FIREBALL_SPEED * player.facing, 'vy': 0}
            )
            self.audio.play('fireball')

    def update_game(self):
        player = self.player
        level_data = self.level_data

        if self.clear_timer > 0:
            self.clear_timer -= 1
            if self.clear_timer <= 0:
                self.advance_level()
            return

        if player.dead:
            self.death_timer += 1
            if self.death_timer < 30:
                return
            player.vy += GRAVITY
            player.y += player.vy
            if self.death_timer > 180:
                player.lives -= 1
                if player.lives <= 0:
                    self.state = 'game_over'
                else:
                    self.saved_big = False
                    self.saved_fire = False
                    self.saved_lives = player.lives
                    self.saved_coins = player.coins
                    self.saved_score = player.score
                    self.reset_level()
            return

        if player.grow_timer > 0:
            player.grow_timer -= 1
            return

        if player.reached_flag and self.clear_timer <= 0:
            self.clear_timer = 120
            return

        if player.invincible > 0:
            player.invincible -= 1

        self.timer_tick += 1
        if self.timer_tick >= 24:
            self.timer_tick = 0
            self.level_timer -= 1
            if self.level_timer <= 100 and self.level_timer % 50 == 0:
                self.audio.play('warning')
            if self.level_timer <= 0:
                self.kill_player()
                return

        keys = pygame.key.get_pressed()
        acc = PLAYER_ACC
        max_speed = PLAYER_MAX_WALK
        if keys[pygame.K_LSHIFT] or keys[pygame.K_x]:
            acc *= 1.5
            max_speed = PLAYER_MAX_RUN

        if keys[pygame.K_RIGHT]:
            player.vx = min(max_speed, player.vx + acc)
            player.facing = 1
            player.state = 'walk'
            player.frame += 0.2
        elif keys[pygame.K_LEFT]:
            player.vx = max(-max_speed, player.vx - acc)
            player.facing = -1
            player.state = 'walk'
            player.frame += 0.2
        else:
            player.vx *= PLAYER_FRIC
            if abs(player.vx) < 0.1:
                player.vx = 0
            player.state = 'idle'
            player.frame = 0

        if player.on_ground and ((keys[pygame.K_RIGHT] and player.vx < -1) or (keys[pygame.K_LEFT] and player.vx > 1)):
            player.state = 'skid'

        player.x += player.vx
        if player.x < self.cam_x:
            player.x = self.cam_x
            player.vx = 0
        self.check_collision(player, 'x')

        player.vy += GRAVITY
        if player.vy < 0 and not (keys[pygame.K_z] or keys[pygame.K_SPACE]):
            player.vy += 0.5
        player.vy = min(MAX_FALL, player.vy)
        player.y += player.vy

        was_on_ground = player.on_ground
        player.on_ground = False
        self.check_collision(player, 'y')

        if was_on_ground and not player.on_ground and player.vy >= 0:
            player.coyote_timer = 6
        elif player.coyote_timer > 0:
            player.coyote_timer -= 1

        if not player.on_ground:
            player.state = 'jump'

        target_cam = player.x - SCREEN_W // 3
        if target_cam > self.cam_x:
            self.cam_x = max(0, min(target_cam, LEVEL_WIDTH_TILES * TILE - SCREEN_W))

        if player.y > SCREEN_H + 50:
            self.kill_player()

        if level_data.has_flag and player.x + player.w >= level_data.flag_x and not player.reached_flag:
            player.reached_flag = True
            player.vx = 0
            player.vy = 0
            self.audio.play('flagpole')
            player.score += max(100, (SCREEN_H - int(player.y)) * 5)
            self.add_particle(player.x, player.y, 'text', 'CLEAR!')

        if not level_data.has_flag and level_data.bowser and not player.reached_flag:
            if player.x + player.w >= level_data.axe_x - 8:
                player.reached_flag = True
                player.vx = 0
                player.vy = 0
                self.audio.play('bowser_fall')
                for bx, by in level_data.bridge_tiles:
                    level_data.tiles[by][bx] = 0
                if level_data.bowser['alive']:
                    level_data.bowser['alive'] = False
                    level_data.bowser['vy'] = 2
                player.score += 5000
                self.add_particle(player.x, player.y - 20, 'text', '5000')

        self.update_bowser()
        self.update_enemies()
        self.update_fireballs()

    def update_bowser(self):
        player = self.player
        level_data = self.level_data
        if not level_data.bowser:
            return
        bowser = level_data.bowser
        if bowser['alive']:
            bowser['frame'] += 1
            bowser['x'] += bowser['vx']
            if bowser['x'] <= bowser['left_bound']:
                bowser['vx'] = abs(bowser['vx'])
            elif bowser['x'] >= bowser['right_bound']:
                bowser['vx'] = -abs(bowser['vx'])
            bowser['vy'] += GRAVITY * 0.5
            bowser['vy'] = min(6, bowser['vy'])
            bowser['y'] += bowser['vy']
            bx_tile = int((bowser['x'] + 28) // TILE)
            by_tile = int((bowser['y'] + 68) // TILE)
            if 0 <= by_tile < LEVEL_HEIGHT_TILES and 0 <= bx_tile < LEVEL_WIDTH_TILES:
                if level_data.tiles[by_tile][bx_tile] == 5:
                    bowser['y'] = by_tile * TILE - 68
                    bowser['vy'] = 0
                    if random.random() < 0.01 + level_data.difficulty * 0.003:
                        bowser['vy'] = -8
            bowser['fire_timer'] += 1
            fire_rate = max(40, 120 - level_data.difficulty * 10)
            if bowser['fire_timer'] >= fire_rate:
                bowser['fire_timer'] = 0
                direction = -1 if player.x < bowser['x'] else 1
                bowser['fireballs'].append(
                    {'x': bowser['x'] + (0 if direction < 0 else 56), 'y': bowser['y'] + 24, 'vx': direction * (4 + level_data.difficulty * 0.3)}
                )
                self.audio.play('fireball')
            for fireball in bowser['fireballs'][:]:
                fireball['x'] += fireball['vx']
                if fireball['x'] < self.cam_x - 100 or fireball['x'] > self.cam_x + SCREEN_W + 100:
                    bowser['fireballs'].remove(fireball)
                    continue
                if player.rect.colliderect(pygame.Rect(fireball['x'], fireball['y'], 16, 8)) and not player.invincible:
                    self.damage_player()
            bowser_rect = pygame.Rect(bowser['x'], bowser['y'], 56, 68)
            if player.rect.colliderect(bowser_rect) and not player.invincible:
                self.damage_player()
            for fireball in player.fireballs[:]:
                if pygame.Rect(fireball['x'] - 4, fireball['y'] - 4, 8, 8).colliderect(bowser_rect):
                    bowser['hp'] -= 1
                    if fireball in player.fireballs:
                        player.fireballs.remove(fireball)
                    self.audio.play('bump')
                    if bowser['hp'] <= 0:
                        bowser['alive'] = False
                        bowser['vy'] = 2
                        self.audio.play('bowser_fall')
                        player.score += 5000
                        self.add_particle(bowser['x'], bowser['y'], 'text', '5000')
                        for tx, ty in level_data.bridge_tiles:
                            level_data.tiles[ty][tx] = 0
                        player.reached_flag = True
                        player.vx = 0
                    break
        else:
            bowser['vy'] += GRAVITY
            bowser['y'] += bowser['vy']

    def update_enemies(self):
        player = self.player
        level_data = self.level_data
        for enemy in level_data.enemies:
            if not enemy['alive']:
                continue
            if abs(enemy['x'] - player.x) > SCREEN_W + 100:
                continue
            enemy['frame'] += 1
            enemy['vy'] = min(MAX_FALL, enemy['vy'] + GRAVITY)
            enemy['x'] += enemy['vx']
            enemy['y'] += enemy['vy']
            ex_tile = int((enemy['x'] + TILE // 2) // TILE)
            ey_tile = int((enemy['y'] + TILE) // TILE)
            if 0 <= ey_tile < LEVEL_HEIGHT_TILES and 0 <= ex_tile < LEVEL_WIDTH_TILES and level_data.tiles[ey_tile][ex_tile] != 0:
                enemy['y'] = ey_tile * TILE - TILE
                enemy['vy'] = 0
            check_x = enemy['x'] + (TILE if enemy['vx'] > 0 else 0)
            tx = int(check_x // TILE)
            ty = int(enemy['y'] // TILE)
            wall_hit = 0 <= ty < LEVEL_HEIGHT_TILES and 0 <= tx < LEVEL_WIDTH_TILES and level_data.tiles[ty][tx] != 0
            floor_ahead_x = int((enemy['x'] + (TILE if enemy['vx'] > 0 else -4)) // TILE)
            floor_y = int((enemy['y'] + TILE) // TILE)
            no_floor = not (0 <= floor_y < LEVEL_HEIGHT_TILES and 0 <= floor_ahead_x < LEVEL_WIDTH_TILES and level_data.tiles[floor_y][floor_ahead_x] != 0)
            if wall_hit or no_floor:
                enemy['vx'] *= -1
                enemy['facing'] *= -1
            if enemy['x'] < self.cam_x - TILE:
                enemy['vx'] = abs(enemy['vx'])
                enemy['facing'] = 1
            if enemy['y'] > SCREEN_H + 100:
                enemy['alive'] = False
                continue
            enemy_rect = pygame.Rect(enemy['x'] + 4, enemy['y'] + 8, TILE - 8, TILE - 8)
            if player.rect.colliderect(enemy_rect) and not player.invincible:
                if player.vy > 0 and player.rect.bottom < enemy['y'] + TILE // 2 + 8:
                    enemy['alive'] = False
                    player.vy = BOUNCE_FORCE
                    self.audio.play('stomp')
                    self.add_particle(enemy['x'], enemy['y'], 'text', '100')
                    player.score += 100
                else:
                    self.damage_player()

    def update_fireballs(self):
        player = self.player
        for fireball in player.fireballs[:]:
            fireball['x'] += fireball['vx']
            fireball['y'] += fireball['vy']
            fireball['vy'] += GRAVITY
            if fireball['x'] > self.cam_x + SCREEN_W + 50 or fireball['x'] < self.cam_x - 50 or fireball['y'] > SCREEN_H:
                player.fireballs.remove(fireball)
                continue
            fx_tile = int(fireball['x'] // TILE)
            fy_tile = int((fireball['y'] + 8) // TILE)
            if 0 <= fy_tile < LEVEL_HEIGHT_TILES and 0 <= fx_tile < LEVEL_WIDTH_TILES and self.level_data.tiles[fy_tile][fx_tile] != 0:
                fireball['y'] = fy_tile * TILE - 8
                fireball['vy'] = -5
            fireball_rect = pygame.Rect(fireball['x'] - 4, fireball['y'] - 4, 8, 8)
            hit = False
            for enemy in self.level_data.enemies:
                if enemy['alive'] and fireball_rect.colliderect(pygame.Rect(enemy['x'], enemy['y'], TILE, TILE)):
                    enemy['alive'] = False
                    hit = True
                    self.audio.play('stomp')
                    self.add_particle(enemy['x'], enemy['y'], 'text', '200')
                    player.score += 200
                    break
            if hit and fireball in player.fireballs:
                player.fireballs.remove(fireball)

    def check_collision(self, ent, axis):
        rect = ent.rect
        start_x = max(0, int(rect.left // TILE) - 1)
        end_x = min(LEVEL_WIDTH_TILES, int(rect.right // TILE) + 2)
        start_y = max(0, int(rect.top // TILE) - 1)
        end_y = min(LEVEL_HEIGHT_TILES, int(rect.bottom // TILE) + 2)
        for ty in range(start_y, end_y):
            for tx in range(start_x, end_x):
                tile = self.level_data.tiles[ty][tx]
                if tile == 0:
                    continue
                tile_rect = pygame.Rect(tx * TILE, ty * TILE, TILE, TILE)
                prect = pygame.Rect(ent.x + 6, ent.y, ent.w, ent.h)
                if not prect.colliderect(tile_rect):
                    continue
                if axis == 'x':
                    if ent.vx > 0:
                        ent.x = tile_rect.left - ent.w - 6
                    elif ent.vx < 0:
                        ent.x = tile_rect.right - 6
                    ent.vx = 0
                elif axis == 'y':
                    if ent.vy > 0:
                        ent.y = tile_rect.top - ent.h
                        ent.on_ground = True
                        ent.vy = 0
                    elif ent.vy < 0:
                        ent.y = tile_rect.bottom
                        ent.vy = 0
                        if tile not in (9, 5):
                            self.hit_block(tx, ty)

    def hit_block(self, x, y):
        tile = self.level_data.tiles[y][x]
        if tile == 3:
            self.level_data.tiles[y][x] = 2
            self.audio.play('bump')
            if (x, y) in self.level_data.blocks:
                content = self.level_data.blocks.pop((x, y))
                if content == CONTENTS_COIN:
                    self.player.coins += 1
                    self.player.score += 200
                    self.audio.play('coin')
                    self.add_particle(x * TILE, y * TILE - 20, 'text', '200')
                    if self.player.coins >= 100:
                        self.player.coins -= 100
                        self.player.lives += 1
                        self.audio.play('1up')
                elif content == CONTENTS_MUSHROOM:
                    if not self.player.big:
                        self.player.big = True
                        self.player.y -= TILE
                        self.player.grow_timer = 30
                        self.audio.play('powerup')
                        self.add_particle(x * TILE, y * TILE - 20, 'text', 'SUPER!')
                    else:
                        self.player.fire = True
                        self.player.grow_timer = 15
                        self.audio.play('powerup')
                        self.add_particle(x * TILE, y * TILE - 20, 'text', 'FIRE!')
                elif content == CONTENTS_1UP:
                    self.player.lives += 1
                    self.audio.play('1up')
                    self.add_particle(x * TILE, y * TILE - 20, 'text', '1UP')
                elif content == CONTENTS_FIRE:
                    self.player.fire = True
                    self.player.big = True
                    self.audio.play('powerup')
        elif tile == 2:
            if self.player.big:
                self.level_data.tiles[y][x] = 0
                self.audio.play('break')
                for dx in (-1, 1):
                    for dy in (-1, 0):
                        self.particles.append(
                            {
                                'x': x * TILE + TILE // 2 + dx * 10,
                                'y': y * TILE + dy * 10,
                                'type': 'debris',
                                'vx': dx * 3 + random.uniform(-1, 1),
                                'vy': -6 + dy * 2,
                                'val': None,
                                'life': 40,
                            }
                        )
            else:
                self.audio.play('bump')

    def damage_player(self):
        if self.player.invincible > 0:
            return
        if self.player.fire:
            self.player.fire = False
            self.player.invincible = 120
            self.audio.play('shrink')
        elif self.player.big:
            self.player.big = False
            self.player.invincible = 120
            self.audio.play('shrink')
        else:
            self.kill_player()

    def kill_player(self):
        if self.player.dead:
            return
        self.player.dead = True
        self.player.vy = JUMP_FORCE * 0.8
        self.player.vx = 0
        self.death_timer = 0
        self.audio.play('die')

    def add_particle(self, x, y, ptype, val):
        self.particles.append({'x': x, 'y': y, 'type': ptype, 'val': val, 'life': 60, 'vx': 0, 'vy': -1.5})

    def draw_menu(self):
        self.screen.fill(C_BLACK)
        title = self.big_font.render('ULTRA MARIO', True, C_MARIO_RED)
        subtitle = self.big_font.render('2D. BROS', True, C_WHITE)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 100))
        self.screen.blit(subtitle, (SCREEN_W // 2 - subtitle.get_width() // 2, 170))
        draw_mario(self.screen, SCREEN_W // 2 - 20, 280, 'idle', 0, 1, False, False)
        if (self.frame_count // 30) % 2 == 0:
            start = self.font.render('PUSH START BUTTON', True, C_QUESTION)
            self.screen.blit(start, (SCREEN_W // 2 - start.get_width() // 2, 370))
        mus = 'ON' if self.audio.music_on else 'OFF'
        files = 'ON' if self.audio.use_files else 'OFF'
        info = [
            'ARROWS = Move   Z/SPACE = Jump',
            'SHIFT = Run   X = Fireball',
            f'M = Music {mus}   F = File OST {files}',
            'Put YouTube rips in music/ as over.mp3 under.mp3 castle.mp3',
            '',
            'WORLDS 1-1 THROUGH 8-4',
        ]
        y = 430
        for line in info:
            txt = self.small_font.render(line, True, C_CASTLE_GRAY)
            self.screen.blit(txt, (SCREEN_W // 2 - txt.get_width() // 2, y))
            y += 22

    def draw_transition(self):
        self.screen.fill(C_BLACK)
        world_text = self.big_font.render(f'WORLD  {self.world}-{self.level}', True, C_WHITE)
        self.screen.blit(world_text, (SCREEN_W // 2 - world_text.get_width() // 2, SCREEN_H // 2 - 60))
        draw_mario(self.screen, SCREEN_W // 2 - 50, SCREEN_H // 2 + 10, 'idle', 0, 1, self.saved_big, self.saved_fire)
        lives = self.font.render(f'x  {self.saved_lives}', True, C_WHITE)
        self.screen.blit(lives, (SCREEN_W // 2, SCREEN_H // 2 + 18))
        label = ['OVERWORLD', 'UNDERGROUND', 'ATHLETIC', 'CASTLE'][self.level - 1]
        type_text = self.small_font.render(label, True, C_CASTLE_GRAY)
        self.screen.blit(type_text, (SCREEN_W // 2 - type_text.get_width() // 2, SCREEN_H // 2 + 70))

    def draw_game_over(self):
        self.screen.fill(C_BLACK)
        self.screen.blit(self.font.render('GAME OVER', True, C_WHITE), (SCREEN_W // 2 - 80, SCREEN_H // 2 - 20))
        self.screen.blit(self.small_font.render('PRESS ENTER', True, C_CASTLE_GRAY), (SCREEN_W // 2 - 50, SCREEN_H // 2 + 30))
        score = self.player.score if self.player else 0
        self.screen.blit(self.small_font.render(f'FINAL SCORE: {score}', True, C_COIN_GOLD), (SCREEN_W // 2 - 70, SCREEN_H // 2 + 60))

    def draw_win(self):
        self.screen.fill(C_BLACK)
        self.screen.blit(self.big_font.render('CONGRATULATIONS!', True, C_COIN_GOLD), (SCREEN_W // 2 - 250, 150))
        self.screen.blit(self.font.render('THANK YOU MARIO!', True, C_WHITE), (SCREEN_W // 2 - 130, 250))
        self.screen.blit(self.font.render('YOUR QUEST IS OVER.', True, C_WHITE), (SCREEN_W // 2 - 150, 300))
        score = self.player.score if self.player else 0
        self.screen.blit(self.font.render(f'FINAL SCORE: {score}', True, C_COIN_GOLD), (SCREEN_W // 2 - 120, 380))
        if (self.frame_count // 40) % 2 == 0:
            self.screen.blit(self.small_font.render('PRESS ENTER', True, C_CASTLE_GRAY), (SCREEN_W // 2 - 50, 460))
        draw_mario(self.screen, SCREEN_W // 2 - 20, 500, 'idle', 0, 1, True, True)

    def draw_game(self):
        level_data = self.level_data
        player = self.player
        cam = self.cam_x
        if level_data.level_type == 'overworld':
            sky = C_SKY if self.world <= 5 else C_SKY_NIGHT
        elif level_data.level_type == 'underground':
            sky = C_SKY_UNDER
        elif level_data.level_type == 'athletic':
            sky = C_SKY_ATHLETIC if self.world <= 6 else C_SKY_NIGHT
        else:
            sky = C_SKY_CASTLE
        self.screen.fill(sky)

        start_col = max(0, int(cam // TILE) - 1)
        end_col = min(LEVEL_WIDTH_TILES, start_col + (SCREEN_W // TILE) + 3)

        for type_name, x, y in level_data.decor:
            if cam - 100 < x < cam + SCREEN_W + 100:
                draw_scenery(self.screen, x - cam, y, type_name)

        if level_data.has_flag:
            draw_castle(self.screen, level_data.castle_x - cam, (LEVEL_HEIGHT_TILES - 5) * TILE - 40)
            draw_flagpole(self.screen, level_data.flag_x - cam, (LEVEL_HEIGHT_TILES - 2) * TILE)

        gy = LEVEL_HEIGHT_TILES - 2
        for lx_start, lx_end in level_data.lava_ranges:
            for lx in range(lx_start, lx_end):
                sx = lx * TILE - cam
                sy = gy * TILE
                wave = int(math.sin(self.frame_count * 0.1 + lx * 0.5) * 4)
                pygame.draw.rect(self.screen, C_LAVA, (sx, sy + wave, TILE, TILE * 2 - wave))
                pygame.draw.rect(self.screen, C_LAVA_BRIGHT, (sx + 4, sy + wave, TILE - 8, 6))

        for x in range(start_col, end_col):
            for y in range(LEVEL_HEIGHT_TILES):
                tile = level_data.tiles[y][x]
                sx = x * TILE - cam
                sy = y * TILE
                if tile == 1:
                    draw_block(self.screen, sx, sy, 'ground', underground=level_data.underground)
                elif tile == 2:
                    draw_block(self.screen, sx, sy, 'brick', underground=level_data.underground)
                elif tile == 3:
                    draw_block(self.screen, sx, sy, 'q_block', self.frame_count)
                elif tile == 4:
                    draw_block(self.screen, sx, sy, 'hard')
                elif tile == 5:
                    pygame.draw.rect(self.screen, C_BRIDGE, (sx, sy, TILE, TILE // 3))
                    pygame.draw.rect(self.screen, (120, 80, 0), (sx, sy, TILE, TILE // 3), 2)
                    for cx in range(0, TILE, 12):
                        pygame.draw.rect(self.screen, (120, 80, 0), (sx + cx + 2, sy + 4, 8, 4))

        for pipe_x, pipe_y, pipe_h in level_data.pipes:
            draw_pipe(self.screen, pipe_x * TILE - cam, pipe_y * TILE, TILE * 2, pipe_h * TILE)

        if not level_data.has_flag and level_data.bowser:
            draw_axe(self.screen, level_data.axe_x - cam, (level_data._ground_row() - 3) * TILE, self.frame_count)

        if level_data.bowser:
            bowser = level_data.bowser
            if bowser['y'] < SCREEN_H + 200:
                draw_bowser(self.screen, bowser['x'] - cam, bowser['y'], bowser['frame'])
            for fireball in bowser.get('fireballs', []):
                bfx = int(fireball['x'] - cam)
                bfy = int(fireball['y'])
                pygame.draw.ellipse(self.screen, C_FIREBALL, (bfx, bfy, 16, 8))
                pygame.draw.ellipse(self.screen, C_LAVA_BRIGHT, (bfx + 4, bfy + 2, 8, 4))

        for enemy in level_data.enemies:
            if enemy['alive'] and cam - 50 < enemy['x'] < cam + SCREEN_W + 50:
                if enemy['type'] == 'goomba':
                    draw_goomba(self.screen, enemy['x'] - cam, enemy['y'], enemy['frame'])
                else:
                    draw_koopa(self.screen, enemy['x'] - cam, enemy['y'], enemy['frame'], enemy['facing'])

        if player and not player.dead:
            if player.invincible == 0 or (player.invincible % 4) < 2:
                draw_mario(self.screen, player.x - cam, player.y, player.state, player.frame, player.facing, player.big, player.fire)
        elif player:
            draw_mario(self.screen, player.x - cam, player.y, 'jump', 0, player.facing, False, False)

        if player:
            for fireball in player.fireballs:
                fx = int(fireball['x'] - cam)
                fy = int(fireball['y'])
                pygame.draw.circle(self.screen, C_FIREBALL, (fx, fy), 6)
                pygame.draw.circle(self.screen, C_COIN_GOLD, (fx, fy), 3)

        for particle in self.particles[:]:
            particle['life'] -= 1
            particle['x'] += particle.get('vx', 0)
            particle['y'] += particle.get('vy', -1)
            if particle['type'] == 'debris':
                particle['vy'] = particle.get('vy', 0) + 0.4
            if particle['life'] <= 0:
                self.particles.remove(particle)
                continue
            if particle['type'] == 'text':
                txt = self.hud_font.render(str(particle['val']), True, C_WHITE)
                self.screen.blit(txt, (particle['x'] - cam, particle['y']))
            elif particle['type'] == 'debris':
                pygame.draw.rect(self.screen, C_BRICK, (int(particle['x'] - cam), int(particle['y']), 8, 8))

        hud_y = 16
        self.screen.blit(self.hud_font.render(f'SCORE  {player.score:06d}', True, C_HUD), (40, hud_y))
        pygame.draw.circle(self.screen, C_COIN_GOLD, (265, hud_y + 10), 8)
        pygame.draw.circle(self.screen, C_COIN_SHADOW, (265, hud_y + 10), 8, 2)
        self.screen.blit(self.hud_font.render(f'x{player.coins:02d}', True, C_HUD), (278, hud_y))
        self.screen.blit(self.hud_font.render('WORLD', True, C_HUD), (420, hud_y))
        self.screen.blit(self.hud_font.render(f' {self.world}-{self.level}', True, C_HUD), (420, hud_y + 22))
        self.screen.blit(self.hud_font.render('TIME', True, C_HUD), (550, hud_y))
        time_color = C_HUD if self.level_timer > 100 else C_MARIO_RED
        self.screen.blit(self.hud_font.render(f' {self.level_timer:3d}', True, time_color), (550, hud_y + 22))
        self.screen.blit(self.hud_font.render(f'LIVES x {player.lives}', True, C_HUD), (650, hud_y))

if __name__ == '__main__':
    Game().run()
