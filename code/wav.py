import argparse
import wave
import struct
import random
import json

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--encode', action='store_true')
parser.add_argument('-H', '--header', action='store_true', help='generate only WAV header')
parser.add_argument('-d', '--decode', action='store_true')

args = parser.parse_args()

if args.encode:
    freq = 44100
    freq = freq / 16
    out = wave.open('test.wav', 'w')
    out.setparams((1, 2, freq, 0, 'NONE', 'not compressed'))

    if not args.header:
        event = {
            'connector': 'wav',
            'connector_name': 'wav',
            'event_type': 'check',
            'source_type': 'resource',
            'component': 'localhost',
            'resource': 'ROC - Realtime Audio Streamer',
            'output': 'event'
        }

        binary_event = json.dumps(event).encode('utf-8')
        binary_event *= 10000

        values = []
        len_evt = len(binary_event)
        for i in range(0, len_evt, 2):
            valuel = binary_event[i % len_evt]
            try:
                valuer = binary_event[i % len_evt + 1] << 8
            except IndexError:
                valuer = 0
            valuef = valuel | valuer
            packed_value = struct.pack('H', valuef)
            values.append(packed_value)

        frames = b''.join(values)
        out.writeframesraw(frames)

    out.close()

if args.decode:
    in_ = wave.open('test.wav', 'r')
    frames = in_.readframes(in_.getnframes())
    in_.close()
    print(frames.decode('utf-8'))
