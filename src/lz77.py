"""LZ77 Algorithm Implementation."""
from itertools import cycle, islice


class LZ77:
    """LZ77 Algorithm Implementation.

    Either raw text or compressed data can be used to initialize the class.
    compress() will use the raw data to compress it.
    decompress() will use the compressed data to decompress it.

    Attributes:
        buffer_size (int): Size of the buffer, defaults to 256
        lookahead_size (int): How far ahead to look for matches, defaults to 256
        _buffer (bytes): Buffer, used between methods
        compressed_data (bytes): Compressed data
        raw_data (str): Raw data
        _raw_data_bytes (bytes): Raw data in bytes

    Methods:
        compress(): Compresses a string using the LZ77 algorithm.
        _find_match(): Finds the longest match in the buffer, used by compress().
        set_compressed(): Sets the compressed data.
        compress_and_set(): Compresses the data and saves it to a variable.
        decompress(): Decompresses the data.
        set_raw(): Sets the raw data.
        decompress_and_set(): Decompresses the data and saves it to a variable.
        save_compressed(): Saves the compressed data to a file.
        save_raw(): Saves the raw data to a file.
    """

    def __init__(
        self,
        compressed_data: bytes = b"",
        raw_data: str = "",
        buffer_size: int = 256,
        lookahead_size: int = 256,
    ) -> None:
        self.buffer_size = buffer_size
        self.lookahead_size = lookahead_size
        self._buffer: bytes = b""
        self.compressed_data: bytes = compressed_data
        self._raw_data_bytes: bytes = raw_data.encode("utf-8")
        self.raw_data: str = raw_data

    def compress(self) -> list[tuple[int, int, int]]:
        """Compresses a string using the LZ77 algorithm.

        Returns:
            list[tuple[int, int, int]]: Compressed data. Format:
            [(offset, length, char), ...]
        """
        compressed = []
        i = 0
        while i < len(self._raw_data_bytes):
            offset, length, char = self._find_match(i)
            compressed.append((offset, length, char))
            self._buffer += self._raw_data_bytes[i : i + length + 1]
            i += length + 1
            if len(self._buffer) > self.buffer_size:
                self._buffer = self._buffer[-self.buffer_size :]

        self._buffer = b""
        return compressed

    def _find_match(self, position: int) -> tuple[int, int, int]:
        """Finds the longest match in the buffer.

        Args:
            position (int): Current position in the data

        Returns:
            tuple[int, int, int]: Tuple containing the length of the match,
            the offset of the match and the character after the match in bytes
        """
        possible_matches = []
        for i in range(len(self._buffer)):
            if self._buffer[i] == self._raw_data_bytes[position]:
                length = 0
                for length in range(self.lookahead_size):
                    if position + length >= len(self._raw_data_bytes):
                        break
                    if (
                        self._buffer[i + length % (len(self._buffer) - i)]
                        != self._raw_data_bytes[position + length]
                    ):
                        break
                possible_matches.append((len(self._buffer) - i - 1, length))

        if not possible_matches:
            return (0, 0, self._raw_data_bytes[position])

        longest_match = max(possible_matches, key=lambda x: x[1])
        if len(self._raw_data_bytes) == position + longest_match[1]:
            return longest_match[0], longest_match[1] - 1, self._raw_data_bytes[-1]

        return (
            longest_match[0],
            longest_match[1],
            self._raw_data_bytes[position + longest_match[1]],
        )

    def set_compressed(self, compressed_data: bytes) -> None:
        """Sets the compressed data.

        Args:
            compressed_data (bytes): Compressed data
        """
        self.compressed_data = compressed_data

    def compress_and_set(self) -> None:
        """Compresses the data and saves it to a variable."""
        self.set_compressed(
            bytes(item for sublist in self.compress() for item in sublist)
        )

    def decompress(self) -> bytes:
        """Decompresses the data.

        Returns:
            bytes: Decompressed data in bytes
        """
        decompressed: bytes = b""
        for i in range(0, len(self.compressed_data), 3):
            code = self.compressed_data[i : i + 3]
            offset, length, char = code
            offset = int(offset)
            length = int(length)
            buffer_part = decompressed[
                -offset - 1 : len(decompressed) - offset - 1 + length
            ]
            decompressed += bytes(
                islice(
                    cycle(buffer_part),
                    length,
                )
            )
            decompressed += bytes([char])
        return decompressed

    def set_raw(self, raw_data: bytes) -> None:
        """Sets the raw data.

        Args:
            raw_data (bytes): Raw data
        """
        self._raw_data_bytes = raw_data
        self.raw_data = raw_data.decode("utf-8")

    def decompress_and_set(self) -> None:
        """Decompresses the data and saves it to a variable."""
        self.set_raw(self.decompress())

    def save_compressed(self, path: str) -> None:
        """Saves the compressed data to a file.

        Args:
            path (str): Path to the file
        """
        with open(path, "wb") as file:
            file.write(self.compressed_data)

    def save_raw(self, path: str) -> None:
        """Saves the raw data to a file.

        Args:
            path (str): Path to the file
        """
        with open(path, "w", encoding="utf-8") as file:
            file.write(self.raw_data)
