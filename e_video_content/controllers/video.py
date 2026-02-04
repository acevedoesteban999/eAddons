import os
import re
from wsgiref.util import FileWrapper
from odoo import http
from odoo.http import request, Response

class VideoStreamController(http.Controller):
    
    CHUNK_SIZE = 256 * 1024
    
    @http.route('/e_design_website/video/stream/<int:video_id>', type='http', auth='user')
    def stream_video(self, video_id, **kwargs):
        record = request.env['e_design_website.video.content'].browse(video_id)
        
        if not record.exists():
            return request.not_found()
        
        attachment = request.env['ir.attachment'].sudo().search([
            ('res_model', '=', record._name),
            ('res_id', '=', record.id),
            ('res_field', '=', 'video_data')
        ], limit=1)
        
        if not attachment or not attachment.store_fname:
            return request.not_found()
        
        file_path = attachment._full_path(attachment.store_fname)
        file_size = os.path.getsize(file_path)
        
        range_header = request.httprequest.headers.get('Range', '')
        start, end = 0, file_size - 1
        
        if range_header:
            match = re.match(r'bytes=(\d+)-(\d*)', range_header)
            if match:
                start = int(match.group(1))
                end = min(int(match.group(2)) if match.group(2) else file_size - 1, file_size - 1)
        
        content_length = end - start + 1
        
        file_handle = open(file_path, 'rb')
        file_handle.seek(start)
        
        wrapper = FileWrapper(file_handle, blksize=self.CHUNK_SIZE)
        
        headers = [
            ('Content-Type', attachment.mimetype or 'video/mp4'),
            ('Accept-Ranges', 'bytes'),
            ('Content-Length', str(content_length)),
            ('Cache-Control', 'private, max-age=3600'),
            ('ETag', f'"{attachment.checksum}"' if attachment.checksum else ''),
        ]
        
        status = 206 if range_header else 200
        if range_header:
            headers.append(('Content-Range', f'bytes {start}-{end}/{file_size}'))
        
        response = Response(wrapper, status=status, headers=headers, direct_passthrough=True)
        response.call_on_close(file_handle.close)
        return response