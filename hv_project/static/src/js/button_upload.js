odoo.define('hv_project.button_upload', function (require) {
'use strict';
var core = require('web.core');
var ajax = require('web.ajax');
var qweb = core.qweb;
ajax.loadXML('/hv_project/static/src/xml/button_upload.xml', qweb);
});