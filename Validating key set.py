import time
class CSVTupleLoader:
	
	def __init__(self, header=False, nullMarker="?", delimeter=","):
		self._tuples = set()
		self._header = header
		self._nullMarker = nullMarker
		self._delimeter = delimeter
		
	def load(self, filepath):
		self._tuples = set();
		skip = self._header
		with open(filepath, "r") as lines:
			for line in lines:
				if skip:
					skip = False
					continue
				t = line.split(self._delimeter)
				t[len(t)-1] = t[len(t)-1].replace("\n","")
				self._tuples.add(tuple(t))
				
	@property
	def tuples(self):
		return list(self._tuples)
		

	
def violate_key_set(t1:tuple, t2:tuple, k, nullMarker="?"):
	total = all([t1[a]!=nullMarker and t2[a]!=nullMarker for a in k])
	t1k = tuple(t1[a] for a in k)
	t2k = tuple(t2[a] for a in k)
	return (not total) or (t1k==t2k)
	
#K is a key set, for example [0, 1, 2, 3]
def is_key_set(K, tuples, nullMarker="?"):
	tuple_List = []
	for i in range(len(tuples)):
		t1 = tuples[i]
		for j in range(len(tuples)):
			if i == j:
				continue
			t2 = tuples[j]
			if all([violate_key_set(t1, t2, k) for k in K]):
				tuple_List.append(t1)
				break
	return tuple_List
	
	
if __name__ == "__main__":
	loader = CSVTupleLoader()
	loader.load("./bridges.csv")
	file_one = open("bridges.csv","r")
	max_size = len(file_one.readline().split(","))
	print("Max key set:",max_size)
	num = input("Enter key set size:")
	keyset_list = []
	for n in range(int(num)):
		keyset_list.append(n)
	for i in range(1,len(keyset_list)+1):
		keysets = []
		keysets += [keyset_list[:i]]
		key = []
		for j in range(i,len(keyset_list)):
			key += [[keyset_list[j]]]
		keysets += key
		start_time = time.clock()
		total_size = len(loader.tuples)
		v = len(is_key_set(keysets, loader.tuples))
		if v == 0:
			result = "Satisfied"
		else:
			result = "Violated({})".format(v)
		
		print("Key set: {} -> Return Tuples:{} Total size:{} Time:{} seconds".format(keysets, v,total_size,time.clock() - start_time))
		#print("Returned tuples:",is_key_set(keysets, loader.tuples))
		print("This key set is ",result)
	
	
	