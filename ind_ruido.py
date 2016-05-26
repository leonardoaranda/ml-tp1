# Construir una familia de datasets induciendo ruido. Preservar un 20% sin
# alterar para las corridas de validacion .Variar desde 0 a 35 en intervalos de 5.

import yaml
import os

config = yaml.safe_load(open('config.yaml'))

def add_noise(percent):
	weka = 'weka.filters.unsupervised.attribute.AddNoise -C {0} -P {1} -S 1 -i {2} -o {2}_noise_{1}.arff'
	weka =	weka.format(config['class_index'],percent,config['data'])
	os.popen('java -cp \'{0}\' {1}'.format(config['weka_path'],weka))

i = 0
while i <= 35:
	add_noise(i)
	i+= 5