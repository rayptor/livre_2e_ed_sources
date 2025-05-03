import numpy as np

def kronecker(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    r = a.shape[0]
    s = a.shape[1]
    t = b.shape[0]
    u = b.shape[1]
    c = np.zeros((r*t,s*u))
    for i in range(0,r):
        for j in range(0,s):
            for k in range(0,t):
                for l in range(0,u):
                     c[k+i*t,l+j*u] = a[i,j] * b[k,l]
    return c

def kronecker_somme(a: np.array, b: np.array) -> np.array:
	ia = np.identity(a.shape[0])
	ib = np.identity(b.shape[0])
	return kronecker(a,ib) + kronecker(ia,b)


if __name__ == "__main__":
    a = np.array([[3,2],[4,-1]])
    b = np.array([[1,-1,2],[3,-2,4],[-1,-2,5]])
    k = kronecker(a,b)
    print(f"A x B = \n{k}")


    a = np.array([[-3,4,9],[6,2,8],[-5,7,-4]])
    b = np.array([[-2,-9],[6,-3]])
    k = kronecker_somme(a,b)
    print(f"A + B = \n{k}")
