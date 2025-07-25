import lzma
import base64

with open("data.json", "r", encoding="utf-8") as f:
    text = f.read()

input_bytes = text.encode("utf-8")
input_size = len(input_bytes)

compressed_bytes = lzma.compress(input_bytes)
compressed_size = len(compressed_bytes)

compressed_b64 = base64.b64encode(compressed_bytes).decode("ascii")

saved_bytes = input_size - compressed_size
saved_percent = (saved_bytes / input_size) * 100 if input_size > 0 else 0

print(f"Original size: {input_size} bytes")
print(f"Compressed size: {compressed_size} bytes")
print(f"Saved: {saved_bytes} bytes ({saved_percent:.2f}%)")

with open("compressed.txt", "w", encoding="utf-8") as f:
    f.write(compressed_b64)
