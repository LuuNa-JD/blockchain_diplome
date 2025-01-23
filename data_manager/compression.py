import zlib


def compress_data(data):
    """
    Compresse les données en utilisant zlib.
    """
    compressed = zlib.compress(data)
    if len(compressed) >= len(data):
        return b"NOC" + data
    return b"CMP" + compressed


def decompress_data(data):
    """
    Décompresse les données en utilisant zlib.
    """
    if data[:3] == b"CMP":  # Données compressées
        return zlib.decompress(data[3:])
    elif data[:3] == b"NOC":  # Données non compressées
        return data[3:]
    else:
        raise ValueError("Format de données non reconnu.")
