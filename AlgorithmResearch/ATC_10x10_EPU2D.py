import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

data = [1.33034607, 1.19513603, 1.02067693, 0.81365557, 0.58485772, 0.34723182, 0.11357884, 0.0, 0.0, 0.0, 0.10580655,
        0.21556823, 0.29772605, 0.35437419, 0.38764359, 0.39942618, 0.39129295, 0.36455025, 0.32039769, 0.2601728,
        0.18569587, 0.0998161, 0.00765579, 0.0, 0.0, 0.0, 0.00469201, 0.09628542, 0.18169324, 0.25582941, 0.31594177,
        0.36033084, 0.38780095, 0.39732482, 0.38781245, 0.35796572, 0.30622562, 0.23083686, 0.13006671, 0.00262426, 0.0,
        0.0, 0.0319749, 0.25048252, 0.47662707, 0.70000614, 0.90940805, 1.09433158]

data2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.00271448]




def normalize_array(array):
    """Normalize an array to the range [0,1]"""
    array = np.array(array)
    min_val = np.min(array)
    max_val = np.max(array)

    # Avoid division by zero
    if max_val == min_val:
        return np.zeros_like(array)

    return (array - min_val) / (max_val - min_val)


def reshape_to_10x10(array):
    # First, normalize the array
    normalized_array = normalize_array(array)

    original_length = len(normalized_array)
    original_size = int(np.ceil(np.sqrt(original_length)))

    # Pad the array to fit a square shape
    original_matrix = np.pad(normalized_array, (0, original_size ** 2 - original_length), 'constant')
    original_matrix = original_matrix.reshape(original_size, original_size)

    # Generate original grid
    x_orig = np.linspace(0, 1, original_size)
    y_orig = np.linspace(0, 1, original_size)
    X_orig, Y_orig = np.meshgrid(x_orig, y_orig)

    # Generate target grid (10x10)
    x_target = np.linspace(0, 1, 10)
    y_target = np.linspace(0, 1, 10)
    X_target, Y_target = np.meshgrid(x_target, y_target)

    # Perform cubic interpolation
    points = np.column_stack((X_orig.flatten(), Y_orig.flatten()))
    values = original_matrix.flatten()
    matrix_10x10 = griddata(points, values, (X_target, Y_target), method='cubic')

    # Handle NaN values by replacing them with the mean
    if np.isnan(matrix_10x10).any():
        matrix_10x10 = np.nan_to_num(matrix_10x10, nan=np.nanmean(matrix_10x10))

    return matrix_10x10, X_target, Y_target


# Get the normalized 10x10 matrix
matrix1, X1, Y1 = reshape_to_10x10(data)

# Plot contour heatmap
fig, ax = plt.subplots(figsize=(7, 5))

contour1 = ax.contourf(X1, Y1, matrix1, cmap='jet', levels=20)
contour_lines1 = ax.contour(X1, Y1, matrix1, colors='black', linewidths=0.8)
fig.colorbar(contour1, ax=ax, label="Normalized Value")
ax.clabel(contour_lines1, inline=True, fontsize=8)
ax.set_title("Contour Heatmap of EPU2D (10x10) - Normalized")
ax.set_xlabel("X-Axis")
ax.set_ylabel("Y-Axis")
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
