from odoo import http
from odoo.http import request
import json
import base64
import logging

_logger = logging.getLogger(__name__)

class FileUploadController(http.Controller):
    
    @http.route('/chatbot/upload_excel', type='http', auth='public', methods=['POST'], csrf=False)
    def upload_excel_file(self, **kwargs):
        """Handle Excel file upload to Google Drive"""
        try:
            # Get uploaded file
            uploaded_file = request.httprequest.files.get('excel_file')
            
            if not uploaded_file:
                return json.dumps({
                    'success': False,
                    'error': 'No se ha seleccionado ningún archivo'
                })
            
            # Validate file type
            filename = uploaded_file.filename
            if not filename.lower().endswith(('.xlsx', '.xls')):
                return json.dumps({
                    'success': False,
                    'error': 'Solo se permiten archivos Excel (.xlsx, .xls)'
                })
            
            # Read file data
            file_data = uploaded_file.read()
            file_data_b64 = base64.b64encode(file_data).decode('utf-8')
            
            # Upload to Google Drive
            file_upload_model = request.env['chatbot.file.upload'].sudo()
            result = file_upload_model.upload_to_drive(filename, file_data_b64)
            
            return json.dumps(result)
            
        except Exception as e:
            _logger.error(f"Error in file upload controller: {str(e)}")
            return json.dumps({
                'success': False,
                'error': f'Error interno del servidor: {str(e)}'
            })
    
    @http.route('/chatbot/upload_status/<int:upload_id>', type='json', auth='public')
    def get_upload_status(self, upload_id):
        """Get upload status"""
        try:
            upload_record = request.env['chatbot.file.upload'].sudo().browse(upload_id)
            if not upload_record.exists():
                return {
                    'success': False,
                    'error': 'Registro de subida no encontrado'
                }
            
            return {
                'success': True,
                'status': upload_record.status,
                'filename': upload_record.filename,
                'drive_url': upload_record.drive_url,
                'error_message': upload_record.error_message
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }