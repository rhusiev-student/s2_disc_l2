"""LZW algorithm implementation."""
import struct
from typing import Iterable


class LZW:
    """LZW compression algorithm implementation class.

    Attributes:
        raw_data (str): Raw data to compress.
        raw_data_bytes (bytes): Raw data bytes.
        compressed_data (bytes): Compressed data to decompress.
    """

    def __init__(self, raw_data: str = "", compressed_data: bytes = b"") -> None:
        """Initialize LZW object.

        Args:
            raw_data (str): Raw data to compress.
            compressed_data (bytes): Compressed data to decompress.
        """
        self.raw_data: str = raw_data
        self.raw_data_bytes: bytes = raw_data.encode("utf-8")
        self.compressed_data: bytes = compressed_data

    def compress(self) -> bytes:
        """Compress raw data.

        Returns:
            bytes: Compressed data.
        """
        compressed = []
        start_dictionary = list(set(self.raw_data_bytes))
        dictionary: list[list[int]] = [[i] for i in start_dictionary]
        i = 0
        while i < len(self.raw_data_bytes):
            prefix_id = self.find_longest_prefix(
                dictionary,
                (self.raw_data_bytes[j] for j in range(i, len(self.raw_data_bytes))),
            )
            if prefix_id == -1:
                break
            prefix = dictionary[prefix_id]
            compressed.append(prefix_id)
            i += len(prefix)
            if i < len(self.raw_data_bytes):
                dictionary.append(prefix + [self.raw_data_bytes[i]])

        start_dict_bytes = bytes(start_dictionary)
        compressed_bytes = b""
        for i in compressed:
            compressed_bytes += struct.pack(">I", i)
        start_dict_header = struct.pack("I", len(start_dict_bytes))
        compressed_header = struct.pack("I", len(compressed_bytes))
        return (
            start_dict_header + start_dict_bytes + compressed_header + compressed_bytes
        )

    def find_longest_prefix(
        self, dictionary: list[list[int]], sequence: Iterable[int]
    ) -> int:
        """Find longest prefix in dictionary.

        Args:
            dictionary (list[list[int]]): Dictionary to search in.
            sequence (Iterable[int]): Sequence to search for.

        Returns:
            int: Index of longest prefix in dictionary.
        """
        prefix = []
        for char in sequence:
            prefix += [char]
            if prefix in dictionary:
                continue
            return dictionary.index(prefix[:-1])
        return dictionary.index(prefix)

    def compress_and_set(self) -> None:
        """Compress raw data and set compressed data."""
        self.compressed_data = self.compress()

    def save_compressed(self, path: str) -> None:
        """Save compressed data to file.

        Args:
            path (str): Path to file.
        """
        with open(path, "wb") as file:
            file.write(self.compressed_data)

    def load_compressed(self, path: str) -> None:
        """Load compressed data from file.

        Args:
            path (str): Path to file.
        """
        with open(path, "rb") as file:
            self.compressed_data = file.read()

    def decompress(self) -> str:
        """Decompress compressed data.

        Returns:
            str: Decompressed data.
        """
        start_dict_size = struct.unpack("I", self.compressed_data[:4])[0]
        start_dict = self.compressed_data[4 : 4 + start_dict_size]
        compressed_size = struct.unpack(
            "I", self.compressed_data[4 + start_dict_size : 8 + start_dict_size]
        )[0]
        compressed = []
        for i in range(8 + start_dict_size, 8 + start_dict_size + compressed_size, 4):
            compressed.append(struct.unpack(">I", self.compressed_data[i : i + 4])[0])
        dictionary = [[i] for i in start_dict]
        decompressed = []
        prev_i = compressed[0]
        decompressed += dictionary[prev_i]
        for i in compressed[1:]:
            if i < len(dictionary):
                dictionary.append(dictionary[prev_i] + [dictionary[i][0]])
                decompressed += dictionary[i]
            else:
                dictionary.append(dictionary[prev_i] + [dictionary[prev_i][0]])
                decompressed += dictionary[-1]
            prev_i = i
        return bytes(decompressed).decode("utf-8")

    def decompress_and_set(self) -> None:
        """Decompress compressed data and set raw data."""
        self.raw_data = self.decompress()

    def save_decompressed(self, path: str) -> None:
        """Save decompressed data to file.

        Args:
            path (str): Path to file.
        """
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.raw_data)

    def load_raw(self, path: str) -> None:
        """Load raw data from file.

        Args:
            path (str): Path to file.
        """
        with open(path, "r", encoding="utf-8") as file:
            self.raw_data = file.read()
            self.raw_data_bytes = self.raw_data.encode("utf-8")
