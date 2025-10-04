const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

let client;
let isReady = false;

// Inicializar cliente de WhatsApp
function initializeWhatsApp() {
    client = new Client({
        authStrategy: new LocalAuth(),
        puppeteer: {
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        }
    });

    client.on('qr', (qr) => {
        console.log('📱 Escanea este código QR con WhatsApp:');
        qrcode.generate(qr, { small: true });
    });

    client.on('ready', () => {
        console.log('✅ WhatsApp está listo!');
        isReady = true;
    });

    client.on('authenticated', () => {
        console.log('✅ Autenticado correctamente');
    });

    client.on('auth_failure', () => {
        console.error('❌ Error de autenticación');
        isReady = false;
    });

    client.on('disconnected', (reason) => {
        console.log('❌ Cliente desconectado:', reason);
        isReady = false;
    });

    client.initialize();
}

// Endpoint de estado
app.get('/status', (req, res) => {
    res.json({
        status: isReady ? 'ready' : 'not_ready',
        message: isReady ? 'WhatsApp está conectado' : 'WhatsApp no está conectado'
    });
});

// Endpoint para enviar mensajes
app.post('/send-message', async (req, res) => {
    try {
        if (!isReady) {
            return res.status(503).json({
                success: false,
                error: 'WhatsApp no está conectado. Por favor escanea el código QR.'
            });
        }

        const { phone, message } = req.body;

        if (!phone || !message) {
            return res.status(400).json({
                success: false,
                error: 'Se requieren los campos "phone" y "message"'
            });
        }

        // Formatear número (agregar @c.us si no lo tiene)
        const chatId = phone.includes('@c.us') ? phone : `${phone}@c.us`;

        await client.sendMessage(chatId, message);

        res.json({
            success: true,
            message: 'Mensaje enviado correctamente',
            phone: phone
        });

    } catch (error) {
        console.error('Error al enviar mensaje:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Endpoint para enviar mensajes masivos
app.post('/send-bulk', async (req, res) => {
    try {
        if (!isReady) {
            return res.status(503).json({
                success: false,
                error: 'WhatsApp no está conectado'
            });
        }

        const { phones, message } = req.body;

        if (!phones || !Array.isArray(phones) || !message) {
            return res.status(400).json({
                success: false,
                error: 'Se requiere un array de "phones" y un "message"'
            });
        }

        const results = [];

        for (const phone of phones) {
            try {
                const chatId = phone.includes('@c.us') ? phone : `${phone}@c.us`;
                await client.sendMessage(chatId, message);
                results.push({ phone, success: true });
                
                // Esperar 2 segundos entre mensajes para evitar bloqueos
                await new Promise(resolve => setTimeout(resolve, 2000));
            } catch (error) {
                results.push({ phone, success: false, error: error.message });
            }
        }

        res.json({
            success: true,
            results: results,
            total: phones.length,
            sent: results.filter(r => r.success).length,
            failed: results.filter(r => !r.success).length
        });

    } catch (error) {
        console.error('Error en envío masivo:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`🚀 API de WhatsApp corriendo en http://localhost:${PORT}`);
    console.log('📱 Inicializando WhatsApp...');
    initializeWhatsApp();
});
