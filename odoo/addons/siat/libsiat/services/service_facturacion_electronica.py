import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, tostring, register_namespace
from xml.dom.minidom import parseString
from lxml import etree
from signxml import XMLSigner, XMLVerifier, methods

# ET.register_namespace('', "http://www.w3.org/2000/09/xmldsig#");

from .service_facturacion import ServiceFacturacion
from ..invoices.siatinvoice import SiatInvoice


class ServiceFacturacionElectronica(ServiceFacturacion):
	
	def __init__(self):
		super().__init__()
		self.privateCertFile = None
		self.publicCertFile = None
	
	def setConfig(self, data):
		super().setConfig(data)
		self.publicCertFile = data['pubCert'] if 'pubCert' in data else None
		self.privateCertFile = data['privCert'] if 'privCert' in data else None
		
	def validate(self):
		super().validate()
		if os.path.exists(self.publicCertFile) == False:
			raise Exception('Archivo de certificado no existe')
		if os.path.exists(self.privateCertFile) == False:
			raise Exception('Archivo de llave de certificado no existe')
		
		
	def buildInvoiceXml(self, invoice: SiatInvoice):
		pubCertBuffer = open(self.publicCertFile).read()
		privCertBuffer = open(self.privateCertFile).read()
		
		xml = super().buildInvoiceXml(invoice)
		self.debugData('UNSIGNED XML')
		self.debugData(xml.decode('utf-8'))
		
		root = etree.fromstring(xml)
		signer = XMLSigner(
			method=methods.enveloped,
			# c14n_algorithm='http://www.w3.org/2001/10/xml-exc-c14n#',
			c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315',
			signature_algorithm='rsa-sha256', 
			digest_algorithm='sha256'
		)

		signer.namespaces = None
		signed_root = signer.sign(
			root, 
			key=privCertBuffer, 
			cert=pubCertBuffer, 
			# reference_uri='http://www.w3.org/2000/09/xmldsig#enveloped-signature',
			always_add_key_value=False
		)
		
		# verified_data = XMLVerifier().verify(signed_root, x509_cert=pubCertBuffer).signed_xml
		signedXml = etree.tostring(signed_root, encoding='utf-8', method='xml', xml_declaration=True)
		#print('SIGNED XML\n', signedXml)
		
		dom = parseString( signedXml )
		# print('SIGNED XML\n', signedXml.decode('utf-8'))
		self.debugData('SIGNED XML')
		self.debugData(dom.toprettyxml())
		# print('VERIFIED DATA\n', parseString( tostring(verified_data,  encoding='utf-8', method='xml')).toprettyxml() )
		return signedXml
		
	
