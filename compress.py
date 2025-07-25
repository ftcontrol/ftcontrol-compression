import lzma
import zlib
import bz2
import brotli
import lz4.frame
import zstandard as zstd
import time


def bytes_to_mb(size_bytes: int) -> float:
    return size_bytes / (1024 * 1024)


def compress_lzma(data: bytes) -> bytes:
    return lzma.compress(data)


def decompress_lzma(data: bytes) -> bytes:
    return lzma.decompress(data)


def compress_zlib(data: bytes) -> bytes:
    return zlib.compress(data, level=9)


def decompress_zlib(data: bytes) -> bytes:
    return zlib.decompress(data)


def compress_bz2(data: bytes) -> bytes:
    return bz2.compress(data, compresslevel=9)


def decompress_bz2(data: bytes) -> bytes:
    return bz2.decompress(data)


def compress_brotli(data: bytes) -> bytes:
    return brotli.compress(data, quality=11)


def decompress_brotli(data: bytes) -> bytes:
    return brotli.decompress(data)


def compress_lz4(data: bytes) -> bytes:
    return lz4.frame.compress(data, compression_level=16)


def decompress_lz4(data: bytes) -> bytes:
    return lz4.frame.decompress(data)


def compress_zstd(data: bytes) -> bytes:
    cctx = zstd.ZstdCompressor(level=22)
    return cctx.compress(data)


def decompress_zstd(data: bytes) -> bytes:
    dctx = zstd.ZstdDecompressor()
    return dctx.decompress(data)


with open("data.json", "r", encoding="utf-8") as f:
    text = f.read()

input_bytes = text.encode("utf-8")
input_size = len(input_bytes)

results = {}

print(
    f"Original size: {input_size} bytes ({bytes_to_mb(input_size):.4f} MB)\n")

methods = {
    'LZMA': (compress_lzma, decompress_lzma),
    'Zlib': (compress_zlib, decompress_zlib),
    'Bz2': (compress_bz2, decompress_bz2),
    'Brotli': (compress_brotli, decompress_brotli),
    'LZ4': (compress_lz4, decompress_lz4),
    'Zstandard': (compress_zstd, decompress_zstd),
}

best_method = None
best_size = None

for method, (compress_func, decompress_func) in methods.items():
    start_time = time.perf_counter()
    compressed_data = compress_func(input_bytes)
    compress_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    decompressed_data = decompress_func(compressed_data)
    decompress_time = time.perf_counter() - start_time

    if decompressed_data != input_bytes:
        print(
            f"Warning: Decompressed data does NOT match original for {method}!")

    compressed_size = len(compressed_data)
    saved_bytes = input_size - compressed_size
    saved_percent = (saved_bytes / input_size) * 100 if input_size > 0 else 0

    print(f"{method}:")
    print(
        f"  Compressed size: {compressed_size} bytes ({bytes_to_mb(compressed_size):.4f} MB)")
    print(f"  Saved: {saved_bytes} bytes ({saved_percent:.2f}%)")
    print(f"  Compression time: {compress_time:.3f} seconds")
    print(f"  Decompression time: {decompress_time:.3f} seconds\n")

    results[method] = compressed_data

    if best_size is None or compressed_size < best_size:
        best_size = compressed_size
        best_method = method

print(
    f"Best compression method: {best_method} with size {best_size} bytes ({bytes_to_mb(best_size):.4f} MB)")

with open(f"compressed_best.{best_method.lower()}", "wb") as f:
    f.write(results[best_method])
