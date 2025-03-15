#sample data
'''
[1.33034607,1.19513603,1.02067693,0.81365557,0.58485772,0.34723182, 0.11357884,0.0,0.0,0.0,0.10580655,
        0.21556823, 0.29772605, 0.35437419, 0.38764359, 0.39942618, 0.39129295, 0.36455025, 0.32039769, 0.2601728,
        0.18569587, 0.0998161,  0.00765579, 0.0, 0.0,0.0, 0.00469201, 0.09628542, 0.18169324, 0.25582941, 0.31594177,
        0.36033084, 0.38780095, 0.39732482, 0.38781245, 0.35796572, 0.30622562, 0.23083686, 0.13006671, 0.00262426, 0.0,
        0.0, 0.0319749,  0.25048252, 0.47662707, 0.70000614, 0.90940805, 1.09433158]
'''

data = [1.33034607,1.19513603,1.02067693,0.81365557,0.58485772,0.34723182, 0.11357884,0.0,0.0,0.0,0.10580655,
        0.21556823, 0.29772605, 0.35437419, 0.38764359, 0.39942618, 0.39129295, 0.36455025, 0.32039769, 0.2601728,
        0.18569587, 0.0998161,  0.00765579, 0.0, 0.0,0.0, 0.00469201, 0.09628542, 0.18169324, 0.25582941, 0.31594177,
        0.36033084, 0.38780095, 0.39732482, 0.38781245, 0.35796572, 0.30622562, 0.23083686, 0.13006671, 0.00262426, 0.0,
        0.0, 0.0319749,  0.25048252, 0.47662707, 0.70000614, 0.90940805, 1.09433158]

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


def reshape_to_10x10(array):
    """
    Reshape any array to a 10x10 matrix using interpolation.
    """
    # Determine the original shape
    original_length = len(array)
    original_size = int(np.ceil(np.sqrt(original_length)))

    # Reshape the original array to a square matrix (might have padding)
    original_matrix = np.pad(array, (0, original_size ** 2 - original_length), 'constant')
    original_matrix = original_matrix.reshape(original_size, original_size)

    # Create coordinates for the original matrix
    x_orig = np.linspace(0, 1, original_size)
    y_orig = np.linspace(0, 1, original_size)
    X_orig, Y_orig = np.meshgrid(x_orig, y_orig)

    # Create coordinates for the target 10x10 matrix
    x_target = np.linspace(0, 1, 10)
    y_target = np.linspace(0, 1, 10)
    X_target, Y_target = np.meshgrid(x_target, y_target)

    # Flatten the original coordinates and values for interpolation
    points = np.column_stack((X_orig.flatten(), Y_orig.flatten()))
    values = original_matrix.flatten()

    # Perform interpolation to get 10x10 matrix
    matrix_10x10 = griddata(points, values, (X_target, Y_target), method='cubic')

    # Fill any NaN values that might occur during interpolation
    if np.isnan(matrix_10x10).any():
        matrix_10x10 = np.nan_to_num(matrix_10x10, nan=np.nanmean(matrix_10x10))

    return matrix_10x10, X_target, Y_target


# Define both random arrays
random_array = np.array([
    0.69935256, 0.4188343, 0.46922909, 0.50996807, 0.42327686, 0.46424802,
    0.52712323, 0.66655355, 0.28070822, 0.80457604, 0.35276328, 0.01660237,
    0.69874535, 0.8969703, 0.63637249, 0.6979229, 0.28983526, 0.66852897,
    0.42433465, 0.73759059, 0.47504017, 0.91865827, 0.39735647, 0.95383332,
    0.45858451, 0.01660237, 0.69874535
])

# random_array2 = np.array([
#     0.69935256, 0.4188343, 0.46922909, 0.50996807, 0.42327686, 0.46424802,
#     0.52712323, 0.66655355, 0.28070822, 0.80457604, 0.35276328, 0.01660237,
#     0.69874535, 0.8969703, 0.63637249, 0.6979229, 0.28983526, 0.66852897,
#     0.42433465, 0.73759059, 0.47504017, 0.91865827, 0.39735647, 0.95383332,
#     0.45858451, 0.01660237, 0.69874535, 0.01660237, 0.69874535, 0.01660237,
#     0.69874535, 0.01660237, 0.69874535
# ])

# Reshape both arrays into 10x10 matrices with interpolation
matrix1, X1, Y1 = reshape_to_10x10(random_array)
# matrix2, X2, Y2 = reshape_to_10x10(random_array2)

# Create the figure and subplots for comparison
fig, ax = plt.subplots(figsize=(7, 5))

# Plot the first contour heatmap
contour1 = ax.contourf(X1, Y1, matrix1, cmap='jet', levels=20)
contour_lines1 = ax.contour(X1, Y1, matrix1, colors='black', linewidths=0.8)
fig.colorbar(contour1, ax=ax, label="Value")
ax.clabel(contour_lines1, inline=True, fontsize=8)
ax.set_title("Contour Heatmap of random_array (10x10)")
ax.set_xlabel("X-Axis")
ax.set_ylabel("Y-Axis")
ax.grid(True, linestyle='--', alpha=0.5)

# Plot the second contour heatmap
# contour2 = axs[1].contourf(X2, Y2, matrix2, cmap='jet', levels=20)
# contour_lines2 = axs[1].contour(X2, Y2, matrix2, colors='black', linewidths=0.8)
# fig.colorbar(contour2, ax=axs[1], label="Value")
# axs[1].clabel(contour_lines2, inline=True, fontsize=8)
# axs[1].set_title("Contour Heatmap of random_array2 (10x10)")
# axs[1].set_xlabel("X-Axis")
# axs[1].set_ylabel("Y-Axis")
# axs[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()