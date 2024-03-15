(function(ns)
{
	ns.ComSyncActividadesDocumentoSector = {
		template: `<div id="com-sync-actividades">
			<div class="mb-3"><button type="button" class="btn btn-primary" v-on:click="getData(true)">Sincronizar</button></div>
			<div class="table-responsive">
				<table class="table table-sm">
				<thead>
				<tr>
					<th>Nro</th>
					<th>Codigo Actividad</th>
					<th>Cod. Doc. Sector</th>
					<th>Tipo Doc. Sector</th>
				</tr>
				</thead>
				<tbody>
				<tr v-for="(item, index) in lista">
					<td>{{ index + 1 }}</td>
					<td>{{ item.codigoActividad }}</td>
					<td>{{ item.codigoDocumentoSector }}</td>
					<td>{{ item.tipoDocumentoSector  }}</td>
				</tr>
				</tbody>
				</table>
			</div>
		</div>`,
		data()
		{
			return {
				lista: [],
				codigo_sucursal:this.$parent.priv_sucursal_id,
				codigo_puntoVenta:this.$parent.priv_puntoventa_id,
			};	
		},
		methods: 
		{
			setSucursal() {
				this.codigo_sucursal = this.$parent.priv_sucursal_id;
			},
			setPuntoVenta() {
				this.codigo_puntoVenta = this.$parent.priv_puntoventa_id;
			},
			async getData()
			{
				try {
					this.$root.$processing.show('Obtenido datos del sector...');
					const res = await this.$parent.service.obtenerActividadesDocumentoSector(this.codigo_sucursal, this.codigo_puntoVenta);
					this.$root.$processing.hide();
					this.lista = res.data.RespuestaListaActividadesDocumentoSector.listaActividadesDocumentoSector;
				} catch (e) {
					this.$root.$processing.hide();
					alert(e.error || e.message || 'Error desconocido');
				} 
			}
		},
		mounted()
		{
			
		},
		created()
		{
			this.getData();
		}
	};
})(SBFramework.Components.Siat);