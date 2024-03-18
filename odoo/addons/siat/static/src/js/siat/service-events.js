(function(ns)
{
	class ServiceEvents extends SBFramework.Classes.Api
	{
		constructor()
		{
			super();
		}
		async obtenerActivo(sucursal, puntoventa)
		{
			let res = await this.Get(`/siat/eventos/activo/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			
			return res;
		}
		async crear(evento)
		{
			const res = await this.Post('/siat/eventos', evento, this.getHeaders());
			
			return res;
		}
		async cerrar(eventId)
		{
			const res = await this.Get(`/siat/eventos/${eventId}/cerrar`);
			return res;
		}
		async anular(eventId)
		{
			const res = await this.Get('/siat/eventos/' + eventId + '/anular');
			
			return res;
		}
		async validarRecepcion(eventId)
		{
			const res = await this.Get(`/siat/eventos/${eventId}/validar-recepcion`);
			
			return res;
		}
		async obtenerEventos(sucursal, puntoventa, page)
		{
			page = page || 1;
			const res = await this.Get(`/siat/eventos/sucursal/${sucursal}/puntoventa/${puntoventa}/page/${page}`)
			return res;
		}
		async syncEventos(sucursal, puntoventa)
		{
			const res = await this.Get(`/siat/eventos/sucursal/${sucursal}/puntoventa/${puntoventa}`);
			
			return res;
		}
		async stats(eventId)
		{
			const res = await this.Get(`/siat/eventos/${eventId}/stats`);
			
			return res;
		}
	}
	ns.ServiceEvents = ServiceEvents;
})(SBFramework.Services);
