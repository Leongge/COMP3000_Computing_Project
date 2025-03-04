import numpy as np
import matplotlib.pyplot as plt

def reshape_to_square(array):
    matrix_size = int(np.floor(np.sqrt(len(random_array))))  # 取平方根的整数部分
    matrix = random_array[:matrix_size ** 2].reshape(matrix_size, matrix_size)
    return matrix


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
matrix1 = reshape_to_square(random_array)
matrix2 = reshape_to_square(random_array2)

# Create X, Y coordinates based on matrix shape
matrix_size1 = matrix1.shape[0]
matrix_size2 = matrix2.shape[0]

x1 = np.linspace(0, 1, matrix_size1)
y1 = np.linspace(0, 1, matrix_size1)
X1, Y1 = np.meshgrid(x1, y1)

x2 = np.linspace(0, 1, matrix_size2)
y2 = np.linspace(0, 1, matrix_size2)
X2, Y2 = np.meshgrid(x2, y2)

# Create the figure and subplots for comparison
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Plot the first contour heatmap
contour1 = axs[0].contourf(X1, Y1, matrix1, cmap='jet', levels=20)
contour_lines1 = axs[0].contour(X1, Y1, matrix1, colors='black', linewidths=0.8)
fig.colorbar(contour1, ax=axs[0], label="Value")
axs[0].clabel(contour_lines1, inline=True, fontsize=8)
axs[0].set_title("Contour Heatmap of random_array")
axs[0].set_xlabel("X-Axis")
axs[0].set_ylabel("Y-Axis")
axs[0].grid(True, linestyle='--', alpha=0.5)

# Plot the second contour heatmap
contour2 = axs[1].contourf(X2, Y2, matrix2, cmap='jet', levels=20)
contour_lines2 = axs[1].contour(X2, Y2, matrix2, colors='black', linewidths=0.8)
fig.colorbar(contour2, ax=axs[1], label="Value")
axs[1].clabel(contour_lines2, inline=True, fontsize=8)
axs[1].set_title("Contour Heatmap of random_array2")
axs[1].set_xlabel("X-Axis")
axs[1].set_ylabel("Y-Axis")
axs[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
