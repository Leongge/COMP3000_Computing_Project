import numpy as np
import matplotlib.pyplot as plt

def reshape_to_square(array):
    """Reshape an array into the best square matrix by choosing minimal modification (padding or truncation)."""
    length = len(array)
    size_ceil = int(np.ceil(np.sqrt(length)))  # Upper bound (padding)
    size_floor = int(np.floor(np.sqrt(length)))  # Lower bound (truncation)

    padding_needed = size_ceil**2 - length  # Number of zeros to add
    truncation_needed = length - size_floor**2  # Number of elements to remove

    # Choose the method with minimal modification
    if padding_needed < truncation_needed:
        matrix_size = size_ceil
        matrix = np.pad(array, (0, padding_needed), 'constant')
    else:
        matrix_size = size_floor
        matrix = array[:matrix_size**2]

    return matrix.reshape(matrix_size, matrix_size), matrix_size

# Define both random arrays
random_array = np.array([
    0.69935256, 0.4188343 , 0.46922909, 0.50996807, 0.42327686,
    0.46424802, 0.52712323, 0.66655355, 0.28070822, 0.80457604,
    0.35276328, 0.01660237, 0.69874535, 0.8969703 , 0.63637249,
    0.6979229 , 0.28983526, 0.66852897, 0.42433465, 0.73759059,
    0.47504017, 0.91865827, 0.39735647, 0.95383332, 0.45858451,
    0.01660237, 0.69874535
])

random_array2 = np.array([
    0.69935256, 0.4188343 , 0.46922909, 0.50996807, 0.42327686,
    0.46424802, 0.52712323, 0.66655355, 0.28070822, 0.80457604,
    0.35276328, 0.01660237, 0.69874535, 0.8969703 , 0.63637249,
    0.6979229 , 0.28983526, 0.66852897, 0.42433465, 0.73759059,
    0.47504017, 0.91865827, 0.39735647, 0.95383332, 0.45858451,
    0.01660237, 0.69874535, 0.01660237, 0.69874535, 0.01660237,
    0.69874535, 0.01660237, 0.69874535,
])

# Reshape both arrays into square matrices
matrix1, size1 = reshape_to_square(random_array)
matrix2, size2 = reshape_to_square(random_array2)

# Create X, Y coordinates for both matrices
x1 = np.linspace(0, 1, size1)
y1 = np.linspace(0, 1, size1)
X1, Y1 = np.meshgrid(x1, y1)

x2 = np.linspace(0, 1, size2)
y2 = np.linspace(0, 1, size2)
X2, Y2 = np.meshgrid(x2, y2)

# Create the figure and subplots for comparison
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Plot the first contour heatmap
contour1 = axs[0].contourf(X1, Y1, matrix1, cmap='jet', levels=20)
fig.colorbar(contour1, ax=axs[0], label="Value")
axs[0].set_title("Contour Heatmap of random_array")
axs[0].set_xlabel("X-Axis")
axs[0].set_ylabel("Y-Axis")

# Plot the second contour heatmap
contour2 = axs[1].contourf(X2, Y2, matrix2, cmap='jet', levels=20)
fig.colorbar(contour2, ax=axs[1], label="Value")
axs[1].set_title("Contour Heatmap of random_array2")
axs[1].set_xlabel("X-Axis")
axs[1].set_ylabel("Y-Axis")

plt.tight_layout()
plt.show()
