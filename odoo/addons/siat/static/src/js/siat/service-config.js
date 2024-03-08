(function(ns)
{
	class ServiceConfig extends SBFramework.Classes.Api
	{
		constructor()
		{
			super();
		}
		async save(data)
		{
			const headers = this.getHeaders();
			const res = await this.Post(`/siat/config`, data, headers);
			
			return res;
		}
		async uploadCerts(formData)
		{
		    const headers = this.getHeaders();
		    const res = await this.Upload(`/siat/config/certs`, formData);

		    return res;
		}
		async read()
		{
			const headers = this.getHeaders();
			const res = await this.Get(`/siat/config`, headers);
			
			return res;
		}
	}
	ns.ServiceConfig = ServiceConfig;
})(SBFramework.Services);