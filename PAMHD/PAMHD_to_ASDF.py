import PAMHD
import asdf
import sys, argparse
import numpy as np

print 'hello world'
print asdf.__version__

def main(argv):
	parser = argparse.ArgumentParser(description="Interpolates variables onto grid.")
	parser.add_argument("-v", "--verbose", action="count", default=0, help = 'verbosity of output')
	parser.add_argument("input_file", metavar = 'full/path/to/input_file.cdf', type=str, help="kameleon-compatible file")
	parser.add_argument("-ginfo","--global-info", action='store_true', help = 'print global attributes')
	parser.add_argument("-db", "--debug", default = False, help = 'debugging flag')

	args = parser.parse_args()

	print args.input_file
	mhd_dict = {}
	sim_params = PAMHD.load(args.input_file, mhd_dict)
	sim_params.
	print sim_params

def get_variables(self):
	mhd_data = []
	for cell_id, mhd_array in self.mhd_dict.items():
		for mhd in mhd_array:
			mhd_data.append(tuple(list(mhd)+[cell_id]))

	mhd_dtype = np.dtype([
							('c0', float),
							('c1', float), 
							('c2',float),
							('mass_density', float),
							('px',float),
							('py',float),
							('pz',float),
							('total_energy_density',float),
							('bx',float),
							('by',float),
							('bz',float),
							('jx',float),
							('jy',float),
							('jz',float),
							('cell_type',int),
							('mpi_rank',int),
							('electric_resistivity',float),
							('cell_id',int)
							])
	mhd_data = np.array(mhd_data, dtype=mhd_dtype)

	return mhd_data.view(np.recarray)

def set_positions(self):
	np.sort(self.mhd_data, order=['c0','c1','c2'])
	self.unique_points = np.unique(self.mhd_data.c0), np.unique(self.mhd_data.c1), np.unique(self.mhd_data.c2)
	self.res_3D = tuple([len(u) for u in self.unique_points]) # (n0,n1,n2)

	self._select = tuple([i for i in range(3) if self.res_3D[i] > 1]) # e.g. (0,2) if n1 = 1 
	
	if self.res_3D[0]*self.res_3D[1]*self.res_3D[2] == len(self.mhd_data):
		self.resolution = tuple([self.res_3D[s] for s in self._select]) # e.g. (n0,n2) if n1 = 1
		self.sparse_grid = tuple([self.unique_points[s] for s in self._select])
		self.mhd_data = self.mhd_data.reshape(self.resolution)
	else:
		raise ArithmeticError('Could not construct regular grid')


if __name__ == '__main__':
    main(sys.argv[1:])