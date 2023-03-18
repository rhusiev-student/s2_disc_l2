"""Tests for the LZ77 compression algorithm."""
import timeit

import matplotlib.pyplot as plt

from src.lz77 import LZ77
from src.lzw import LZW


def test_lz77_correctness() -> None:
    """Test that the compression algorithm works correctly."""
    compressor = LZ77(raw_data="abracadabra")
    compressor.compress_and_set()
    compressor.decompress_and_set()
    assert compressor.raw_data == "abracadabra"

    compressor = LZ77(raw_data="abracadabra", lookahead_size=4, buffer_size=4)
    compressor.compress_and_set()
    compressor.decompress_and_set()
    assert compressor.raw_data == "abracadabra"

    compressor = LZ77(raw_data="abracadabra", lookahead_size=50, buffer_size=50)
    compressor.compress_and_set()
    compressor.decompress_and_set()
    assert compressor.raw_data == "abracadabra"

    with open("ChornaRada.txt", "r", encoding="utf-8") as file:
        data = file.read()
    compressor = LZ77(raw_data=data)
    compressor.compress_and_set()
    compressor.decompress_and_set()
    assert compressor.raw_data == data


def test_lzw_correctness() -> None:
    """Test that the compression algorithm works correctly."""
    compressor = LZW(raw_data="abracadabra")
    compressor.compress_and_set()
    assert compressor.decompress() == "abracadabra"

    compressor = LZW(raw_data="abracadabra")
    compressor.compress_and_set()
    assert compressor.decompress() == "abracadabra"

    data = """абракадабра 123 йцукенгшщзхїфівапролджєячсмитьбю.йфіквчмрнпамитолщл
ьбжхзжпрвічсмреамитьдшгневчсмитьдшгнеамиоЙЦУКЕНГШЗХЇҐЇХЖ,ЮБЬТИМ-=_+()*?:%;#"!@#$^&
:";'<>,./?\\|][{}`~'ʼ"""
    compressor = LZW(raw_data=data)
    compressor.compress_and_set()
    assert compressor.decompress() == data

    with open("ChornaRada.txt", "r", encoding="utf-8") as file:
        data = file.read()
    data = data[: len(data) // 5]
    compressor = LZW(raw_data=data)
    compressor.compress_and_set()
    assert compressor.decompress() == data


def test_effectiveness(cls: LZ77 | LZW, fractions: list[int], data: str) -> None:
    """Test that the compression algorithm is fast enough."""
    with open("ChornaRada.txt", "r", encoding="utf-8") as file:
        data = file.read()

    lens = [len(data) // fraction for fraction in fractions]
    datas = [data[:length] for length in lens]
    byte_sizes = [len(data.encode("utf-8")) for data in datas]

    compressors = [cls(raw_data=data) for data in datas]

    times = []
    for compressor in compressors:
        time_start = timeit.default_timer()
        compressor.compress_and_set()
        time_end = timeit.default_timer()
        times.append(time_end - time_start)

    times_decompress = []
    for compressor in compressors:
        time_start = timeit.default_timer()
        compressor.decompress()
        time_end = timeit.default_timer()
        times_decompress.append(time_end - time_start)

    bytes_compressed = [len(compressor.compressed_data) for compressor in compressors]

    kilobytes = [byte_size / 1024 for byte_size in byte_sizes]

    compression_ratio = [
        byte_compressed / byte_size
        for byte_compressed, byte_size in zip(bytes_compressed, byte_sizes)
    ]

    plt.suptitle(cls.__name__)
    plt.subplot(2, 2, 1)
    plt.plot(kilobytes, times, label="Compression")
    plt.plot(kilobytes, times_decompress, label="Decompression")
    plt.title("Time")
    plt.ylabel("Time (s)")
    plt.xlabel("Kilobytes")

    plt.subplot(2, 2, 2)
    plt.plot(kilobytes, compression_ratio)
    plt.title("Compression ratio")
    plt.ylabel("Compression ratio")
    plt.xlabel("Kilobytes")

    plt.show()
