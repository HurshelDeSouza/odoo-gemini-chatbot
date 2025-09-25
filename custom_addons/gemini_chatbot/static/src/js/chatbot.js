/* Backend Chatbot JavaScript */
odoo.define('gemini_chatbot.chatbot', function (require) {
    'use strict';

    var core = require('web.core');
    var FormController = require('web.FormController');
    var ListView = require('web.ListView');

    var _t = core._t;

    // Extend Form Controller for chatbot configuration
    FormController.include({
        _onButtonClicked: function (event) {
            if (event.data.attrs.name === 'test_connection') {
                this._testChatbotConnection();
                return;
            }
            return this._super.apply(this, arguments);
        },

        _testChatbotConnection: function () {
            var self = this;
            this._rpc({
                model: 'chatbot.config',
                method: 'test_connection',
                args: [this.handle.data.id],
            }).then(function (result) {
                if (result && result.params) {
                    self.displayNotification({
                        title: result.params.title,
                        message: result.params.message,
                        type: result.params.type,
                    });
                }
            });
        },
    });

    // Add some utility functions for token usage visualization
    var ChatbotUtils = {
        formatTokens: function (tokens) {
            if (tokens > 1000000) {
                return (tokens / 1000000).toFixed(1) + 'M';
            } else if (tokens > 1000) {
                return (tokens / 1000).toFixed(1) + 'K';
            }
            return tokens.toString();
        },

        getTokenUsageColor: function (tokens, maxTokens) {
            var ratio = tokens / maxTokens;
            if (ratio < 0.5) return '#28a745';
            if (ratio < 0.8) return '#ffc107';
            return '#dc3545';
        }
    };

    return {
        ChatbotUtils: ChatbotUtils
    };
});