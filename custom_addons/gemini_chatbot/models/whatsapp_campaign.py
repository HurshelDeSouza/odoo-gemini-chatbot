from odoo import models, fields, api
import logging
import base64

_logger = logging.getLogger(__name__)

class WhatsAppCampaign(models.Model):
    _name = 'gemini.whatsapp.campaign'
    _description = 'WhatsApp Campaign Management'

    name = fields.Char('Nombre de Campaña', required=True)
    product_name = fields.Char('Nombre del Producto', required=True)
    product_description = fields.Text('Descripción del Producto')
    excel_file = fields.Binary('Archivo Excel de Contactos', required=True, attachment=True)
    excel_filename = fields.Char('Nombre del Archivo')
    landing_page_url = fields.Char('URL Landing Page', compute='_compute_landing_url')
    message_template = fields.Text('Plantilla de Mensaje', required=True)
    
    # Control de envío
    max_messages_per_batch = fields.Integer('Máximo de Mensajes por Lote', default=25, 
                                           help='Cantidad máxima de mensajes a enviar de una vez (recomendado: 20-30)')
    delay_between_messages = fields.Integer('Delay entre Mensajes (segundos)', default=3,
                                           help='Tiempo de espera entre cada mensaje (recomendado: 2-5 segundos)')
    total_contacts = fields.Integer('Total de Contactos', compute='_compute_total_contacts', store=True)
    messages_sent = fields.Integer('Mensajes Enviados', default=0)
    messages_failed = fields.Integer('Mensajes Fallidos', default=0)
    last_send_date = fields.Datetime('Última Fecha de Envío')
    
    @api.depends('excel_file')
    def _compute_total_contacts(self):
        for record in self:
            if record.excel_file:
                try:
                    numbers = record.process_excel_file()
                    record.total_contacts = len(numbers)
                except:
                    record.total_contacts = 0
            else:
                record.total_contacts = 0
    
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
        """Procesa el archivo Excel/CSV y extrae los números de WhatsApp"""
        if not self.excel_file:
            raise ValueError(
                "No se ha cargado ningún archivo. Por favor, sube un archivo CSV con el siguiente formato:\n"
                "nombre,whatsapp,email\n"
                "Juan,573001234567,juan@email.com\n"
                "Maria,573007654321,maria@email.com"
            )
        
        try:
            _logger.info(f"Procesando archivo: {self.excel_filename}")
            _logger.info(f"Tipo de datos del archivo: {type(self.excel_file)}")
            
            # Decodificar el contenido del archivo desde base64
            try:
                file_content = base64.b64decode(self.excel_file)
                _logger.info("✅ Archivo decodificado correctamente desde base64")
                _logger.info(f"Tamaño del archivo: {len(file_content)} bytes")
            except Exception as e:
                _logger.error(f"❌ Error al decodificar base64: {str(e)}")
                raise ValueError(f"Error al leer el archivo: {str(e)}")

            # Intentar decodificar el contenido como texto con diferentes codificaciones
            excel_content = None
            encodings_to_try = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings_to_try:
                try:
                    excel_content = file_content.decode(encoding)
                    _logger.info(f"✅ Archivo decodificado correctamente usando {encoding}")
                    _logger.info(f"Primeras 200 caracteres: {excel_content[:200]}")
                    break
                except UnicodeDecodeError:
                    _logger.warning(f"No se pudo decodificar con {encoding}, intentando siguiente...")
                    continue
            
            if excel_content is None:
                raise ValueError("No se pudo decodificar el contenido del archivo. Asegúrate de que sea un archivo CSV válido en formato UTF-8 o Latin1.")

            # Dividir por líneas y filtrar líneas vacías
            lines = [line.strip() for line in excel_content.split('\n') if line.strip()]
            _logger.info(f"📄 Total de líneas en el archivo: {len(lines)}")
            _logger.info(f"📄 Primeras 5 líneas del archivo:\n{chr(10).join(lines[:5])}")
            
            if not lines:
                raise ValueError("El archivo está vacío. Por favor, sube un archivo CSV con datos.")
            
            if len(lines) < 2:
                raise ValueError("El archivo debe contener al menos una línea de encabezado y una línea de datos.")
            
            # Procesar el encabezado - intentar diferentes separadores
            separators = [',', ';', '\t', '|']
            headers = None
            sep_used = None
            
            for sep in separators:
                test_headers = [h.strip() for h in lines[0].split(sep)]
                if len(test_headers) > 1:  # Si encontramos más de una columna
                    headers = test_headers
                    sep_used = sep
                    _logger.info(f"✅ Separador detectado: '{sep}' (encontradas {len(headers)} columnas)")
                    break
            
            if not headers or len(headers) < 2:
                raise ValueError(
                    f"Formato de archivo no válido. El archivo debe ser CSV con columnas separadas por coma (,), punto y coma (;) o tabulación.\n\n"
                    f"Primera línea detectada: {lines[0][:100]}\n\n"
                    f"Formato esperado:\n"
                    f"nombre,whatsapp,email\n"
                    f"Juan,573001234567,juan@email.com"
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
            processed_count = 0
            skipped_count = 0
            
            for i, line in enumerate(lines[1:], start=2):
                if not line.strip():
                    continue
                    
                columns = [col.strip() for col in line.split(sep_used)]
                _logger.info(f"📱 Línea {i}: {len(columns)} columnas - {line[:100]}")
                
                if len(columns) <= whatsapp_index:
                    _logger.warning(f"⚠️ Línea {i} no tiene suficientes columnas (esperadas: {whatsapp_index + 1}, encontradas: {len(columns)})")
                    skipped_count += 1
                    continue
                
                raw_number = columns[whatsapp_index].strip()
                
                if not raw_number:
                    _logger.warning(f"⚠️ Línea {i}: columna de WhatsApp vacía")
                    skipped_count += 1
                    continue
                
                _logger.info(f"📞 Número original: '{raw_number}'")
                
                # Limpiar el número (remover espacios, guiones, paréntesis, +)
                number = ''.join(filter(str.isdigit, raw_number))
                _logger.info(f"🔢 Número limpio: '{number}'")
                    
                if not number:
                    _logger.warning(f"⚠️ Línea {i}: no se encontraron dígitos en '{raw_number}'")
                    skipped_count += 1
                    continue
                
                # Normalizar el número según el país
                formatted_number = None
                
                # Cuba: 8 dígitos sin código (ej: 53065305) -> agregar 53
                if len(number) == 8 and number[0] in ['5', '6', '7']:
                    formatted_number = '53' + number
                    _logger.info(f"🇨🇺 Cuba: {number} -> {formatted_number}")
                
                # Cuba: ya tiene código 53 (ej: 5353065305)
                elif len(number) == 10 and number.startswith('53'):
                    formatted_number = number
                    _logger.info(f"🇨🇺 Cuba (completo): {formatted_number}")
                
                # Colombia: 10 dígitos empezando con 3 (ej: 3001234567) -> agregar 57
                elif len(number) == 10 and number.startswith('3'):
                    formatted_number = '57' + number
                    _logger.info(f"🇨🇴 Colombia: {number} -> {formatted_number}")
                
                # Colombia: ya tiene código 57 (ej: 573001234567)
                elif len(number) == 12 and number.startswith('57'):
                    formatted_number = number
                    _logger.info(f"🇨🇴 Colombia (completo): {formatted_number}")
                
                # México: 10 dígitos -> agregar 52
                elif len(number) == 10 and not number.startswith('53'):
                    formatted_number = '52' + number
                    _logger.info(f"🇲🇽 México: {number} -> {formatted_number}")
                
                # Número internacional con código de país (10+ dígitos)
                elif len(number) >= 10:
                    formatted_number = number
                    _logger.info(f"🌍 Internacional: {formatted_number}")
                
                else:
                    _logger.warning(f"⚠️ Línea {i}: número inválido '{number}' (longitud: {len(number)})")
                    skipped_count += 1
                    continue
                
                if formatted_number:
                    whatsapp_numbers.append(formatted_number)
                    processed_count += 1
                    _logger.info(f"✅ Número agregado: {formatted_number}")
            
            _logger.info(f"📊 Resumen del procesamiento:")
            _logger.info(f"   - Total de líneas procesadas: {len(lines) - 1}")
            _logger.info(f"   - Números válidos: {processed_count}")
            _logger.info(f"   - Líneas omitidas: {skipped_count}")
            
            if not whatsapp_numbers:
                _logger.error("No se encontraron números válidos en el archivo")
                _logger.error(f"Contenido del archivo:\n{lines}")
                raise ValueError(
                    "No se encontraron números de WhatsApp válidos en el archivo.\n"
                    "Los números deben tener uno de estos formatos:\n"
                    "1. Cuba - 8 dígitos: 53065305 (se agrega código 53)\n"
                    "2. Cuba - completo: 5353065305\n"
                    "3. Colombia - 10 dígitos: 3001234567 (se agrega código 57)\n"
                    "4. Colombia - completo: 573001234567\n"
                    "5. Internacional: código de país + número\n\n"
                    "Por favor, verifica que los números en tu archivo:\n"
                    "- No contengan espacios, guiones o paréntesis\n"
                    "- No tengan el símbolo '+' al inicio\n"
                    "- Sean números de celular válidos"
                )
            
            _logger.info(f"Total de números procesados: {len(whatsapp_numbers)}")
            return whatsapp_numbers
            
        except Exception as e:
            _logger.error(f"Error al procesar el archivo: {str(e)}")
            raise ValueError(f"Error al procesar el archivo: {str(e)}")

    def send_whatsapp_messages(self):
        """Envía mensajes de WhatsApp a todos los contactos usando la API con control de límites"""
        from ..services.whatsapp_service import WhatsAppService
        import time
        
        try:
            # Inicializar servicio de WhatsApp
            whatsapp = WhatsAppService()
            
            # Verificar conexión
            status = whatsapp.check_status()
            if status['status'] != 'ready':
                raise ValueError(
                    "WhatsApp no está conectado. Por favor:\n"
                    "1. Ejecuta Iniciar-API.bat en la carpeta whatsapp-api\n"
                    "2. Escanea el código QR con WhatsApp\n"
                    "3. Espera a ver '✅ WhatsApp está listo!'"
                )
            
            # Procesar números del archivo
            numbers = self.process_excel_file()
            total_numbers = len(numbers)
            _logger.info(f"📊 Total de números a procesar: {total_numbers}")
            
            # Validar límite de seguridad
            if total_numbers > self.max_messages_per_batch:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': '⚠️ Límite de Seguridad',
                        'message': f"Tu archivo tiene {total_numbers} contactos, pero el límite configurado es {self.max_messages_per_batch}.\n\n"
                                 f"Para evitar bloqueos de WhatsApp:\n"
                                 f"1. Divide tu archivo en lotes más pequeños\n"
                                 f"2. O aumenta el límite en el campo 'Máximo de Mensajes por Lote'\n\n"
                                 f"Recomendación: No envíes más de 25-30 mensajes por hora.",
                        'type': 'warning',
                        'sticky': True,
                    }
                }
            
            # Advertencia si el número es alto
            if total_numbers > 30:
                _logger.warning(f"⚠️ ADVERTENCIA: Enviando {total_numbers} mensajes. Riesgo de bloqueo.")
            
            # Preparar mensaje
            message = self.message_template.format(
                product_name=self.product_name,
                landing_url=self.landing_page_url
            )
            
            _logger.info(f"⏱️ Delay configurado: {self.delay_between_messages} segundos entre mensajes")
            _logger.info(f"⏱️ Tiempo estimado: {(total_numbers * self.delay_between_messages) / 60:.1f} minutos")
            
            # Enviar mensajes uno por uno con control de delay
            sent = 0
            failed = 0
            results = []
            
            for i, phone in enumerate(numbers, 1):
                try:
                    _logger.info(f"📤 Enviando mensaje {i}/{total_numbers} a {phone}")
                    result = whatsapp.send_message(phone, message)
                    
                    if result.get('success'):
                        sent += 1
                        results.append({'phone': phone, 'success': True})
                        _logger.info(f"✅ Mensaje {i}/{total_numbers} enviado correctamente")
                    else:
                        failed += 1
                        results.append({'phone': phone, 'success': False, 'error': result.get('error')})
                        _logger.error(f"❌ Error en mensaje {i}/{total_numbers}: {result.get('error')}")
                    
                    # Delay entre mensajes (excepto en el último)
                    if i < total_numbers:
                        _logger.info(f"⏸️ Esperando {self.delay_between_messages} segundos...")
                        time.sleep(self.delay_between_messages)
                        
                except Exception as e:
                    failed += 1
                    results.append({'phone': phone, 'success': False, 'error': str(e)})
                    _logger.error(f"❌ Excepción en mensaje {i}/{total_numbers}: {str(e)}")
            
            # Actualizar estadísticas
            self.messages_sent = sent
            self.messages_failed = failed
            self.last_send_date = fields.Datetime.now()
            
            # Crear mensaje de resultado
            result_message = f"✅ Envío completado:\n\n"
            result_message += f"📤 Mensajes enviados: {sent} de {total_numbers}\n"
            
            if failed > 0:
                result_message += f"❌ Mensajes fallidos: {failed}\n"
            
            result_message += f"\n⏱️ Tiempo total: {(total_numbers * self.delay_between_messages) / 60:.1f} minutos"
            
            if sent > 0:
                result_message += f"\n\n💡 Recomendación: Espera al menos 1 hora antes de enviar más mensajes."
            
            _logger.info(f"📊 Resumen final: {sent} enviados, {failed} fallidos")
            
            # Mostrar mensaje al usuario
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '📱 Envío de Mensajes WhatsApp',
                    'message': result_message,
                    'type': 'success' if failed == 0 else 'warning',
                    'sticky': True,
                }
            }
            
        except Exception as e:
            _logger.error(f"❌ Error en el proceso de envío: {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '❌ Error',
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
    
    _sql_constraints = [
        ('phone_unique', 'UNIQUE(phone)', 'Este número de teléfono ya está registrado. Por favor, usa otro número.')
    ]
    
    def action_export_to_csv(self):
        """Exporta los leads seleccionados a CSV para usar en campañas de WhatsApp"""
        import csv
        import io
        from odoo.http import request
        
        # Crear CSV en memoria
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezados
        writer.writerow(['nombre', 'whatsapp', 'email'])
        
        # Escribir datos
        for lead in self:
            writer.writerow([lead.name, lead.phone, lead.email])
        
        # Obtener contenido
        csv_content = output.getvalue()
        output.close()
        
        # Crear archivo adjunto
        attachment = self.env['ir.attachment'].create({
            'name': f'leads_export_{fields.Datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            'type': 'binary',
            'datas': base64.b64encode(csv_content.encode('utf-8')),
            'mimetype': 'text/csv',
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }