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
        # Return original value instead of a default
        return np.zeros_like(array) + (min_val if min_val != 0 else 0)

    return (array - min_val) / (max_val - min_val)


def reshape_to_square_adaptive(array, fill_value=1.0):
    """Reshape array to square with minimal modification (either padding or truncation)"""
    # Convert to numpy array
    array = np.array(array)

    # Calculate original length
    length = len(array)

    # Calculate upper and lower bounds for square size
    size_ceil = int(np.ceil(np.sqrt(length)))  # Upper bound (padding)
    size_floor = int(np.floor(np.sqrt(length)))  # Lower bound (truncation)

    padding_needed = size_ceil ** 2 - length  # Number of elements to add
    truncation_needed = length - size_floor ** 2  # Number of elements to remove

    # Choose the method with minimal modification
    if padding_needed <= truncation_needed:
        matrix_size = size_ceil
        matrix = np.pad(array, (0, padding_needed), 'constant', constant_values=fill_value)
    else:
        matrix_size = size_floor
        matrix = array[:size_floor ** 2]

    return matrix.reshape(matrix_size, matrix_size), matrix_size


def reshape_to_10x10_adaptive_then_normalize(array, fill_value=1.0):
    """Reshape array to square with minimal modification, then interpolate to 10x10"""
    # Get the optimally reshaped square matrix
    original_matrix, original_size = reshape_to_square_adaptive(array, fill_value)

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

    # Handle NaN values by replacing them with the fill_value
    if np.isnan(matrix_10x10).any():
        matrix_10x10 = np.nan_to_num(matrix_10x10, nan=fill_value)

    # Normalize the 10x10 matrix
    normalized_matrix = normalize_array(matrix_10x10)

    return normalized_matrix, X_target, Y_target


# Get the 10x10 matrices for both datasets with adaptive reshaping
matrix1, X1, Y1 = reshape_to_10x10_adaptive_then_normalize(data, fill_value=1.0)
matrix2, X2, Y2 = reshape_to_10x10_adaptive_then_normalize(data2, fill_value=1.0)

# Create a figure with two subplots side by side
fig, axs = plt.subplots(1, 2, figsize=(14, 5))

# Plot first contour heatmap
contour1 = axs[0].contourf(X1, Y1, matrix1, cmap='jet', levels=20)
contour_lines1 = axs[0].contour(X1, Y1, matrix1, colors='black', linewidths=0.8)
fig.colorbar(contour1, ax=axs[0], label="Normalized Value")
axs[0].clabel(contour_lines1, inline=True, fontsize=8)
axs[0].set_title("Contour Heatmap of Data1 (10x10)")
axs[0].set_xlabel("X-Axis")
axs[0].set_ylabel("Y-Axis")
axs[0].grid(True, linestyle='--', alpha=0.5)

# Plot second contour heatmap
contour2 = axs[1].contourf(X2, Y2, matrix2, cmap='jet', levels=np.linspace(0, 1, 20))
contour_lines2 = axs[1].contour(X2, Y2, matrix2, colors='black', linewidths=0.8)
fig.colorbar(contour2, ax=axs[1], label="Normalized Value")
axs[1].clabel(contour_lines2, inline=True, fontsize=8)
axs[1].set_title("Contour Heatmap of Data2 (10x10)")
axs[1].set_xlabel("X-Axis")
axs[1].set_ylabel("Y-Axis")
axs[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()