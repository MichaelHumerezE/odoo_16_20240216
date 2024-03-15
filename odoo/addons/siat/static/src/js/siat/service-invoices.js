(function(ns)
{
	class ServiceInvoices extends SBFramework.Classes.Api
	{
		constructor()
		{
			super();
		}
		//async obtenerCuis(renew)
		async obtenerCuis(sucursal,puntoventa,renew)
		{
			let res = await this.Get(`/siat/sync/cuis/sucursal/${sucursal}/puntoventa/${puntoventa}/renew/` + ( renew ? 1 : 0));
			//let res = await this.Get(`/siat/sync/cuis/sucursal/0/puntoventa/0/renew/` + ( renew ? 1 : 0));
			
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
		async obtenerUnidadesMedidaPiloto(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/unidades_medida/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			
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
		async obtenerDocumentosIdentidadPiloto(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/documentos_identidad/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			
			return res;
		}
		async obtenerMetodosPago()
		{
			let res = await this.Get('/siat/sync/metodos_pago');
			
			return res;
		}
		async obtenerMetodosPagoPiloto(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/metodos_pago/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			
			return res;
		}
		//async obtenerActividades()
		async obtenerActividades(sucursal,puntoventa)
		{
			//let res = await this.Get('/siat/sync/actividades');
			let res = await this.Get(`/siat/sync/actividades/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			
			return res;
		}
		//async obtenerActividadesDocumentoSector()
		async obtenerActividadesDocumentoSector(sucursal,puntoventa)
		{
			//let res = await this.Get('/siat/sync/actividades_doc_sector');
			let res = await this.Get(`/siat/sync/actividades_doc_sector/sucursal/${sucursal}/puntoventa/${puntoventa}`);

			return res;
		}
		async obtenerMotivosAnulacion()
		{
			let res = await this.Get('/siat/sync/motivos_anulacion');
			return res;
		}
		async obtenerMotivosAnulacionPiloto(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/motivos_anulacion/sucursal/${sucursal}/puntoventa/${puntoventa}`);
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
		async obtenerEventos(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/eventos/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			return res;
		}
		//async obtenerLeyendas()
		async obtenerLeyendas(sucursal,puntoventa)
		{
			//let res = await this.Get('/siat/sync/leyendas');
			let res = await this.Get(`/siat/sync/leyendas/sucursal/${sucursal}/puntoventa/${puntoventa}`);

			return res;
		}
		//async obtenerProductosServicios()
		async obtenerProductosServicios(sucursal,puntoventa)
		{
			//let res = await this.Get('/siat/sync/productos_servicios');
			let res = await this.Get(`/siat/sync/productos_servicios/sucursal/${sucursal}/puntoventa/${puntoventa}`);

			return res;
		}
		//async obtenerTiposDocumentoSector()
		async obtenerTiposDocumentoSector(sucursal,puntoventa)
		{
			//let res = await this.Get('/siat/sync/tipos_documentos_sector');
			let res = await this.Get(`/siat/sync/tipos_documentos_sector/sucursal/${sucursal}/puntoventa/${puntoventa}`);

			return res;
		}
		async obtenerTiposEmision(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/tipos_emision/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			return res;
		}
		async obtenerTiposFactura(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/tipos_facturas/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			return res;
		}
		async obtenerTiposHabitacion(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/tipos_habitacion/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			return res;
		}
		async obtenerTiposMetodoPago()
		{
			let res = await this.Get('/siat/sync/metodos_pago');
			return res;
		}
		async obtenerTiposMoneda(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/tipos_moneda/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			return res;
		}
		async obtenerTiposPuntoVenta()
		{
			let res = await this.Get('/siat/sync/tipos_puntoventa');
			return res;
		}
		async obtenerTiposPuntoVentaPiloto(sucursal,puntoventa)
		{
			let res = await this.Get(`/siat/sync/tipos_puntoventa/sucursal/${sucursal}/puntoventa/${puntoventa}`);
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
		//MODIFY - Api Renewal invoice
		async renovar(id)
		{
			const res = await this.Get(`/siat/invoices/${id}/renovar`);
			return res;
		}
		//**********************************************************
	}
	ns.ServiceInvoices = ServiceInvoices;
})(SBFramework.Services);
