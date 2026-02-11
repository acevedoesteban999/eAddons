import base64
import io
import logging

_logger = logging.getLogger(__name__)

try:
    import aspose.zip as az
    ASPOSE_AVAILABLE = True
except ImportError:
    az = None
    ASPOSE_AVAILABLE = False
    _logger.debug("aspose-zip not installed. RAR to ZIP conversion disabled.")


def convert_rar_to_zip(binary_data):
    if not ASPOSE_AVAILABLE:
        _logger.warning("Cannot convert RAR to ZIP: 'aspose-zip' library not installed")
        return binary_data

    try:
        if isinstance(binary_data, str):
            rar_bytes = base64.b64decode(binary_data)
        else:
            rar_bytes = binary_data

        rar_buffer = io.BytesIO(rar_bytes)
        zip_buffer = io.BytesIO()

        with az.Archive() as zip_archive:
            with az.rar.RarArchive(rar_buffer) as rar:
                for i in range(rar.entries.length):
                    entry = rar.entries[i]
                    if not entry.is_directory:
                        ms = io.BytesIO()
                        entry.extract(ms)
                        ms.seek(0)
                        zip_archive.create_entry(entry.name, ms)
                    else:
                        zip_archive.create_entry(entry.name + "/", None)
            
            zip_archive.save(zip_buffer)
        
        zip_buffer.seek(0)
        return base64.b64encode(zip_buffer.getvalue())
        
    except Exception as e:
        _logger.error("Error converting RAR to ZIP: %s", e)
        return binary_data