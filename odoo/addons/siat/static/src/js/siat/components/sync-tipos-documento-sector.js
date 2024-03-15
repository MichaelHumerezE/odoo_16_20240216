(function(ns)
{
	ns.ComSyncTiposDocumentosSector = {
		template: `<div id="com-sync-tipos-documentos-sector">
			<div class="mb-3"><button type="button" class="btn btn-primary" v-on:click="getData()">Sincronizar</button></div>
			<div class="table-responsive">
				<table class="table table-sm table-striped">
				<thead>
				<tr>
					<th>Nro</th>
					<th>Codigo</th>
					<th>Descripcion</th>
				</tr>
				</thead>
				<tbody>
				<tr v-for="(item, index) in lista">
					<td>{{ index + 1 }}</td>
					<td>{{ item.codigoClasificador }}</td>
					<td>{{ item.descripcion }}</td>
				</tr>
				</tbody>
				</table>
			</div>
		</div>`,
		data()
		{
			return {
				lista: [],
				codigo_sucursal: this.$parent.priv_sucursal_id,
				codigo_puntoVenta: this.$parent.priv_puntoventa_id,
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
					const res = await this.$parent.service.obtenerTiposDocumentoSector(this.codigo_sucursal, this.codigo_puntoVenta);
					this.lista = res.data.RespuestaListaParametricas.listaCodigos;
				} catch (e) {
					this.$root.$processing.hide();
					alert(e.error || e.message || 'Error desconocido');
				}
				//const res = await this.$parent.service.obtenerTiposDocumentoSector();
				//this.lista = res.data.RespuestaListaParametricas.listaCodigos;
			}
		},
		created()
		{
			this.getData();
		}
	};
})(SBFramework.Components.Siat);