from scipy import sparse
from scipy.sparse.linalg import spsolve
import numpy as np

class BaselineFiltering:
    def __init__(self, ec_data):
        self.ydata = ec_data                   # Load electric current values to be filtered

    def baseline_asls(self, lam, p, n_iter):   # Asymmetric Least Squares Smoothing (P.Eilers, H.Boelens, 2005)
        L = len(self.ydata)
        D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
        w = np.ones(L)
        for i in range(n_iter):
            W = sparse.spdiags(w, 0, L, L)
            Z = W + lam * D.dot(D.transpose())
            z = spsolve(Z, w * self.ydata)
            w = p * (self.ydata > z) + (1 - p) * (self.ydata < z)
        z = np.where(z < 0, 0, z)
        return z