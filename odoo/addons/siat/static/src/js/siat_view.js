odoo.define('siat_view.SiatView', function (require) {
	"use strict";

	var AbstractController = require('web.AbstractController');
	var AbstractModel = require('web.AbstractModel');
	var AbstractRenderer = require('web.AbstractRenderer');
	var AbstractView = require('web.AbstractView');
	var viewRegistry = require('web.view_registry');
	var SiatViewController = AbstractController.extend({});
	var SiatViewRenderer = AbstractRenderer.extend({
		className: "o_siat_view",
		on_attach_callback: function () 
		{
			this.isInDOM = true;
			//this._renderMap();
		},
		_render: function () 
		{
			if (this.isInDOM) {
				//this._renderMarkers();
				return $.when();
			}
			//console.log('SiatViewRenderer._render.state', this.state);
			//console.log('SiatViewRenderer._render.view', this.state.view);
			let tag = '<siat-sync />';
			if( this.state.view == 'cufds' )
				tag = '<siat-cufd-listing />';
			else if( this.state.view == 'pos' )
				tag = '<siat-puntos-venta />';
			else if( this.state.view == 'events' )
				tag = '<siat-eventos />';
			else if( this.state.view == 'invoices' )
				tag = '<siat-invoice-listing />';
			else if( this.state.view == 'invoicer' )
				tag = '<siat-invoicer />';
			else if( this.state.view == 'config' )
			    tag = '<siat-config />';

			this.$el.append(
				$(`<div id="siat-app">${tag}</div>`)
				//$('<script>loadSiatApp("#siat-app", [], "es");</script>')
			);
			setTimeout(function()
			{
				//console.log('Loading Vue APP');
				loadSiatApp("#siat-app", [], "es");
			}, 800);
			return $.when();
		},
	});
	var SiatViewModel = AbstractModel.extend({
		get: function () 
		{
			return {view: this.view};
		},
		load: function (params) {
			this.view = params.view;
			return this._load(params);
		},
		reload: function (id, params) {
			return this._load(params);
		},
		_load: function (params) 
		{
			this.domain = params.domain || this.domain || [];
			if ( this.view == 'cufds' ) 
			{
				var self = this;
				return this._rpc({
					model: 'res.partner',
					method: 'search_read',
					fields: ['id','name','partner_latitude', 'partner_longitude'],
					domain: this.domain,
				})
				.then(function (result) {
					//self.contacts = result;
				});
			}
			//this.contacts = [];
			return $.when();
		},
	});
	var KanbanView = require('web.KanbanView')
	
	var SiatView = AbstractView.extend({
		config: _.extend({}, KanbanView.prototype.config, {
			Model: SiatViewModel,
			Controller: SiatViewController,
			Renderer: SiatViewRenderer,
			withControlPanel: false,
			withSearchPanel: false
		}),
		cssLibs: [
			//'/hello_world_view/static/lib/leaflet/leaflet.css'
		],
		jsLibs: [
			//'https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js',
			'https://cdn.jsdelivr.net/npm/vue@2.7.13',
			'/siat/static/src/js/siat/config.js',
			'/siat/static/src/js/siat/plugins/processing.js',
			'/siat/static/src/js/siat/plugins/toast.js',
			'/siat/static/src/js/siat/siat-config.js',
			'/siat/static/src/js/siat/models/Model.js',
			'/siat/static/src/js/siat/models/invoice.js',
			'/siat/static/src/js/siat/models/evento.js',
			'/siat/static/src/js/siat/models/User.js',
			'/siat/static/src/js/siat/functions.js',
			'/siat/static/src/js/siat/api.js',
			'/siat/static/src/js/siat/mixins/mixin-common.js',
			'/siat/static/src/js/siat/mixins/mixin-events.js',
			'/siat/static/src/js/siat/service-config.js',
			'/siat/static/src/js/siat/service-branches.js',
			'/siat/static/src/js/siat/service-pos.js',
			'/siat/static/src/js/siat/service-invoices.js',
			'/siat/static/src/js/siat/service-customers.js',
			'/siat/static/src/js/siat/service-products.js',
			'/siat/static/src/js/siat/service-events.js',
			'/siat/static/src/js/siat/components/sync-actividades.js',
			'/siat/static/src/js/siat/components/sync-actividades-documento-sector.js',
			'/siat/static/src/js/siat/components/sync-anulacion.js',
			'/siat/static/src/js/siat/components/sync-documentos-identidad.js',
			'/siat/static/src/js/siat/components/sync-eventos.js',
			'/siat/static/src/js/siat/components/sync-leyendas.js',
			'/siat/static/src/js/siat/components/sync-productos-servicios.js',
			'/siat/static/src/js/siat/components/sync-tipos-documento-sector.js',
			'/siat/static/src/js/siat/components/sync-tipos-emision.js',
			'/siat/static/src/js/siat/components/sync-tipos-factura.js',
			'/siat/static/src/js/siat/components/sync-tipos-habitacion.js',
			'/siat/static/src/js/siat/components/sync-tipos-metodo-pago.js',
			'/siat/static/src/js/siat/components/sync-tipos-moneda.js',
			'/siat/static/src/js/siat/components/sync-tipos-punto-venta.js',
			'/siat/static/src/js/siat/components/sync-unidades-medida.js',
			'/siat/static/src/js/siat/components/sync-codigos.js',
			'/siat/static/src/js/siat/components/siat-sync.js',
			'/siat/static/src/js/siat/components/cufd-listing.js',
			'/siat/static/src/js/siat/components/cerrar-evento.js',
			'/siat/static/src/js/siat/components/eventos.js',
			'/siat/static/src/js/siat/components/void-invoice.js',
			'/siat/static/src/js/siat/components/invoice-listing.js',
			'/siat/static/src/js/siat/components/sectores/alquiler.js',
			'/siat/static/src/js/siat/components/sectores/colegios.js',
			'/siat/static/src/js/siat/components/sectores/entidad-financiera.js',
			'/siat/static/src/js/siat/components/sectores/exportacion.js',
			'/siat/static/src/js/siat/components/sectores/exportacion-servicio.js',
			'/siat/static/src/js/siat/components/sectores/hospitales.js',
			'/siat/static/src/js/siat/components/sectores/hoteles.js',
			'/siat/static/src/js/siat/components/sectores/prevalorada.js',
			'/siat/static/src/js/siat/components/sectores/tasa-cero.js',
			'/siat/static/src/js/siat/components/sectores/turistico-hospedaje.js',
			'/siat/static/src/js/siat/components/invoicer-top.js',
			'/siat/static/src/js/siat/components/form-tarjeta.js',
			'/siat/static/src/js/siat/components/invoicer.js',
			'/siat/static/src/js/siat/components/puntos-venta.js',
			'/siat/static/src/js/siat/components/config.js',
			'/siat/static/src/js/siat/app.js',
		],
		viewType: 'siat_view',
		groupable: false,
		init: function () 
		{
			this._super.apply(this, arguments);
			this.loadParams.view = this.arch.attrs.view;
			console.log('siat_view.view', this.loadParams.view);
		},
	});

	viewRegistry.add('siat_view', SiatView);

	return SiatView;

});

