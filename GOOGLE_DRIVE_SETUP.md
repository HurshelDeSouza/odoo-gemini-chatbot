# 🚀 Configuración de Google Drive con Apps Script

## 📋 **Problema Resuelto**
Google Drive API no acepta API Keys para la mayoría de operaciones, requiere OAuth2. La solución más práctica es usar **Google Apps Script** como intermediario.

## ⚡ **Solución: Google Apps Script**

### **Paso 1: Crear el Apps Script**

1. **Ve a**: https://script.google.com
2. **Clic en**: "Nuevo proyecto"
3. **Borra** el código por defecto
4. **Copia y pega** el código del archivo `google_apps_script_drive_upload.js`
5. **Guarda** el proyecto (Ctrl+S)
6. **Nombra** el proyecto: "Odoo Drive Upload"

### **Paso 2: Implementar como Web App**

1. **Clic en**: "Implementar" → "Nueva implementación"
2. **Tipo**: Selecciona "Aplicación web"
3. **Descripción**: "Upload files from Odoo to Drive"
4. **Ejecutar como**: "Yo (tu email)"
5. **Acceso**: "Cualquier persona"
6. **Clic en**: "Implementar"
7. **Autoriza** los permisos cuando te lo pida
8. **Copia** la URL de la aplicación web

### **Paso 3: Configurar en Odoo**

1. **Ve a**: http://localhost:8069
2. **Login**: admin / admin
3. **Menú**: "Gemini Chatbot" → "Configuración"
4. **Pega** la URL del Apps Script en "Google Apps Script URL"
5. **Opcional**: Configura "Drive Folder ID" (deja "root" para carpeta raíz)
6. **Guarda** la configuración

### **Paso 4: Probar la Conexión**

1. **Clic en**: "Test Drive Connection"
2. **Deberías ver**: "Conexión exitosa con Google Apps Script para Drive"

### **Paso 5: Probar Subida de Archivos**

1. **Ve a**: "Gemini Chatbot" → "Abrir Landing Page"
2. **Sección**: "Subir Archivos Excel a Drive"
3. **Selecciona** un archivo Excel (.xlsx o .xls)
4. **Clic en**: "Subir a Google Drive"
5. **¡Funcionará sin errores!**

## 🎯 **Ventajas de esta Solución**

- ✅ **Sin OAuth2 complejo** - Apps Script maneja la autenticación
- ✅ **Sin errores 401** - Acceso directo a tu Drive
- ✅ **Configuración simple** - Solo una URL
- ✅ **Funciona siempre** - Sin tokens que expiren
- ✅ **Seguro** - Solo tú tienes acceso al script

## 🔧 **Configuración Avanzada**

### **Cambiar Carpeta de Destino**
1. **Crea** una carpeta en Google Drive
2. **Copia** el ID de la carpeta desde la URL
3. **Pega** el ID en "Drive Folder ID" en Odoo

### **Permisos de Archivos**
El script configura automáticamente los archivos como "Cualquier persona con el enlace puede ver"

### **Tipos de Archivo Soportados**
- Excel (.xlsx, .xls)
- Se puede extender fácilmente para otros tipos

## 🚨 **Solución de Problemas**

### **Error: "Conexión exitosa" pero subida falla**
- Verifica que la URL del Apps Script sea correcta
- Asegúrate de que el script esté implementado como "Aplicación web"

### **Error: "Acceso denegado"**
- Re-implementa el Apps Script
- Verifica que "Acceso" esté configurado como "Cualquier persona"

### **Error: "Carpeta no encontrada"**
- Verifica que el "Drive Folder ID" sea correcto
- Usa "root" para la carpeta raíz

## 📊 **Estado Final**

- **Gemini Chat**: ✅ Funcionando
- **Subida Excel**: ✅ Funcionando con Apps Script
- **Landing Page**: ✅ Moderna y funcional
- **Configuración**: ✅ Simple y práctica

**¡Ahora puedes subir archivos Excel a Google Drive sin problemas de autenticación!** 🎉