# moda, se rellena el dato faltante con la moda del atributo.
# modaclase, se rellena el dato faltante con la moda del atributo segun la clase.

# Construir una familia de dataset induciendo datos faltantes para cada
# estrategia de relleno sobre el 80% de los datos. Preservar un 20% sin alterar
# para las corridas de validacion. Variar desde 0 a 85 en intervalos de 2.5.

import yaml
import os

config = yaml.safe_load(open('config.yaml'))

class WekaMissingGenerator():

	# Init
	def __init__(self,probability):
		self.probability = probability

	# Ejecuta Weka
	def run(self,weka):
		os.popen('java -cp \'{0}\' {1}'.format(config['weka_path'],weka))

	# Genera valores faltantes
	def replace_with_missing_value(self):
		output = 'missing_{0}.arff'.format(self.probability)
		weka = 'weka.filters.unsupervised.attribute.ReplaceWithMissingValue -R first-last -S 1 -P {0} -i {1} -o {2} -c {3}'
		weka =	weka.format(self.probability,config['data'],output,config['class_index'])
		self.run(weka)
		return output

	# Para cada valor de la clase, reemplaza valores faltantes con la moda
	def replace_missing_values_class(self,filename):
		replaced = []
		for c in config['class_values']:
			output = '{0}_{1}_replaced.arff'.format(filename,c)
			filters = {
				'subset' : 'weka.filters.unsupervised.instance.SubsetByExpression -E \\"CLASS is \'{0}\'\\"'.format(c),
				'missing' : 'weka.filters.unsupervised.attribute.ReplaceMissingValues'
			}
			weka = 'weka.filters.MultiFilter -F "{0}" -F "{1}" -i {2} -o {3} -c {4}'
			weka = weka.format(filters['subset'],filters['missing'],filename,output,config['class_index'])
			self.run(weka)
			replaced.append(output)
		return replaced

	# Une los datasets de cada clase
	def replace_missing_values_class_appender(self,replaced):
		weka = 'weka.core.Instances append {0} {1} > {0}_{1}'.format(replaced[0],replaced[1])
		self.run(weka)

		weka = 'weka.core.Instances append {0}_{1} {2} > missing_{3}_class_replaced.arff'.format(replaced[0],replaced[1],replaced[2],self.probability)
		self.run(weka)

	# Reemplaza valores faltantes con la moda
	def replace_missing_values(self):
		weka = 'weka.filters.unsupervised.attribute.ReplaceMissingValues -i {0} -o missing_{1}_replaced.arff -c {2}'
		weka =	weka.format(config['data'],self.probability,config['class_index'])
		self.run(weka)

p = 0
while p <= 0.1:
	print p
	weka = WekaMissingGenerator(p)
	output = weka.replace_with_missing_value()
	replaced = weka.replace_missing_values_class(output)
	weka.replace_missing_values_class_appender(replaced)
	weka.replace_missing_values()
	p+= 0.025