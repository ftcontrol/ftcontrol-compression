import lzma


def bytes_to_mb(size_bytes: int) -> float:
    return size_bytes / (1024 * 1024)


with open("data.json", "r", encoding="utf-8") as f:
    text = f.read()

input_bytes = text.encode("utf-8")
input_size = len(input_bytes)

compressed_bytes = lzma.compress(input_bytes)
compressed_size = len(compressed_bytes)

saved_bytes = input_size - compressed_size
saved_percent = (saved_bytes / input_size) * 100 if input_size > 0 else 0

print(f"Original size: {input_size} bytes ({bytes_to_mb(input_size):.4f} MB)")
print(
    f"Compressed size: {compressed_size} bytes ({bytes_to_mb(compressed_size):.4f} MB)")
print(f"Saved: {saved_bytes} bytes ({saved_percent:.2f}%)")

with open("compressed.lzma", "wb") as f:
    f.write(compressed_bytes)
