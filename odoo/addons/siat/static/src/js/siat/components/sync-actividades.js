(function(ns)
{
	ns.ComSyncActividades = {
		template: `<div id="com-sync-actividades">
			<div class="mb-3"><button type="button" class="btn btn-primary" v-on:click="getData()">Sincronizar</button></div>
			<div class="table-responsive">
				<table class="table table-sm">
				<thead>
				<tr>
					<th>Nro</th>
					<th>Codigo</th>
					<th>Descripcion</th>
					<th>Tipo</th>
				</tr>
				</thead>
				<tbody>
				<tr v-for="(item, index) in lista">
					<td>{{ index + 1 }}</td>
					<td>{{ item.codigoCaeb }}</td>
					<td>{{ item.descripcion }}</td>
					<td>{{ item.tipoActividad  }}</td>
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
					// this.$root.$processing.show('Obtenido datos...');
					const res = await this.$parent.service.obtenerActividades(this.codigo_sucursal, this.codigo_puntoVenta);
					// this.$root.$processing.hide();
					this.lista = Array.isArray(res.data.RespuestaListaActividades.listaActividades) ?
						res.data.RespuestaListaActividades.listaActividades : 
						[res.data.RespuestaListaActividades.listaActividades];
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