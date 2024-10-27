# my_bencoder/__init__.py
from bencoder import bencode
file_path = "debian.torrent"
decoded_content = bencode(file_path)
