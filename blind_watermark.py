#!/usr/bin/env python3
# coding=utf-8
import numpy as np
import cv2
from bwm_core import WaterMarkCore

class WaterMark:
    def __init__(self, password_wm=1, password_img=1, block_shape=(4, 4), mode='common', processes=None):
        self.bwm_core = WaterMarkCore(password_img=password_img, mode=mode, processes=processes)
        self.password_wm = password_wm
        self.wm_bit = None
        self.wm_size = 0

    def read_img(self, filename=None, img=None):
        img = img or cv2.imread(filename, flags=cv2.IMREAD_UNCHANGED)
        assert img is not None, f"image file '{filename}' not read"
        self.bwm_core.read_img_arr(img=img)
        return img

    def read_wm(self, wm_content, mode='img'):
        assert mode in ('img', 'str', 'bit')
        if mode == 'img':
            wm = cv2.imread(filename=wm_content, flags=cv2.IMREAD_GRAYSCALE)
            assert wm is not None, f'file "{wm_content}" not read'
            self.wm_bit = wm.flatten() > 128
        elif mode == 'str':
            byte = bin(int(wm_content.encode('utf-8').hex(), 16))[2:]
            self.wm_bit = np.array(list(byte)) == '1'
        else:
            self.wm_bit = np.array(wm_content)
        self.wm_size = self.wm_bit.size
        np.random.RandomState(self.password_wm).shuffle(self.wm_bit)
        self.bwm_core.read_wm(self.wm_bit)

    def embed(self, filename=None, compression_ratio=None):
        embed_img = self.bwm_core.embed()
        if filename:
            params = []
            if compression_ratio is not None:
                if filename.endswith('.jpg'):
                    params = [cv2.IMWRITE_JPEG_QUALITY, compression_ratio]
                elif filename.endswith('.png'):
                    params = [cv2.IMWRITE_PNG_COMPRESSION, compression_ratio]
            cv2.imwrite(filename, embed_img, params)
        return embed_img

    def extract_decrypt(self, wm_avg):
        wm_index = np.arange(self.wm_size)
        np.random.RandomState(self.password_wm).shuffle(wm_index)
        wm_avg[wm_index] = wm_avg.copy()
        return wm_avg

    def extract(self, filename=None, embed_img=None, wm_shape=None, out_wm_name=None, mode='img'):
        assert wm_shape, 'wm_shape needed'
        if filename:
            embed_img = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
            assert embed_img is not None, f"{filename} not read"
        self.wm_size = np.prod(wm_shape)
        wm_avg = self.bwm_core.extract_with_kmeans(img=embed_img, wm_shape=wm_shape) if mode in ('str', 'bit') else self.bwm_core.extract(img=embed_img, wm_shape=wm_shape)
        wm = self.extract_decrypt(wm_avg=wm_avg)
        if mode == 'img':
            wm = 255 * wm.reshape(wm_shape)
            cv2.imwrite(out_wm_name, wm)
        elif mode == 'str':
            byte = ''.join(str(int(i >= 0.5)) for i in wm)
            wm = bytes.fromhex(hex(int(byte, 2))[2:]).decode('utf-8', errors='replace')
        return wm
