#!/bin/sh

# Параметры контура для Alpine Linux / iSH
SOURCE_STREAM_DIR="./incoming_stream"
MASTER_REGISTRY="./master_registry.json"
TIMESTAMP=$(date -u +"%Y%m%d_%H%M%S")

ARCHIVE_NAME="linear_pool_${TIMESTAMP}.tar"
ARCHIVE_PATH="${SOURCE_STREAM_DIR}/${ARCHIVE_NAME}"

# Убедиться, что директория существует
mkdir -p "$SOURCE_STREAM_DIR"

# 1. Потоковая сборка tar-архива без проприетарных заголовков
tar -cvf "$ARCHIVE_PATH" -C "$SOURCE_STREAM_DIR" . --exclude="*.tar" 2>/dev/null

# 2. Атомарная генерация хэша через стандартный sha256sum
if [ -f "$ARCHIVE_PATH" ]; then
    POOL_HASH=$(sha256sum "$ARCHIVE_PATH" | awk '{print $1}')
    
    # 3. Регистрация в мастер-реестре (JSON)
    ENTRY="  {\n    \"timestamp\": \"$TIMESTAMP\",\n    \"archive\": \"$ARCHIVE_NAME\",\n    \"sha256\": \"$POOL_HASH\",\n    \"status\": \"verified_linear_pool_ish\"\n  }"
    
    if [ ! -f "$MASTER_REGISTRY" ]; then
        printf "[\n%b\n]\n" "$ENTRY" > "$MASTER_REGISTRY"
    else
        sed -i '$ d' "$MASTER_REGISTRY"
        if grep -q "{" "$MASTER_REGISTRY"; then
            echo "," >> "$MASTER_REGISTRY"
        fi
        printf "%b\n]\n" "$ENTRY" >> "$MASTER_REGISTRY"
    fi
    
    echo "[$TIMESTAMP] Линейный пул успешно сформирован в iSH. Хэш: $POOL_HASH"
else
    echo "Ошибка: Не удалось сформировать архивный поток в директории $SOURCE_STREAM_DIR" >&2
    exit 1
fi
