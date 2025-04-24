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


def reshape_to_10x10_then_normalize(array):
    # Convert to numpy array
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

    # Perform cubic interpolation
    points = np.column_stack((X_orig.flatten(), Y_orig.flatten()))
    values = original_matrix.flatten()
    matrix_10x10 = griddata(points, values, (X_target, Y_target), method='cubic')

    # Handle NaN values by replacing them with the mean
    if np.isnan(matrix_10x10).any():
        matrix_10x10 = np.nan_to_num(matrix_10x10, nan=np.nanmean(matrix_10x10))

    # Normalize the 10x10 matrix after reshaping
    normalized_matrix = normalize_array(matrix_10x10)

    return normalized_matrix, X_target, Y_target


def calculate_contour_cost(matrix, constraints):
    """
    Calculate the cost of a contour based on constraints.

    Parameters:
    - matrix: The normalized 10x10 contour matrix
    - constraints: List of tuples [(x_idx, y_idx, target_value), ...] where:
      - x_idx, y_idx: Indices in the matrix (0-9)
      - target_value: Target value (0 = blue, 1 = red)

    Returns:
    - total_cost: Sum of costs for all constraints
    - costs: Dictionary of individual costs for each constraint
    """
    costs = {}
    total_cost = 0

    for constraint in constraints:
        x_idx, y_idx, target_value = constraint
        actual_value = matrix[y_idx, x_idx]  # Note: y is rows, x is columns

        # Calculate cost: difference between actual and target value
        # If target is 0 (blue), cost increases as actual value approaches 1 (red)
        # If target is 1 (red), cost increases as actual value approaches 0 (blue)
        cost = abs(actual_value - target_value)

        constraint_name = f"({x_idx},{y_idx})"
        costs[constraint_name] = cost
        total_cost += cost

    return total_cost, costs


def plot_contour_with_constraints(matrix, X, Y, constraints=None, title="Contour Heatmap with Constraints"):
    """
    Plot contour heatmap with marked constraint points

    Parameters:
    - matrix: The normalized 10x10 contour matrix
    - X, Y: Meshgrid coordinates
    - constraints: List of tuples [(x_idx, y_idx, target_value), ...]
    - title: Plot title
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot contour
    contour = ax.contourf(X, Y, matrix, cmap='jet', levels=np.linspace(0, 1, 20))
    contour_lines = ax.contour(X, Y, matrix, colors='black', linewidths=0.8)
    fig.colorbar(contour, ax=ax, label="Value (0=Blue, 1=Red)")
    ax.clabel(contour_lines, inline=True, fontsize=8)

    # Mark constraint points
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
                       edgecolor='white', linewidth=1.5, label='Target: Blue')

        if red_points:
            red_x, red_y = zip(*red_points)
            ax.scatter(red_x, red_y, color='red', marker='^', s=100,
                       edgecolor='white', linewidth=1.5, label='Target: Red')

    ax.set_title(title)
    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")
    ax.grid(True, linestyle='--', alpha=0.5)
    if constraints:
        ax.legend(loc='upper right')

    plt.tight_layout()
    return fig, ax


# Example usage of the new functions
if __name__ == "__main__":
    # Get the 10x10 matrices for both datasets (reshape first, then normalize)
    # matrix1, X1, Y1 = reshape_to_10x10_then_normalize(data)
    matrix2, X2, Y2 = reshape_to_10x10_then_normalize(data2)

    # Define constraints - list of (x_idx, y_idx, target_value)
    # target_value: 0 = should be blue, 1 = should be red
    constraints = [
        (5, 1, 0),  # Position (5,1) should be blue (0)
        (7, 8, 0)  # Position (8,8) should be red (1) - adding another constraint as example
    ]

    # Calculate costs for both matrices
    # cost1, detail_cost1 = calculate_contour_cost(matrix1, constraints)
    cost2, detail_cost2 = calculate_contour_cost(matrix2, constraints)

    # print(f"Cost for matrix1: {cost1}")
    # print(f"Detailed costs for matrix1: {detail_cost1}")
    print(f"Cost for matrix2: {cost2}")
    print(f"Detailed costs for matrix2: {detail_cost2}")

    # Plot with constraints highlighted
    # plot_contour_with_constraints(matrix1, X1, Y1, constraints, "Contour Heatmap of Data1 with Constraints")
    plot_contour_with_constraints(matrix2, X2, Y2, constraints, "Contour Heatmap of Data2 with Constraints")

    plt.show()