odoo.define('siat_view.SiatViewController', function (require) {
	"use strict";

	var AbstractController = require('web.AbstractController');
	var SiatViewController = AbstractController.extend({});

	return SiatViewController;

});

odoo.define('siat_view.SiatViewEvolution', function (require) {
	"use strict";

	var SiatView = require('siat_view.SiatView');
	var SiatViewController = require('siat_view.SiatViewController');
	var viewRegistry = require('web.view_registry');

	var SiatEvolutionController = SiatViewController.extend({

		renderButtons: function ($node) 
		{
			this.$buttons = $('<div>');
			var $button = $('<div class="btn-group" role="toolbar" aria-label="Main actions">')
							.append(
								$('<button class="btn btn-primary">').text('Toggle Contact Markers')
							);
			$button.click(this._onButtonClick.bind(this));
			this.$buttons.append($button);
			this.$buttons.appendTo($node);
		},

		_onButtonClick: function (event) {
			this.model.displayContacts = !this.model.displayContacts;
			this.update({});
		},
	});

	var SiatViewEvolution = SiatView.extend({
		config: _.extend({}, SiatView.prototype.config, {Controller: SiatEvolutionController}) ,
	});

	viewRegistry.add('siat_view_evolution', SiatViewEvolution);

	return SiatViewEvolution;

});
