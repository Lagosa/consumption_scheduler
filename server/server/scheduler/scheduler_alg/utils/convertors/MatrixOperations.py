import numpy as np

def reshape_flat_matrix(solution, shape):
    return np.reshape(solution, shape)


def add_padding_column(matrix):
    padding_column = np.ones((matrix.shape[0], 1))
    matrix_padded = np.hstack((padding_column, matrix))

    return matrix_padded

def multiply_with_first_col(matrix):
    first_column = matrix[:, 0]
    first_column_transposed = first_column.reshape(-1, 1)
    matrix_without_first_col = matrix[:, 1:]

    subset_schedule = first_column_transposed * matrix_without_first_col

    return subset_schedule
