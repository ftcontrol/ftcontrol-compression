import lzma
import zlib
import bz2
import brotli
import lz4.frame
import zstandard as zstd


def bytes_to_mb(size_bytes: int) -> float:
    return size_bytes / (1024 * 1024)


def compress_lzma(data: bytes) -> bytes:
    return lzma.compress(data)


def compress_zlib(data: bytes) -> bytes:
    return zlib.compress(data, level=9)


def compress_bz2(data: bytes) -> bytes:
    return bz2.compress(data, compresslevel=9)


def compress_brotli(data: bytes) -> bytes:
    return brotli.compress(data, quality=11)


def compress_lz4(data: bytes) -> bytes:
    return lz4.frame.compress(data, compression_level=16)


def compress_zstd(data: bytes) -> bytes:
    cctx = zstd.ZstdCompressor(level=22)
    return cctx.compress(data)


with open("data.json", "r", encoding="utf-8") as f:
    text = f.read()

input_bytes = text.encode("utf-8")
input_size = len(input_bytes)

results = {}

results['LZMA'] = compress_lzma(input_bytes)
results['Zlib'] = compress_zlib(input_bytes)
results['Bz2'] = compress_bz2(input_bytes)
results['Brotli'] = compress_brotli(input_bytes)
results['LZ4'] = compress_lz4(input_bytes)
results['Zstandard'] = compress_zstd(input_bytes)

print(
    f"Original size: {input_size} bytes ({bytes_to_mb(input_size):.4f} MB)\n")

best_method = None
best_size = None

for method, compressed_data in results.items():
    compressed_size = len(compressed_data)
    saved_bytes = input_size - compressed_size
    saved_percent = (saved_bytes / input_size) * 100 if input_size > 0 else 0
    print(f"{method} compressed size: {compressed_size} bytes ({bytes_to_mb(compressed_size):.4f} MB)")
    print(f"Saved: {saved_bytes} bytes ({saved_percent:.2f}%)\n")

    if best_size is None or compressed_size < best_size:
        best_size = compressed_size
        best_method = method

print(
    f"Best compression method: {best_method} with size {best_size} bytes ({bytes_to_mb(best_size):.4f} MB)")

with open(f"compressed_best.{best_method.lower()}", "wb") as f:
    f.write(results[best_method])
