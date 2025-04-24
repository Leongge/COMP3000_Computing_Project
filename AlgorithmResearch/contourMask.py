import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from matplotlib.patches import Rectangle

data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
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

def reshape_to_10x10_then_normalize(array):

    #Convert to numpy array
    array = np.array(array)

    # Calculate the original square matrix size
    original_length = len(array)
    original_size = int(np.ceil(np.sqrt(original_length)))

    # Pad the array to fit a square shape
    padded_array = np.pad(array, (0, original_size ** 2 - original_length), 'constant')
    original_matrix = padded_array.reshape(original_size, original_size)

    # Generate original grid
    x_orig = np.linspace(0, 1, original_size)
    y_orig = np.linspace(0, 1, original_size)
    X_orig, Y_orig = np.meshgrid(x_orig, y_orig)

    # Generate target grid (10x10)
    x_target = np.linspace(0, 1, 10)
    y_target = np.linspace(0, 1, 10)
    X_target, Y_target = np.meshgrid(x_target, y_target)

    # Perform interpolation - changed from cubic to linear to avoid negative values
    points = np.column_stack((X_orig.flatten(), Y_orig.flatten()))
    values = original_matrix.flatten()
    matrix_10x10 = griddata(points, values, (X_target, Y_target), method='linear')

    # Handle NaN values by replacing them with the mean
    if np.isnan(matrix_10x10).any():
        matrix_10x10 = np.nan_to_num(matrix_10x10, nan=np.nanmean(matrix_10x10))

    # Normalize the 10x10 matrix after reshaping
    normalized_matrix = normalize_array(matrix_10x10)

    return normalized_matrix, X_target, Y_target

def plot_contour_with_region(matrix, X, Y, region=None, constraints=None, target_value=0,
                             title="Contour Heatmap with Region"):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot contour
    contour = ax.contourf(X, Y, matrix, cmap='jet', levels=np.linspace(0, 1, 20))
    contour_lines = ax.contour(X, Y, matrix, colors='black', linewidths=0.8)
    fig.colorbar(contour, ax=ax, label="Value (0=Blue, 1=Red)")
    ax.clabel(contour_lines, inline=True, fontsize=8)

    # Mark region if provided
    if region is not None:
        x_start, y_start, x_end, y_end = region

        # Ensure indices are within bounds
        x_start = max(0, min(x_start, 9))
        y_start = max(0, min(y_start, 9))
        x_end = max(x_start, min(x_end, 9))
        y_end = max(y_start, min(y_end, 9))

        # Calculate width and height
        width = X[0, x_end] - X[0, x_start]
        height = Y[y_end, 0] - Y[y_start, 0]

        # Draw rectangle
        rect_color = 'blue' if target_value == 0 else 'red'
        rect = Rectangle((X[0, x_start], Y[y_start, 0]), width, height,
                         linewidth=2, edgecolor=rect_color, facecolor='none',
                         linestyle='--', alpha=0.7)
        ax.add_patch(rect)

        # Add annotation with region information
        region_text = f"Target: {'Blue' if target_value == 0 else 'Red'}\nRegion: ({x_start},{y_start}) to ({x_end},{y_end})"
        ax.annotate(region_text, xy=(X[0, x_start], Y[y_start, 0]),
                    xytext=(X[0, x_start], Y[y_start, 0] - 0.1),
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=rect_color, alpha=0.7),
                    ha='left', va='top')

    # Mark constraint points if provided
    if constraints:
        x_coords = [X[0, c[0]] for c in constraints]
        y_coords = [Y[c[1], 0] for c in constraints]
        target_values = [c[2] for c in constraints]

        # Use different markers for blue (square) and red (triangle) targets
        blue_points = [(x, y) for x, y, t in zip(x_coords, y_coords, target_values) if t == 0]
        red_points = [(x, y) for x, y, t in zip(x_coords, y_coords, target_values) if t == 1]

        if blue_points:
            blue_x, blue_y = zip(*blue_points)
            ax.scatter(blue_x, blue_y, color='blue', marker='s', s=100,
                       edgecolor='white', linewidth=1.5, label='Target Point: Blue')

        if red_points:
            red_x, red_y = zip(*red_points)
            ax.scatter(red_x, red_y, color='red', marker='^', s=100,
                       edgecolor='white', linewidth=1.5, label='Target Point: Red')

    ax.set_title(title)
    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")
    ax.grid(True, linestyle='--', alpha=0.5)

    # Add legend if there are constraints or region
    if constraints or region is not None:
        ax.legend(loc='upper right')

    plt.tight_layout()
    return fig, ax

def calculate_region_cost(matrix, region, target_value=0):
    x_start, y_start, x_end, y_end = region

    # Ensure indices are within bounds and x_start <= x_end, y_start <= y_end
    x_start = max(0, min(x_start, 9))
    y_start = max(0, min(y_start, 9))
    x_end = max(x_start, min(x_end, 9))
    y_end = max(y_start, min(y_end, 9))

    # Extract the region from the matrix
    region_matrix = matrix[y_start:y_end + 1, x_start:x_end + 1]

    # Calculate costs for each point in the region
    if target_value == 0:  # Target is blue (0)
        # Cost increases as values approach red (1)
        costs = region_matrix.copy()
    else:  # Target is red (1)
        # Cost increases as values approach blue (0)
        costs = 1 - region_matrix

    total_cost = np.sum(costs)
    mean_cost = np.mean(costs)

    return total_cost, mean_cost, costs

if __name__ == "__main__":
    # Get the 10x10 matrices for both datasets (reshape first, then normalize)
    # matrix1, X1, Y1 = reshape_to_10x10_then_normalize(data)
    matrix2, X2, Y2 = reshape_to_10x10_then_normalize(data)

    example_region = (7, 7, 8, 9)  # (x_start, y_start, x_end, y_end)
    target_value = 0  # 0 = blue target, 1 = red target

    total_cost, mean_cost, cost_matrix = calculate_region_cost(matrix2, example_region, target_value)
    plot_contour_with_region(matrix2, X2, Y2, example_region, target_value=target_value,
                             title=f"Contour with Example Region (Cost: {total_cost:.4f})")

    plt.show()