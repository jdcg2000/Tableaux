#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
	# Imprime una formula como cadena dada una formula como arbol
    	# Input: tree, que es una formula de logica proposicional
    	# Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def String2Tree(A):
   	# Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    	# Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    	# Output: formula como tree
	letrasProposicionales=[char(x) for x in range(97, 123)]
	Conectivos = ['O','Y','>','=']
    	Pila = []
	for c in A:
		if c in letrasProposicionales:
			Pila.append(Tree(c, None, None))
		elif c == '-':
			FormulaAux = Tree(c, None, Pila[-1])
			del Pila[-1]
			Pila.append(FormulaAux)
		elif c in Conectivos:
			FormulaAux = Tree(c, Pila[-1], Pila[-2])
			del Pila[-1]
			del Pila[-1]
			Pila.append(FormulaAux)
		else:
			print("Hay un problema: el simbolo " + str(c) + " no se reconoce")
	return Pila[-1]
	

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def complemento(l): # Retorna el complemento del literal l
	if l.label == '-':
		return Tree(l.right.label, None, None)
	else:
		return Tree('-', None, l)

def par_complementario(l):
	# Esta función determina si una lista de solo literales
	# contiene un par complementario
	# Input: l, una lista de literales
	# Output: True/False
	for x in l:
		new_list = [i for i in l if i != x]
		for y in new_list:
			n_x = complemento(x)
			if n_x.label == y.label and n_x.left == y.left and n_x.right == y.right:
				return True
	return False

def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
	if f.right == None or (f.label == '-' and f.right.right == None):
		return True
	else:
		return False

def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
	for i in l:
		if es_literal(i):
			continue
		else:
			return i
	return None

def clasificacion(f): # Clasifica una formula como alfa o beta
	if es_literal(f) == False:
		if f.label == '-':
			if f.right.label == '-':
				return 'Alfa1'
			elif f.right.label == 'O':
				return 'Alfa3'
			elif f.right.label == '>':
				return 'Alfa4'
			elif f.right.label == 'Y':
				return 'Beta1'
		else:
			if f.label == 'Y':
				return 'Alfa2'
			elif f.label == 'O':
				return 'Beta2'
			elif f.label == '>':
				return 'Beta3'
	else:
		return 'Error en la clasificacion'

def clasifica_y_extiende(f):
	# clasifica una fórmula como alfa o beta y extiende listaHojas
	# de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# Output: no tiene output, pues modifica la variable global listaHojas
	global listaHojas
	print("Formula:", Inorder(f))
    	print("Hoja:", imprime_hoja(h))
	
	assert(f in h), "La formula no esta en la lista!"
	
	clase = clasificacion(f)
    	print("Clasificada como:", clase)
    	assert(clase != None), "Formula incorrecta " + imprime_hoja(h)
	
	if clase == 'Alfa1':
		aux = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux += [f.right.right]
		listaHojas.append(aux)
	elif clase == 'Alfa2':
		aux = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux += [f.left, f.right]
		listaHojas.append(aux)
	elif clase == 'Alfa3':
		aux = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux += [Tree('-', None, f.right.left), Tree('-', None, f.right.right)]
		listaHojas.append(aux)
	elif clase == 'Alfa4':
		aux = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux += [f.right.left, Tree('-', None, f.right.right)]
		listaHojas.append(aux)
	elif clase == 'Beta1':
		aux = [x for x in h]
		aux2 = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux2.remove(f)
		aux += [Tree('-', None, f.right.left)]
		aux2 += [Tree('-', None, f.right.right)]
		listaHojas.append(aux)
		listaHojas.append(aux2)
	elif clase == 'Beta2':
		aux = [x for x in h]
		aux2 = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux2.remove(f)
		aux += [f.left]
		aux2 += [f.right]
		listaHojas.append(aux)
		listaHojas.append(aux2)
	elif clase == 'Beta3':
		aux = [x for x in h]
		aux2 = [x for x in h]
		listaHojas.remove(h)
		aux.remove(f)
		aux2.remove(f)
		aux += [Tree('-', None, f.left)]
		aux2 += [f.right]
		listaHojas.append(aux)
		listaHojas.append(aux2)

def Tableaux(f):
	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f
	global listaHojas
	global listaInterpsVerdaderas

	A = String2Tree(f)
	print('La formula introducida es:\n', Inorder(A))
	
	listaHojas = [[A]]
	
	while (len(listaHojas) > 0):
		h = choice(listaHojas)
		print("Trabajando con hoja:\n", imprime_hoja(h))
		x = no_literales(h)
		if x == None:
			if par_complementario(h):
				listaHojas.remove(h)
			else:
				listaInterpsVerdaderas.append(h)
				listaHojas.remove(h)
		else:
			clasifica_y_extiende(x, h)
			
	return listaInterpsVerdaderas
