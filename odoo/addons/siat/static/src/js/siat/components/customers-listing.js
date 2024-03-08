(function(ns)
{
	ns.ComCustomersListing = {
		template: `<div id="mod-customers-listing">
			<h2>
				Listado de Clientes
				<button type="button" class="btn btn-primary w-100" v-on:click="newCustomer()">Nuevo Cliente</button>
			</h2>
			<div class="panel panel-default card" v-for="(customer, ci) in items">
				<div class="panel-body card-body">
					<div class="row">
						<div class="col-12 col-sm-9">
							<div>ID: {{ customer.id }}</div>
							<div>{{ customer.firstname }} {{ customer.lastname }}</div>
							<div>{{ customer.email }}</div>
						</div>
						<div class="col-12 col-sm-3">
							<button class="btn btn-primary" v-on:click="edit(customer)">Editar</button>
							<button class="btn btn-danger" v-on:click="remove(customer, ci)">Borrar</button>
						</div>
					</div>
				</div>
			</div>
			<siat-customer-form ref="customer_form" v-bind:edit_customer="customer" v-on:customer-saved="onCustomerSaved" />
		</div>`,
		components: 
		{
			'siat-customer-form': ns.ComCustomerForm,
		},
		data()
		{
			return {
				service: new SBFramework.Services.ServiceCustomers(),
				items: [],
				customer: {},
			};	
		},
		methods: 
		{
			async getCustomers()
			{
				this.$root.$processing.show('Obteniendo datos...');
				const res	= await this.service.readAll();
				this.items 	= res.data;
				this.$root.$processing.hide();
			},
			newCustomer()
			{
				this.$refs.customer_form.showModal();
			},
			edit(customer)
			{
				this.customer = customer;
				this.$refs.customer_form.setCustomer(customer);
				this.$refs.customer_form.showModal();
			},
			onCustomerSaved(data)
			{
				this.$root.$toast.ShowSuccess('Cliente guardado correctamente');
				console.log('customer_save', data);
				if( data.action == 'update' )
				{
					Object.assign(this.customer, data.customer);
					return true;
				}
				this.getCustomers();
			},
			async remove(customer, index)
			{
				try
				{
					this.$root.$processing.show('Borrando cliente...');
					const res = await this.service.remove(customer.id);
					this.$root.$processing.hide();
					this.$root.$toast.ShowSuccess('Cliente borrado correctamente');
					//this.getCustomers();
					this.items.splice(index, 1);
				}
				catch(e)
				{
					this.$root.$processing.hide();
				}
			}
		},
		mounted()
		{
			const frame = (window.bootstrap || window.coreui);
			if( frame )
			{
				
			}
			else
			{
			}
		},
		created()
		{
			this.getCustomers();
		}
	};
	SBFramework.AppComponents = {
		'siat-customers-listing': ns.ComCustomersListing, 
	};
})(SBFramework.Components.Siat);