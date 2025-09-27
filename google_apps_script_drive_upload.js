/**
 * Google Apps Script para subir archivos a Google Drive desde Odoo
 *
 * INSTRUCCIONES DE CONFIGURACIÓN:
 * 1. Ve a https://script.google.com
 * 2. Crea un nuevo proyecto
 * 3. Pega este código
 * 4. Guarda el proyecto
 * 5. Ve a "Implementar" > "Nueva implementación"
 * 6. Tipo: "Aplicación web"
 * 7. Ejecutar como: "Yo"
 * 8. Acceso: "Cualquier persona"
 * 9. Copia la URL de la aplicación web
 * 10. Pega esa URL en la configuración de Odoo
 */

function doPost(e) {
  try {
    // Parse JSON data
    const data = JSON.parse(e.postData.contents);

    // Handle different actions
    switch (data.action) {
      case "test":
        return handleTest(data);
      case "upload":
        return handleUpload(data);
      default:
        return ContentService.createTextOutput(
          JSON.stringify({
            success: false,
            error: "Acción no válida",
          })
        ).setMimeType(ContentService.MimeType.JSON);
    }
  } catch (error) {
    return ContentService.createTextOutput(
      JSON.stringify({
        success: false,
        error: error.toString(),
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function handleTest(data) {
  try {
    // Test access to Drive
    const folderId = data.folderId || "root";

    // Try to access the folder
    if (folderId !== "root") {
      DriveApp.getFolderById(folderId);
    }

    return ContentService.createTextOutput(
      JSON.stringify({
        success: true,
        message: "Conexión exitosa con Google Drive",
      })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(
      JSON.stringify({
        success: false,
        error: "Error accediendo a Google Drive: " + error.toString(),
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function handleUpload(data) {
  try {
    // Validate required fields
    if (!data.filename || !data.fileData) {
      throw new Error("Faltan datos del archivo");
    }

    // Decode base64 file data
    const fileBlob = Utilities.newBlob(
      Utilities.base64Decode(data.fileData),
      data.mimeType || "application/octet-stream",
      data.filename
    );

    // Get target folder
    let folder;
    if (data.folderId && data.folderId !== "root") {
      folder = DriveApp.getFolderById(data.folderId);
    } else {
      folder = DriveApp.getRootFolder();
    }

    // Create file in Drive
    const file = folder.createFile(fileBlob);

    // Make file publicly viewable (optional)
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

    return ContentService.createTextOutput(
      JSON.stringify({
        success: true,
        fileId: file.getId(),
        fileUrl: file.getUrl(),
        fileName: file.getName(),
        message: "Archivo subido exitosamente",
      })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(
      JSON.stringify({
        success: false,
        error: "Error subiendo archivo: " + error.toString(),
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

// Handle GET requests (for testing)
function doGet(e) {
  return(
    JSON.stringify({
      success: true,
      message: "Google Apps Script para Odoo Drive Upload está funcionando",
      timestamp: new Date().toISOString(),
    })
  ).setMimeType(ContentService.MimeType.JSON);
}
