(function(ns)
{
	class ServiceBranches extends SBFramework.Classes.Api
	{
		constructor()
		{
			super();
		}
		async readAll()
		{
			const res = await this.Get(`/siat/branches`);
			
			return res;
		}
		async read(id)
		{
			
		}
		async create(branch)
		{
			const headers = this.getHeaders();
			const res = await this.Post(`/siat/branches`, branch, headers);
			
			return res;
		}
		async update(branch)
		{
			const headers = this.getHeaders();
			const res = await this.Put(`/siat/branches`, branch, headers);
			
			return res;
		}
		async remove(id)
		{
			const headers = this.getHeaders();
			const res = await this.Delete(`/siat/branches/${id}`, headers);
			
			return res;
		}
	}
	ns.ServiceBranches = ServiceBranches;
})(SBFramework.Services);
