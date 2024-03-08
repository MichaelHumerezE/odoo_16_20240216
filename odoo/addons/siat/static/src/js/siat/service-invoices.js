(function(ns)
{
	class ServiceInvoices extends SBFramework.Classes.Api
	{
		constructor()
		{
			super();
		}
		async obtenerCuis(renew)
		{
			let res = await this.Get(`/siat/sync/cuis/sucursal/0/puntoventa/0/renew/` + ( renew ? 1 : 0));
			
			return res;
		}
		async obtenerCufd(sucursal, puntoventa, renew)
		{
			let res = await this.Get(`/siat/sync/cufd/sucursal/${sucursal}/puntoventa/${puntoventa}/renew/` + ( renew ? 1 : 0));
			
			return res;
		}
		async obtenerCufds(sucursal, puntoventa)
		{
			let res = await this.Get(`/siat/cufds/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			
			return res;
		}
		async obtenerSucursales()
		{
			let res = await this.Get('/siat/branches');
			
			return res;
		}
		async obtenerPuntosVenta(sucursal)
		{
			sucursal = ( isNaN( parseInt(sucursal) ) ) ? 0 : parseInt(sucursal)
			
			let res = await this.Get(`/siat/sync/puntosventa/sucursal/${sucursal}`);
			
			return res;
		}
		async obtenerTiposProductos()
		{
			let res = await this.Get('/invoices/siat/v2/lista-productos-servicios');
			
			return res;
		}
		async obtenerUnidadesMedida()
		{
			let res = await this.Get('/siat/sync/unidades_medida');
			
			return res;
		}
		async obtenerMonedas()
		{
			let res = await this.Get('/siat/sync/tipos_moneda');
			
			return res;
		}
		async obtenerDocumentosIdentidad()
		{
			let res = await this.Get('/siat/sync/documentos_identidad');
			
			return res;
		}
		async obtenerMetodosPago()
		{
			let res = await this.Get('/siat/sync/metodos_pago');
			
			return res;
		}
		async obtenerActividades()
		{
			let res = await this.Get('/siat/sync/actividades');
			
			return res;
		}
		async obtenerActividadesDocumentoSector()
		{
			let res = await this.Get('/siat/sync/actividades_doc_sector');
			return res;
		}
		async obtenerMotivosAnulacion()
		{
			let res = await this.Get('/siat/sync/motivos_anulacion');
			return res;
		}
		async obtenerDocumentosIdentidad()
		{
			let res = await this.Get('/siat/sync/documentos_identidad');
			return res;
		}
		async obtenerEventos()
		{
			let res = await this.Get('/siat/sync/eventos');
			return res;
		}
		async obtenerLeyendas()
		{
			let res = await this.Get('/siat/sync/leyendas');
			return res;
		}
		async obtenerProductosServicios()
		{
			let res = await this.Get('/siat/sync/productos_servicios');
			return res;
		}
		async obtenerTiposDocumentoSector()
		{
			let res = await this.Get('/siat/sync/tipos_documentos_sector');
			return res;
		}
		async obtenerTiposEmision()
		{
			let res = await this.Get('/siat/sync/tipos_emision');
			return res;
		}
		async obtenerTiposFactura()
		{
			let res = await this.Get('/siat/sync/tipos_facturas');
			return res;
		}
		async obtenerTiposHabitacion()
		{
			let res = await this.Get('/siat/sync/tipos_habitacion');
			return res;
		}
		async obtenerTiposMetodoPago()
		{
			let res = await this.Get('/siat/sync/metodos_pago');
			return res;
		}
		async obtenerTiposMoneda()
		{
			let res = await this.Get('/siat/sync/tipos_moneda');
			return res;
		}
		async obtenerTiposPuntoVenta()
		{
			let res = await this.Get('/siat/sync/tipos_puntoventa');
			return res;
		}
		async crearEvento(evento, system)
		{
			//const res = await this.Post(`/siat/eventos?system=${system}`, evento);
			const res = await this.Post(`/siat/eventos`, evento);
			
			return res;
		}
		async crearFactura(invoice)
		{
			const res = await this.Post(`/siat/invoices`, invoice, this.getHeaders());
			if( res.data && res.data.invoice )
			{
				return  {
					code: res.code,
					status: res.status,
					data: Object.assign({}, res.data.invoice, {id: res.data.invoice.invoice_id})
				};	
			}	
			return res;
		}
		async obtenerFacturas(page, limit, keyword)
		{
			page = page || 1;
			limit = limit || 25;
			let endpoint = `/siat/invoices/page/${page}/limit/${limit}`;
			if( keyword )
				endpoint += `/keyword/${keyword}`;
			const res = await this.Get(endpoint);
			//console.log(res.headers.get("total-pages"));
			return res;
		}
		async anular(id, obj)
		{
			const res = await this.Post('/siat/invoices/void/' + id, obj, this.getHeaders());
			return res;
		}
		async buscar(keyword)
		{
			const res = await this.Get(`/siat/invoices/search?keyword=${keyword}`);
			
			return res;
		}
		async reenviar(id)
		{
			const res = await this.Get(`/siat/invoices/${id}/reenviar`);

			return res;
		}
	}
	ns.ServiceInvoices = ServiceInvoices;
})(SBFramework.Services);
