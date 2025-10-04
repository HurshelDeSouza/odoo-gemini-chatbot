// Script de prueba para verificar la API de WhatsApp
const http = require('http');

console.log('🔍 Verificando API de WhatsApp...\n');

// Test 1: Verificar estado
const options = {
    hostname: 'localhost',
    port: 3000,
    path: '/status',
    method: 'GET'
};

const req = http.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        try {
            const result = JSON.parse(data);
            console.log('✅ API está corriendo');
            console.log('📊 Estado:', result);
            
            if (result.status === 'ready') {
                console.log('\n✅ WhatsApp está conectado y listo!');
                console.log('\n🚀 Puedes enviar mensajes desde Odoo');
            } else {
                console.log('\n⚠️  WhatsApp NO está conectado');
                console.log('📱 Por favor escanea el código QR');
            }
        } catch (e) {
            console.log('❌ Error al parsear respuesta:', e.message);
        }
    });
});

req.on('error', (error) => {
    console.log('❌ No se pudo conectar con la API');
    console.log('💡 Asegúrate de que la API esté corriendo:');
    console.log('   1. Ejecuta: Iniciar-API.bat');
    console.log('   2. O ejecuta: npm run api');
    console.log('\n📝 Error:', error.message);
});

req.end();
