(function(ns)
{
	class ServiceCustomers extends SBFramework.Classes.Api
	{
		constructor()
		{
			super();
		}
		getHeaders()
		{
			const headers = {};
			
			return headers;
		}
		async create(customer)
		{
			const headers = this.getHeaders();
			const res = await this.Post(`/invoices/siat/v2/customers`, customer, headers);
			
			return res;
		}
		async update(customer)
		{
			const headers = this.getHeaders();
			const res = await this.Put(`/invoices/siat/v2/customers`, customer, headers);
			
			return res;
		}
		async read(id)
		{
			const res = await this.Get(`/invoices/siat/v2/customers/${id}`);
			
			return res;
		}
		async readAll()
		{
			const res = await this.Get(`/invoices/siat/v2/customers`);
			
			return res;
		}
		async remove(id)
		{
			const headers = this.getHeaders();
			const res = await this.Delete(`/invoices/siat/v2/customers/${id}`, headers);
			
			return res;
		}
		async search(keyword)
		{
			const headers = this.getHeaders();
			const data = await this.Get(`/../_inc/pos.php?query_string=${keyword}&field=customer_name&action_type=CUSTOMERLIST&limit=30`, headers);
			let res = {data: []};
			if( data && data.length > 0 )
			{
				for(let customer of data)
				{
					const name = this.parseName(customer.customer_name);
					res.data.push({
						id: customer.customer_id,
						firstname: name.firstname,
						lastname: name.lastname,
						text: customer.customer_name,
						nit_ruc_nif: customer.gtin,
						email: customer.customer_email,
					});
				}
			}
			return res;
		}
		parseName(name)
		{
			let data = {
				firstname: '',
				lastname: '',
			};
			let parts = name.split(' ');
			if( parts.length == 4 )
			{
				data.firstname = `${parts[0]} ${parts[1]}`;
				data.lastname = `${parts[2]} ${parts[3]}`;
			}
			else if( parts.length == 3 )
			{
				data.firstname = `${parts[0]} ${parts[1]}`;
				data.firstname = `${parts[2]}`;
			}
			else if( parts.length == 2 )
			{
				data.firstname = `${parts[0]}`;
				data.lastname = `${parts[1]}`;
			}
			else
			{
				data.lastname = `${parts[0]}`;
			}
			return data;
		}
	}
	ns.ServiceCustomers = ServiceCustomers;
})(SBFramework.Services);
