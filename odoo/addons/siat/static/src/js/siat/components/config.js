(function(ns)
{
	ns.ComConfig = {
		template: `<div id="com-siat-config">
			<ul class="nav nav-tabs">
				<li class="nav-item active">
					<a href="#general" class="nav-link active" data-toggle="tab" data-bs-toggle="tab">General</a>
				</li>
				<li class="nav-item">
					<a href="#cafc" class="nav-link" data-toggle="tab" data-bs-toggle="tab">CAFC</a>
				</li>
			</ul>
			<div class="tab-content">
				<div id="general" class="tab-pane p-4 active">
					<div class="row">
						<div class="col-12 col-sm-6">
							<div class="form-group mb-3">
								<label>Nombre Sistema</label>
								<input type="text" class="form-control" v-model="config.nombre_sistema" required />
							</div>
							<div class="form-group mb-3">
								<label>NIT</label>
								<input type="text" class="form-control" v-model="config.nit" required />
							</div>
							<div class="form-group mb-3">
								<label>Modalidad</label>
								<select class="form-control form-select" v-model="config.modalidad" required>
									<option value="1">Eletronica en Linea</option>
									<option value="2">Computarizada en Linea</option>
								</select>
							</div>
							<div class="form-group mb-3">
								<label>Token Delegado</label>
								<textarea class="form-control" v-model="config.token_delegado" style="height:110px;"></textarea>
							</div>
						</div>
						<div class="col-12 col-sm-6">
							<div class="form-group mb-3">
								<label>Codigo Sistema</label>
								<input type="text" class="form-control" v-model="config.codigo_sistema" required />
							</div>
							<div class="form-group mb-3">
								<label>Razon Social</label>
								<input type="text" class="form-control" v-model="config.razon_social" required />
							</div>
							<div class="form-group mb-3">
								<label>Ambiente</label>
								<select class="form-control form-select" v-model="config.ambiente" required>
									<option value="1">Produccion</option>
									<option value="2">Piloto/Pruebas</option>
								</select>
							</div>
							<div class="form-group mb-3">
								<label>Llave privada</label>
								<input type="file" name="private_key" class="form-control" v-on:change="fileSelected($event, 'private')" ref="private_key" />
								<div class="text-success" v-if="config.priv_cert">
									<b>Archivo Actual:</b> {{ config.priv_cert ? config.priv_cert.split('/').reverse()[0] : '' }}
								</div>
							</div>
							<div class="form-group mb-3">
								<label>Certificado</label>
								<input type="file" name="cert" class="form-control" v-on:change="fileSelected($event, 'public')" ref="cert" />
								<div class="text-success" v-if="config.pub_cert">
									<b>Archivo Actual:</b> {{ config.pub_cert ? config.pub_cert.split('/').reverse()[0] : '' }}
								</div>
							</div>
						</div>
					</div>
				</div>
				<div id="cafc" class="tab-pane p-4">
                    <div class="row">
                        <div class="col-12 col-sm-3" v-for="(sector, si) in sectors">
                            <div class="card mb-2">
                                <div class="card-header"><h5 class="card-title">{{ sector.label }}</h5></div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="mb-2">
                                            <label>Codigo CAFC</label>
                                            <input type="text" class="form-control form-control-sm" v-model="config.cafc[si].cafc" />
                                        </div>
                                        <div class="col-12 col-sm-6">
                                            <label>Codigo CAFC</label>
                                            <input type="text" class="form-control form-control-sm" v-model="config.cafc[si].min" />
                                        </div>
                                        <div class="col-12 col-sm-6">
                                            <label>Codigo CAFC</label>
                                            <input type="text" class="form-control form-control-sm" v-model="config.cafc[si].max" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
				</div>
			</div>
			<div class="form-group mb-3">
				<button type="button" class="btn btn-primary" v-on:click="save()">Guardar</button>
			</div>
		</div>`,
		mixins: [],
		data()
		{
			return {
			    sectors: {
			        compra_venta: {code: 1, label: 'Compra Venta', cafc: '', min: '', max: ''},
			        alquiler: {code: 2, label: 'Alquiler Inmuebles', cafc: '', min: '', max: ''},
			        //servicio_turistico: {code: 6, label: 'Servicio Turistico y Hospedaje', cafc: '', min: '', max: ''},
			        tase_cero: {code: 8, label: 'Tasa Cero', cafc: '', min: '', max: ''},
			        educativo: {code: 11, label: 'Sector Educativo', cafc: '', min: '', max: ''},
			        hoteles: {code: 16, label: 'Hoteles', cafc: '', min: '', max: ''},
                },
				config: {
					modalidad: '',
					ambiente: '',
					nombre_sistema: '',
					codigo_sistema: '',
					token_delegado: '',
					razon_social: '',
					nit: '',
					//privCert: '',
					//pubCert: '',
					cafc: {},
				},
				privCert: '',
				pubCert: '',
				service: new SBFramework.Services.ServiceConfig(),
			};
		},
		methods: 
		{
			async save()
			{
				try
				{
				    this.$root.$processing.show('Guardando datos...');
				    const res = await this.service.save(this.config);
                    if( this.$refs.cert.files.length > 0 || this.$refs.private_key.files.length > 0 )
                    {
                        let formData = new FormData();
                        if( this.$refs.cert.files.length > 0 )
                            formData.append(this.$refs.cert.name, this.$refs.cert.files[0]);
                        if( this.$refs.private_key.files.length > 0 )
                            formData.append(this.$refs.private_key.name, this.$refs.private_key.files[0]);
                        const resUpload = await this.service.uploadCerts(formData);
                    }
				    this.$root.$processing.hide();
				}
				catch(e)
				{
				    this.$root.$processing.hide();
				    console.log('ERROR', e);
				}
			},
			async load()
			{
			    try
				{
				    this.$root.$processing.show('Obteniendo datos...');
				    const res = await this.service.read();
				    if( res.data )
				    {
				        if( !res.data.cafc )
				            delete res.data.cafc;
				        else
				        try{
				            res.data.cafc = JSON.parse(res.data.cafc);
				        }
				        catch(e){res.data.cafc = this.sectors}
				        Object.assign(this.config, res.data);
				    }
				    this.$root.$processing.hide();
				}
				catch(e)
				{
				    this.$root.$processing.hide();
				    console.log('ERROR', e);
				}
			},
			fileSelected($event, type)
			{
			    if( type == 'private' )
			    {
			    }
			}
		},
		mounted()
		{
			
		},
		created()
		{
		    this.config.cafc = this.sectors;
			this.load();
		}
	};
	Object.assign(SBFramework.AppComponents, {'siat-config': ns.ComConfig});
})(SBFramework.Components.Siat);