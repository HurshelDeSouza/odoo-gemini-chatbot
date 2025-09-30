from odoo import models, fields, api
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import logging
import base64

_logger = logging.getLogger(__name__)

class WhatsAppCampaign(models.Model):
    _name = 'gemini.whatsapp.campaign'
    _description = 'WhatsApp Campaign Management'

    name = fields.Char('Nombre de Campaña', required=True)
    product_name = fields.Char('Nombre del Producto', required=True)
    product_description = fields.Text('Descripción del Producto')
    excel_file = fields.Binary('Archivo Excel de Contactos', required=True)
    landing_page_url = fields.Char('URL Landing Page', compute='_compute_landing_url')
    message_template = fields.Text('Plantilla de Mensaje', required=True)
    
    @api.depends('name')
    def _compute_landing_url(self):
        for record in self:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            record.landing_page_url = f"{base_url}/product/landing/{record.id}"

    def _find_whatsapp_column(self, headers):
        """Busca una columna que pueda contener números de WhatsApp"""
        possible_names = ['whatsapp', 'Whatsapp', 'WhatsApp', 'WHATSAPP', 'telefono', 'teléfono', 
                         'celular', 'móvil', 'movil', 'phone', 'tel', 'número', 'numero', 
                         'contact', 'contacto', 'phone number', 'mobile', 'mobile number', 
                         'cell', 'cellular']
        
        # Limpiar y normalizar los encabezados
        headers_normalized = []
        for header in headers:
            # Mantener el encabezado original y agregar una versión normalizada
            headers_normalized.append(header.strip())  # Original
            # Versión normalizada
            clean_header = header.strip().lower()
            clean_header = clean_header.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            clean_header = ''.join(c for c in clean_header if c.isalnum() or c.isspace())
            if clean_header not in headers_normalized:
                headers_normalized.append(clean_header)
            
        _logger.info(f"Encabezados normalizados: {headers_normalized}")
        
        # Buscar coincidencias exactas primero
        for i, header in enumerate(headers_normalized):
            if header in possible_names:
                _logger.info(f"Coincidencia exacta encontrada: {header} en posición {i}")
                return i
        
        # Buscar coincidencias parciales
        for i, header in enumerate(headers_normalized):
            for name in possible_names:
                if name in header or header in name:
                    _logger.info(f"Coincidencia parcial encontrada: {header} contiene o está contenido en {name}, posición {i}")
                    return i
        
        _logger.warning(f"No se encontró columna de teléfono. Encabezados disponibles: {headers}")
        return -1

    def process_excel_file(self):
        """Procesa el archivo Excel y extrae los números de WhatsApp"""
        if not self.excel_file:
            raise ValueError(
                "No se ha cargado ningún archivo. Por favor, sube un archivo CSV con el siguiente formato:\n"
                "nombre,whatsapp,email\n"
                "Juan,573001234567,juan@email.com\n"
                "Maria,573007654321,maria@email.com"
            )
        
        try:
            _logger.info(f"Tipo de datos del archivo: {type(self.excel_file)}")
            _logger.info(f"Primeros 100 caracteres del archivo: {str(self.excel_file)[:100]}")
            
            # Decodificar el contenido del archivo
            try:
                # Primero intentamos decodificar directamente como base64
                file_content = base64.b64decode(self.excel_file)
                _logger.info("Archivo decodificado correctamente como base64")
                _logger.info(f"Primeros 100 caracteres después de base64: {file_content[:100]}")
            except Exception as e:
                _logger.error(f"Error al decodificar como base64: {str(e)}")
                # Si falla, asumimos que ya está en texto plano
                file_content = self.excel_file
                _logger.info("Usando contenido del archivo como texto plano")

            # Intentar decodificar el contenido como texto
            try:
                # Intentar diferentes codificaciones
                for encoding in ['utf-8', 'latin1', 'cp1252']:
                    try:
                        excel_content = file_content.decode(encoding)
                        _logger.info(f"Archivo decodificado correctamente usando {encoding}")
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError("No se pudo decodificar el contenido del archivo")
            except Exception as e:
                _logger.error(f"Error al decodificar el contenido: {str(e)}")
                raise ValueError("Error al leer el archivo. Asegúrate de que sea un archivo CSV válido.")

            # Dividir por líneas y filtrar líneas vacías
            lines = [line.strip() for line in excel_content.split('\n') if line.strip()]
            _logger.info(f"Contenido del archivo:\n{lines[:5]}")  # Log primeras 5 líneas
            
            if not lines:
                raise ValueError("El archivo está vacío")
            
            # Procesar el encabezado - intentar diferentes separadores
            separators = [';', ',', '\t']  # Primero intentamos con punto y coma
            headers = None
            sep_used = None
            
            for sep in separators:
                test_headers = lines[0].split(sep)
                if len(test_headers) > 1:  # Si encontramos más de una columna
                    headers = test_headers
                    sep_used = sep
                    _logger.info(f"Usando separador: {sep}")
                    break
            
            if not headers:
                raise ValueError(
                    "Formato de archivo no válido. El archivo debe ser CSV con columnas separadas por coma (,), punto y coma (;) o tabulación."
                )
            
            _logger.info(f"Encabezados encontrados: {headers}")
            whatsapp_index = self._find_whatsapp_column(headers)
            
            if whatsapp_index == -1:
                raise ValueError(
                    "No se encontró una columna para números de WhatsApp. El archivo debe tener una columna llamada:\n"
                    "'whatsapp', 'telefono', 'celular', 'móvil' o similar.\n\n"
                    "Formato esperado del archivo CSV:\n"
                    "nombre,whatsapp,email\n"
                    "Juan,573001234567,juan@email.com\n"
                    "Maria,573007654321,maria@email.com"
                )
            
            # Procesar las líneas restantes
            whatsapp_numbers = []
            for i, line in enumerate(lines[1:], start=2):
                _logger.info(f"Procesando línea {i}: {line}")
                columns = line.split(sep_used)
                if len(columns) > whatsapp_index:
                    raw_number = columns[whatsapp_index].strip()
                    _logger.info(f"Número encontrado en el archivo: {raw_number}")
                    
                    # Limpiar y validar el número
                    number = ''.join(filter(str.isdigit, raw_number))
                    _logger.info(f"Número después de limpiar: {number}")
                    
                    if number:
                        # Asegurarse de que el número tenga el formato correcto
                        if len(number) == 10:  # Número local (ej: 3001234567)
                            number = '57' + number
                            _logger.info(f"Número con código de país agregado: {number}")
                            whatsapp_numbers.append(number)
                        elif len(number) == 12 and number.startswith('57'):  # Número completo (ej: 573001234567)
                            _logger.info(f"Número ya tiene formato correcto: {number}")
                            whatsapp_numbers.append(number)
                        else:
                            _logger.warning(f"Número inválido encontrado: {number} (longitud: {len(number)})")
                    else:
                        _logger.warning(f"No se encontraron dígitos en: {raw_number}")
            
            if not whatsapp_numbers:
                _logger.error("No se encontraron números válidos en el archivo")
                _logger.error(f"Contenido del archivo:\n{lines}")
                raise ValueError(
                    "No se encontraron números de WhatsApp válidos en el archivo.\n"
                    "Los números deben tener uno de estos formatos:\n"
                    "1. Número local de 10 dígitos: 3001234567\n"
                    "2. Número completo de 12 dígitos con código de país: 573001234567\n\n"
                    "Por favor, verifica que los números en tu archivo:\n"
                    "- No contengan espacios, guiones o paréntesis\n"
                    "- No tengan el símbolo '+' al inicio\n"
                    "- Sean números de celular colombianos válidos"
                )
            
            _logger.info(f"Total de números procesados: {len(whatsapp_numbers)}")
            return whatsapp_numbers
            
        except Exception as e:
            _logger.error(f"Error al procesar el archivo: {str(e)}")
            raise ValueError(f"Error al procesar el archivo: {str(e)}")

    def send_whatsapp_messages(self):
        """Envía mensajes de WhatsApp a todos los contactos"""
        try:
            numbers = self.process_excel_file()
            total_numbers = len(numbers)
            _logger.info(f"Procesando {total_numbers} números de WhatsApp")
            
            success_count = 0
            failed_numbers = []
            
            for number in numbers:
                try:
                    # Formatear el mensaje
                    message = self.message_template.format(
                        product_name=self.product_name,
                        landing_url=self.landing_page_url
                    )
                    
                    # Log del envío
                    _logger.info(f"Enviando mensaje a: {number}")
                    _logger.info(f"Mensaje: {message}")
                    
                    # Por ahora, simulamos un envío exitoso
                    success_count += 1
                    
                    # Aquí iría la integración real con la API de WhatsApp
                    # Ejemplo de código para WhatsApp Business API:
                    # response = requests.post(
                    #     'https://graph.facebook.com/v12.0/YOUR_PHONE_NUMBER_ID/messages',
                    #     headers={'Authorization': f'Bearer {access_token}'},
                    #     json={
                    #         'messaging_product': 'whatsapp',
                    #         'to': number,
                    #         'type': 'text',
                    #         'text': {'body': message}
                    #     }
                    # )
                    
                except Exception as e:
                    _logger.error(f"Error enviando mensaje a {number}: {str(e)}")
                    failed_numbers.append(number)
            
            # Crear mensaje de resultado
            result_message = f"Mensajes enviados: {success_count} de {total_numbers}"
            if failed_numbers:
                result_message += f"\nFallaron: {len(failed_numbers)} números"
                _logger.error(f"Números fallidos: {failed_numbers}")
            
            # Mostrar mensaje al usuario
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Envío de mensajes WhatsApp',
                    'message': result_message,
                    'type': 'success' if not failed_numbers else 'warning',
                    'sticky': True,
                }
            }
            
        except Exception as e:
            _logger.error(f"Error en el proceso de envío: {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': f"Error al procesar el envío: {str(e)}",
                    'type': 'danger',
                    'sticky': True,
                }
            }

class ProductLead(models.Model):
    _name = 'gemini.product.lead'
    _description = 'Product Lead from Landing Page'

    name = fields.Char('Nombre', required=True)
    email = fields.Char('Email', required=True)
    phone = fields.Char('Teléfono', required=True)
    campaign_id = fields.Many2one('gemini.whatsapp.campaign', 'Campaña')
    date = fields.Datetime('Fecha', default=fields.Datetime.now)
    
    def export_to_drive(self):
        """Exporta los leads a Google Drive"""
        # Configuración de Google Drive
        creds = self._get_google_credentials()
        service = build('drive', 'v3', credentials=creds)
        
        # Crear DataFrame con los leads
        leads_data = self.search_read([])
        df = pd.DataFrame(leads_data)
        
        # Convertir a Excel
        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        
        # Subir a Drive
        file_metadata = {'name': 'Product_Leads.xlsx'}
        media = MediaIoBaseUpload(output, 
                                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                resumable=True)
        
        file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
        return file.get('id')
    
    def _get_google_credentials(self):
        """Obtiene las credenciales de Google Drive"""
        # Implementar la lógica de autenticación con Google
        # Esto dependerá de cómo quieras manejar las credenciales
        pass