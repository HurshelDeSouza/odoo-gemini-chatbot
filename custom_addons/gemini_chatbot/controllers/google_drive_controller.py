from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class GoogleDriveController(http.Controller):
    
    @http.route('/chatbot/google_drive_callback', type='http', auth='public', methods=['GET'])
    def google_drive_callback(self, **kwargs):
        """Handle Google Drive OAuth2 callback"""
        try:
            _logger.info(f"Google Drive callback received with params: {kwargs}")
            
            code = kwargs.get('code')
            error = kwargs.get('error')
            
            if error:
                return f"""
                <html>
                    <head><title>Error de Autorización</title></head>
                    <body>
                        <h2>Error de Autorización</h2>
                        <p>Error: {error}</p>
                        <p>Descripción: {kwargs.get('error_description', 'Error desconocido')}</p>
                        <script>window.close();</script>
                    </body>
                </html>
                """
            
            if not code:
                return """
                <html>
                    <head><title>Error</title></head>
                    <body>
                        <h2>Error</h2>
                        <p>No se recibió el código de autorización</p>
                        <script>window.close();</script>
                    </body>
                </html>
                """
            
            # Get active configuration
            config = request.env['chatbot.config'].sudo().search([('active', '=', True)], limit=1)
            
            if not config:
                return """
                <html>
                    <head><title>Error</title></head>
                    <body>
                        <h2>Error</h2>
                        <p>No se encontró configuración activa</p>
                        <script>window.close();</script>
                    </body>
                </html>
                """
            
            # Exchange code for tokens
            success = config.exchange_code_for_tokens(code)
            
            if success:
                return """
                <html>
                    <head><title>Autorización Exitosa</title></head>
                    <body>
                        <h2>¡Autorización Exitosa!</h2>
                        <p>Google Drive ha sido autorizado correctamente.</p>
                        <p>Ya puedes cerrar esta ventana y subir archivos a Google Drive.</p>
                        <script>
                            setTimeout(function() {
                                window.close();
                            }, 3000);
                        </script>
                    </body>
                </html>
                """
            else:
                return """
                <html>
                    <head><title>Error</title></head>
                    <body>
                        <h2>Error</h2>
                        <p>No se pudieron obtener los tokens de acceso</p>
                        <script>window.close();</script>
                    </body>
                </html>
                """
                
        except Exception as e:
            _logger.error(f"Error in Google Drive callback: {str(e)}")
            return f"""
            <html>
                <head><title>Error</title></head>
                <body>
                    <h2>Error Interno</h2>
                    <p>Error: {str(e)}</p>
                    <script>window.close();</script>
                </body>
            </html>
            """