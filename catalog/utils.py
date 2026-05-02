from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageOps

MAX_IMAGE_SIZE = (1800, 1800)
JPEG_QUALITY = 88
PNG_COMPRESS_LEVEL = 6

def optimize_image_path(path: str | Path) -> None:
    """Resize and optimize uploaded images while keeping visual quality high."""
    file_path = Path(path)
    if not file_path.exists() or file_path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp'}:
        return

    try:
        with Image.open(file_path) as img:
            img = ImageOps.exif_transpose(img)
            original_format = (img.format or file_path.suffix.replace('.', '')).upper()
            if img.mode in ('RGBA', 'LA') and original_format in {'JPEG', 'JPG'}:
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')

            if img.width > MAX_IMAGE_SIZE[0] or img.height > MAX_IMAGE_SIZE[1]:
                img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

            save_kwargs = {'optimize': True}
            suffix = file_path.suffix.lower()

            if suffix in {'.jpg', '.jpeg'}:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                save_kwargs.update({'quality': JPEG_QUALITY, 'progressive': True})
                img.save(file_path, format='JPEG', **save_kwargs)
            elif suffix == '.png':
                save_kwargs.update({'compress_level': PNG_COMPRESS_LEVEL})
                img.save(file_path, format='PNG', **save_kwargs)
            elif suffix == '.webp':
                save_kwargs.update({'quality': 88, 'method': 6})
                img.save(file_path, format='WEBP', **save_kwargs)
    except Exception:
        return
