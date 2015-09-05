import AnalizadorLexico

CONST = "const"
VAR = "var"
PROCEDURE = "procedure"

class AnalizadorSintactico(object):
	
	def __init__(self, scanner, output):
		self.out = output
		self.scanner = scanner
	
	def _parsear_bloque(self):
		simbolo = self.scanner.obtener_simbolo()
		valor = self.scanner.obtener_valor_actual()
		#Analizamos la parte de constantes:
		if simbolo == AnalizadorLexico.IDENTIFICADOR_O_RESERVADA and valor == CONST:
			while True:
				simbolo = self.scanner.obtener_simbolo()
				if simbolo == AnalizadorLexico.IDENTIFICADOR_O_RESERVADA:
					identificador = self.scanner.obtener_valor_actual()
					#TODO: mandar al analizador semantico para ver que sea correcto el identificador!
				
					simbolo = self.scanner.obtener_simbolo()
					if simbolo == AnalizadorLexico.IGUAL:
						simbolo = self.scanner.obtener_simbolo()
						if simbolo == AnalizadorLexico.NUMERO:
							valor = self.scanner.obtener_valor_actual()
							#TODO: asignarle el valor al identificador
							
							simbolo = self.scanner.obtener_simbolo()
							if simbolo == AnalizadorLexico.PUNTO_Y_COMA:
								break
							elif simbolo != AnalizadorSintactico.COMA:
								output.write("Error Sintactico: Se esperaba punto y coma (;) o coma (,) luego de declaracion de constante")
								break
						else:
							output.write("Error Sintactico: asignacion de constante a un valor no numerico")
							break
					else:
						output.write("Error Sintactico: asignacion de constante esperada (=)")
						break
				else:
					output.write("Error Sintactico: declaracion de constante no seguida de un identificador")
					break
				
	
	def parsear_programa(self):
		self._parsear_bloque()
		simbolo = self.scanner.obtener_tipo_actual()
		if simbolo != AnalizadorLexico.PUNTO:
			output.write("Error Sintactico: Se esperaba punto (.) de finalizacion de programa")
		


if __name__ == "__main__":
	output = open("salida.txt", "w")
	al = AnalizadorLexico.AnalizadorLexico("ejemplo.txt", output)
	as = AnalizadorSintactico(al, output)
	as.parsear_programa()
	output.close()
