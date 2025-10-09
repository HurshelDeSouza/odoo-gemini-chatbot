// JavaScript simple sin módulos de Odoo
(function() {
    'use strict';
    
    console.log('Landing page JS file loaded');
    
    // Función para inicializar
    function init() {
        console.log('Initializing landing page');
        console.log('jQuery available:', typeof $ !== 'undefined');
        console.log('Button exists:', $('#openFormBtn').length);
        console.log('Modal exists:', $('#orderModal').length);
        
        // Abrir modal
        $(document).on('click', '#openFormBtn', function(e) {
            e.preventDefault();
            console.log('Button clicked!');
            $('#orderModal').modal('show');
        });
        
        // Selección de paquetes
        $(document).on('click', '.package-option', function() {
            var packageNum = $(this).data('package');
            console.log('Package selected:', packageNum);
            
            $('.package-option').removeClass('selected');
            $(this).addClass('selected');
            
            var prices = {
                1: { subtotal: 89900, discount: 0, total: 89900 },
                2: { subtotal: 179800, discount: 59900, total: 119900 },
                3: { subtotal: 260700, discount: 100800, total: 159900 }
            };
            
            var price = prices[packageNum];
            $('#subtotal').text('$' + price.subtotal.toLocaleString('es-CO') + '.00');
            $('#discount').text('-$' + price.discount.toLocaleString('es-CO') + '.00');
            $('#total').text('$' + price.total.toLocaleString('es-CO') + '.00');
            $('#btnTotal').text('$' + price.total.toLocaleString('es-CO') + '.00');
            $('#selectedPackage').val('Paquete ' + packageNum);
        });
        
        // Envío prioritario
        $(document).on('change', 'input[name="priority_shipping"]', function() {
            var isChecked = $(this).is(':checked');
            var currentTotal = parseInt($('#total').text().replace(/[^0-9]/g, ''));
            var priorityCost = 5000;
            
            if (isChecked) {
                currentTotal += priorityCost;
            } else {
                currentTotal -= priorityCost;
            }
            
            $('#total').text('$' + currentTotal.toLocaleString('es-CO') + '.00');
            $('#btnTotal').text('$' + currentTotal.toLocaleString('es-CO') + '.00');
        });
        
        // Envío del formulario
        $(document).on('submit', '#leadForm', function(e) {
            e.preventDefault();
            console.log('Form submitted');
            
            var $form = $(this);
            var $submitBtn = $form.find('button[type="submit"]');
            var $messageDiv = $('#formMessage');

            var formData = {
                name: $form.find('input[name="name"]').val() + ' ' + $form.find('input[name="lastname"]').val(),
                email: $form.find('input[name="email"]').val() || 'No proporcionado',
                phone: $form.find('input[name="phone"]').val(),
                product_interest: $form.find('input[name="product_interest"]').val(),
                message: 'Departamento: ' + $form.find('select[name="department"]').val() + '\n' +
                         'Ciudad: ' + $form.find('input[name="city"]').val() + '\n' +
                         'Dirección: ' + $form.find('input[name="address"]').val() + '\n' +
                         'Barrio: ' + $form.find('input[name="neighborhood"]').val() + '\n' +
                         'Teléfono confirmación: ' + $form.find('input[name="phone_confirm"]').val() + '\n' +
                         'Envío prioritario: ' + ($form.find('input[name="priority_shipping"]').is(':checked') ? 'Sí' : 'No'),
            };

            if (formData.phone !== $form.find('input[name="phone_confirm"]').val()) {
                $messageDiv.html('<div class="alert alert-warning">Los números de teléfono no coinciden.</div>');
                return;
            }

            $submitBtn.prop('disabled', true).html('<i class="fa fa-spinner fa-spin"></i> Procesando pedido...');

            $.ajax({
                url: '/landing/submit',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: formData
                }),
                success: function(result) {
                    if (result.result && result.result.success) {
                        $messageDiv.html('<div class="alert alert-success"><i class="fa fa-check-circle"></i> ' + result.result.message + '</div>');
                        $form[0].reset();
                        
                        setTimeout(function() {
                            $('#orderModal').modal('hide');
                            $messageDiv.html('');
                        }, 3000);
                    } else {
                        $messageDiv.html('<div class="alert alert-danger"><i class="fa fa-exclamation-triangle"></i> Error al enviar el formulario.</div>');
                    }
                },
                error: function(error) {
                    $messageDiv.html('<div class="alert alert-danger"><i class="fa fa-exclamation-triangle"></i> Error al enviar el formulario.</div>');
                    console.error('Error:', error);
                },
                complete: function() {
                    $submitBtn.prop('disabled', false).html('<i class="fa fa-shopping-cart"></i> PEDIR CONTRAENTREGA - ' + $('#btnTotal').text());
                }
            });
        });
    }
    
    // Esperar a que el DOM y jQuery estén listos
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof $ !== 'undefined') {
                $(document).ready(init);
            }
        });
    } else {
        if (typeof $ !== 'undefined') {
            $(document).ready(init);
        }
    }
})();
