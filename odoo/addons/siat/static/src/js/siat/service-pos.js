(function(ns)
{
	class ServicePointOfSale extends SBFramework.Classes.Api
	{
		constructor()
		{
			super();
		}
		async readAll()
		{
			const headers = this.getHeaders();
			const res = await this.Get(`/siat/puntos-venta`, headers);
			
			return res;
		}
		async read(id)
		{
			const headers = this.getHeaders();
			const res = await this.Get(`/siat/puntos-venta/${id}`, headers);
			
			return res;
		}
		async create(branch)
		{
			const headers = this.getHeaders();
			const res = await this.Post(`/siat/puntos-venta`, branch, headers);
			
			return res;
		}
		async update(branch)
		{
			const headers = this.getHeaders();
			const res = await this.Put(`/siat/puntos-venta`, branch, headers);
			
			return res;
		}
		async remove(id)
		{
			const headers = this.getHeaders();
			const res = await this.Delete(`/siat/puntos-venta/${id}`, headers);
			
			return res;
		}
		async sync()
		{
			const headers = this.getHeaders();
			const res = await this.Get(`/siat/puntos-venta/sync`, headers);
			
			return res;
		}
	}
	ns.ServicePointOfSale = ServicePointOfSale;
})(SBFramework.Services);
