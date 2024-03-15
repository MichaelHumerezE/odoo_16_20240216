(function(ns)
{
	ns.ComSyncLeyendas = {
		template: `<div id="com-sync-leyendas">
			<div class="mb-3"><button type="button" class="btn btn-primary" v-on:click="getData()">Sincronizar</button></div>
			<div class="table-responsive">
				<table class="table table-sm table-striped">
				<thead>
				<tr>
					<th>Nro</th>
					<th>Codigo Actividad</th>
					<th>Descripcion</th>
				</tr>
				</thead>
				<tbody>
				<tr v-for="(item, index) in lista">
					<td>{{ index + 1 }}</td>
					<td>{{ item.codigoActividad }}</td>
					<td>{{ item.descripcionLeyenda }}</td>
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
					const res = await this.$parent.service.obtenerLeyendas(this.codigo_sucursal, this.codigo_puntoVenta);
					this.lista = res.data.RespuestaListaParametricasLeyendas.listaLeyendas;
				} catch (e) {
					this.$root.$processing.hide();
					alert(e.error || e.message || 'Error desconocido');
				}
				//const res = await this.$parent.service.obtenerLeyendas();
				//this.lista = res.data.RespuestaListaParametricasLeyendas.listaLeyendas;
			}
		},
		created()
		{
			this.getData();
		}
	};
})(SBFramework.Components.Siat);