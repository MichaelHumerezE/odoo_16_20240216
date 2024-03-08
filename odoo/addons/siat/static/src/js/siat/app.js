window.loadSiatApp = function(appEl, langs, lang)
{
	//window.addEventListener('load', function()
	//{
		//console.log('windown onload');
		let app = null;
		let $api = new SBFramework.Classes.Api();
		$api.apiBase = SBFramework.APIBASE;
		function loadApp(selector, _user)
		{
			const appcoms = Object.assign({
				'com-processing': SBFramework.Components.ComProcessing,
				'com-menu': SBFramework.Components.ComMenu,
			}, SBFramework.AppComponents || {});
			let vue_app = new Vue({
				el: selector,
				components: appcoms,
				data: Object.assign({
					ready: false,
					api: $api,
					/*
					user: new SBFramework.Models.User(),
					currentRoute: SBFramework.Components.Router.GetCurrentRoute(),
					currentCom: (function()
					{
						let component = SBFramework.Components.Router.GetCom(SBFramework.Components.Router.GetCurrentRoute());
						
						return (component != null && typeof component == 'object') ? component.com : component;
					})(),
					comData: SBFramework.Components.Router.GetData(),
					routeData: SBFramework.Components.Router.routeData,
					*/
					user: Object.assign(new SBFramework.Models.User(), _user),
					currentRoute: null,
					currentCom: null,
					comData: null,
					routeData: null,
					com_title: '',
					com_subtitle: '',
					com_icon: '',
					company: {},
					supabase: null,
				}, SBFramework.AppData || {}),
				computed: 
				{
					com_current: function()
					{
						//this.CheckSession();
						return this.currentCom;
					},
					com_args: function()
					{
						//let data = Router.ParseURL(this.currentRoute);
						return this.routeData;
					},
					com_key: function()
					{
						return this.currentCom + Date.now();
					},
					top_menu_coms: function()
					{
						return SBFramework.Hooks.top_menu;
					}
				},
				methods:
				{
					CheckSession: function()
					{
						
					},
					toggleSidebar(e)
					{
						e.preventDefault();
						document.body.classList.toggle("sidenav-toggled");
					},
				},
				mounted()
				{
					console.log('vueApp mounted');
					//##check if router component is loaded
					if( SBFramework.Components.Router )
					{
						this.currentRoute 	= SBFramework.Components.Router.GetCurrentRoute();
						let component 		= SBFramework.Components.Router.GetCom(this.currentRoute);
						this.currentCom 	= (component != null && typeof component == 'object') ? component.com : component;
						this.comData = SBFramework.Components.Router.GetData();
						this.routeData = SBFramework.Components.Router.routeData;
					}
					
					this.ready = true;
					this.$emit('app-ready');
					if( this.$refs.com_container )
						this.$refs.com_container.classList.add('show');
				},
				created: async function()
				{
					if( SBFramework.Components.Router )
						SBFramework.Components.Router.app = this;
					//Object.assign(this.user, pres.data);
				}
			});
			return vue_app;
		}
		try
		{
			app = loadApp(appEl, {});
		}
		catch(e)
		{
			console.log('VUE APP ERROR', e);
			console.trace();
		}
	//});
};
