# -*- coding: utf-8 -*-
import requests
import logging

_logger = logging.getLogger(__name__)


class WhatsAppService:
    """Servicio para integración con WhatsApp API"""
    
    def __init__(self, api_url="http://host.docker.internal:3000"):
        """
        Inicializa el servicio de WhatsApp
        
        Args:
            api_url: URL de la API de WhatsApp (usar host.docker.internal para Docker)
        """
        self.api_url = api_url.rstrip('/')
        
    def check_status(self):
        """
        Verifica el estado de la conexión con WhatsApp
        
        Returns:
            dict: Estado de la conexión
        """
        try:
            response = requests.get(f"{self.api_url}/status", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            _logger.error(f"Error al verificar estado de WhatsApp: {str(e)}")
            return {
                'status': 'error',
                'message': f'No se pudo conectar con la API: {str(e)}'
            }
    
    def send_message(self, phone, message):
        """
        Envía un mensaje de WhatsApp a un número
        
        Args:
            phone: Número de teléfono (formato: 5215512345678)
            message: Mensaje a enviar
            
        Returns:
            dict: Resultado del envío
        """
        try:
            # Verificar que el número tenga el formato correcto
            phone = str(phone).strip()
            if not phone:
                raise ValueError("El número de teléfono no puede estar vacío")
            
            payload = {
                'phone': phone,
                'message': message
            }
            
            _logger.info(f"Enviando mensaje a {phone}")
            response = requests.post(
                f"{self.api_url}/send-message",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                _logger.info(f"Mensaje enviado exitosamente a {phone}")
            else:
                _logger.error(f"Error al enviar mensaje a {phone}: {result.get('error')}")
                
            return result
            
        except requests.exceptions.Timeout:
            error_msg = "Timeout al enviar mensaje"
            _logger.error(f"{error_msg} a {phone}")
            return {'success': False, 'error': error_msg}
            
        except requests.exceptions.ConnectionError:
            error_msg = "No se pudo conectar con la API de WhatsApp. Verifica que esté corriendo."
            _logger.error(error_msg)
            return {'success': False, 'error': error_msg}
            
        except Exception as e:
            error_msg = f"Error al enviar mensaje: {str(e)}"
            _logger.error(f"{error_msg} a {phone}")
            return {'success': False, 'error': error_msg}
    
    def send_bulk_messages(self, phones, message):
        """
        Envía mensajes masivos de WhatsApp
        
        Args:
            phones: Lista de números de teléfono
            message: Mensaje a enviar
            
        Returns:
            dict: Resultado del envío masivo
        """
        try:
            if not phones or not isinstance(phones, list):
                raise ValueError("Se requiere una lista de números de teléfono")
            
            payload = {
                'phones': phones,
                'message': message
            }
            
            _logger.info(f"Enviando mensajes masivos a {len(phones)} números")
            response = requests.post(
                f"{self.api_url}/send-bulk",
                json=payload,
                timeout=len(phones) * 5  # 5 segundos por mensaje
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('success'):
                _logger.info(
                    f"Envío masivo completado: {result.get('sent')} enviados, "
                    f"{result.get('failed')} fallidos"
                )
            
            return result
            
        except Exception as e:
            error_msg = f"Error en envío masivo: {str(e)}"
            _logger.error(error_msg)
            return {'success': False, 'error': error_msg}
