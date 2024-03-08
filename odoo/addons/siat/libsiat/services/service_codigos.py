from .service_siat import ServiceSiat

class ServiceCodigos(ServiceSiat):

	def __init__(self):
		super().__init__()
		self.wsdl = 'https://pilotosiatservicios.impuestos.gob.bo/v2/FacturacionCodigos?wsdl'
	
	def buildData(self, sucursal, puntoventa):
		return [
			{
				#'SolicitudCuis': {
					'codigoAmbiente'	: self.ambiente,
					'codigoModalidad'	: self.modalidad,
					'codigoPuntoVenta'	: puntoventa,
					'codigoSistema'		: self.codigoSistema,
					'codigoSucursal'	: sucursal,
					'nit'				: self.nit,
				#}
			}
		]
		
	def getCuis(self, sucursal, puntoventa):
		return self.callAction('cuis', self.buildData(sucursal, puntoventa))
	
	def getCufd(self, sucursal, puntoventa):
		data = self.buildData(sucursal, puntoventa)
		data[0]['cuis'] = self.cuis
		return self.callAction('cufd', data)

	def verificarNit(self, nit, sucursal=0, puntoventa=0):
		data = self.buildData(sucursal, puntoventa)
		data[0]['cuis'] = self.cuis
		data[0]['nitParaVerificacion'] = nit
		
		return self.callAction('verificarNit', data)
		
