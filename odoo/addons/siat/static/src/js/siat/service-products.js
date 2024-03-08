(function(ns)
{
	class ServiceProducts extends SBFramework.Classes.Api
	{
		constructor()
		{
			super();
		}
		async create(product)
		{
			const headers = this.getHeaders();
			const res = await this.Post(`/invoices/siat/v2/products`, product, headers);
			
			return res;
		}
		async read(id)
		{
			const res = await this.Get(`/invoices/siat/v2/products/${id}`);
			
			return res;
		}
		async readAll(page)
		{
			const headers = this.getHeaders();
			const res = await this.Get(`/invoices/siat/v2/products?page=${page}`);
			
			return res;
		}
		async update(product)
		{
			const headers = this.getHeaders();
			const res = await this.Put(`/invoices/siat/v2/products`, product, headers);
			
			return res;
		}
		async remove(id)
		{
			const res = await this.Delete(`/invoices/siat/v2/products/${id}`, {'X-CSRF-TOKEN': document.head.querySelector('[name=csrf-token]').content});
			
			return {data: res};
		}
		async buscarProducto(keyword)
		{
			const resRaw = await this.Get(`/../_inc/pos.php?action_type=PRODUCTLIST&query_string=${keyword}&category_id=&field=p_name&page=1`);
			let res = {
				data: []
			};
			for(let prod of resRaw.products)
			{
				res.data.push({
					id: prod.p_id,
					product_id: prod.p_id,
					code: prod.p_code,
					name: prod.p_name,
					description: prod.description,
					price: prod.sell_price,
					unidad_medida: prod.unidad_medida_sin,
					codigo_actividad: prod.actividad_economica,
					codigo_sin: prod.codigo_producto_sin,
					num_serie: '',
					imei: '',
				});	
			}
			return res;
		}
		async search(keyword)
		{
			const res = await this.Get(`/siat/products/search/${keyword}`);
			
			return res;
		}
	}
	ns.ServiceProducts = ServiceProducts;
})(SBFramework.Services);
