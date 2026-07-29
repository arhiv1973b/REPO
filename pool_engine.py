import hashlib
import json
import os
import tarfile
from datetime import datetime

# Параметры контура
SOURCE_STREAM_DIR = "./incoming_stream"
MASTER_REGISTRY = "./master_registry.json"

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def compile_linear_pool():
    timestamp = datetime.utcnow().isoformat()
    
    if not os.path.exists(SOURCE_STREAM_DIR):
        os.makedirs(SOURCE_STREAM_DIR)
        
    # Сборка потока в единый tar-контур без разрывов
    archive_name = f"linear_pool_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.tar"
    archive_path = os.path.join(SOURCE_STREAM_DIR, archive_name)
    
    with tarfile.open(archive_path, "w") as tar:
        for root, dirs, files in os.walk(SOURCE_STREAM_DIR):
            for file in files:
                if file.endswith(".tar"):
                    continue
                full_path = os.path.join(root, file)
                tar.add(full_path, arcname=file)
                
    # Верификация хэша готового пула
    pool_hash = calculate_sha256(archive_path)
    
    registry_entry = {
        "timestamp": timestamp,
        "archive": archive_name,
        "sha256": pool_hash,
        "status": "verified_linear_pool"
    }
    
    # Запись в мастер-реестр с поддержкой гибридной структуры
    if os.path.exists(MASTER_REGISTRY):
        with open(MASTER_REGISTRY, "r", encoding="utf-8") as f:
            try:
                content = json.load(f)
                if isinstance(content, list):
                    data = content
                else:
                    data = [content]
            except Exception:
                data = []
    else:
        data = []
        
    data.append(registry_entry)
    with open(MASTER_REGISTRY, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"[{timestamp}] Линейный пул успешно сформирован. Хэш: {pool_hash}")

if __name__ == "__main__":
    compile_linear_pool()
