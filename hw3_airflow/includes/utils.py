from typing import Tuple

import h5py
import numpy as np
import scipy
import scipy.sparse


def serialize_training_dataset(
    X: scipy.sparse.csr_matrix, y: np.ndarray, data_path: str
) -> None:
    f = h5py.File(data_path, "w")
    f.create_dataset("X_data", data=X.data)
    f.create_dataset("X_indices", data=X.indices)
    f.create_dataset("X_indptr", data=X.indptr)
    f.create_dataset("X_shape", data=X.shape)
    f.create_dataset("y", data=y)
    f.close()


def load_training_dataset(data_path: str) -> Tuple[scipy.sparse.csr_matrix, np.ndarray]:
    f = h5py.File(data_path, "r")
    X_d = f["X_data"][()]
    X_i = f["X_indices"][()]
    X_in = f["X_indptr"][()]
    shape = f["X_shape"][()]

    X = scipy.sparse.csr_matrix((X_d, X_i, X_in), shape=shape)
    y = f["y"][()]
    f.close()
    return X, y
