import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from matplotlib.patches import Rectangle

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


def calculate_region_cost(matrix, region, target_value=0):
    """
    Calculate the cost of a region in the contour matrix.

    Parameters:
    - matrix: The normalized 10x10 contour matrix
    - region: Tuple (x_start, y_start, x_end, y_end) defining region boundaries (indices 0-9)
      x_start, y_start: Top-left corner
      x_end, y_end: Bottom-right corner (inclusive)
    - target_value: Target value for the entire region (0 = blue, 1 = red)

    Returns:
    - total_cost: Sum of costs for all points in the region
    - mean_cost: Average cost per point in the region
    - region_matrix: Matrix of costs for each point in the region
    """
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


def plot_contour_with_region(matrix, X, Y, region=None, constraints=None, target_value=0,
                             title="Contour Heatmap with Region"):
    """
    Plot contour heatmap with marked region and optional constraint points

    Parameters:
    - matrix: The normalized 10x10 contour matrix
    - X, Y: Meshgrid coordinates
    - region: Tuple (x_start, y_start, x_end, y_end) defining region boundaries
    - constraints: List of tuples [(x_idx, y_idx, target_value), ...]
    - target_value: Target value for the region (0 = blue, 1 = red)
    - title: Plot title
    """
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


def get_region_statistics(matrix, region, target_value=0):
    """
    Get detailed statistics about values in a region.

    Parameters:
    - matrix: The normalized 10x10 contour matrix
    - region: Tuple (x_start, y_start, x_end, y_end) defining region boundaries
    - target_value: Target value (0 = blue, 1 = red)

    Returns:
    - statistics: Dictionary of statistics about the region
    """
    x_start, y_start, x_end, y_end = region

    # Ensure indices are within bounds
    x_start = max(0, min(x_start, 9))
    y_start = max(0, min(y_start, 9))
    x_end = max(x_start, min(x_end, 9))
    y_end = max(y_start, min(y_end, 9))

    # Extract the region
    region_matrix = matrix[y_start:y_end + 1, x_start:x_end + 1]

    # Calculate statistics
    total_cost, mean_cost, _ = calculate_region_cost(matrix, region, target_value)

    statistics = {
        "min_value": np.min(region_matrix),
        "max_value": np.max(region_matrix),
        "mean_value": np.mean(region_matrix),
        "median_value": np.median(region_matrix),
        "std_value": np.std(region_matrix),
        "total_points": region_matrix.size,
        "total_cost": total_cost,
        "mean_cost": mean_cost,
        "target_value": target_value,
        "region_dimensions": f"{x_end - x_start + 1}x{y_end - y_start + 1}"
    }

    return statistics


# Interactive region selection and analysis function
def analyze_contour_region(matrix, X, Y, title="Contour Region Analysis"):
    """
    Interactive function to analyze a contour region:
    1. Plot the contour
    2. Let user define a region and target value
    3. Calculate and display region cost

    Parameters:
    - matrix: The normalized 10x10 contour matrix
    - X, Y: Meshgrid coordinates
    - title: Plot title
    """
    # First, show the contour and get user input
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot contour
    contour = ax.contourf(X, Y, matrix, cmap='jet', levels=np.linspace(0, 1, 20))
    contour_lines = ax.contour(X, Y, matrix, colors='black', linewidths=0.8)
    fig.colorbar(contour, ax=ax, label="Value (0=Blue, 1=Red)")
    ax.clabel(contour_lines, inline=True, fontsize=8)

    ax.set_title("")
    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

    # Get user input for region
    print("\nDefine region by index coordinates (0-9):")
    try:
        x_start = int(input("X start: "))
        y_start = int(input("Y start: "))
        x_end = int(input("X end: "))
        y_end = int(input("Y end: "))

        target_str = input("\nTarget color [b=blue, r=red]: ").lower()
        target_value = 1 if target_str.startswith('r') else 0

        region = (x_start, y_start, x_end, y_end)

        # Calculate costs
        total_cost, mean_cost, cost_matrix = calculate_region_cost(matrix, region, target_value)

        # Get more statistics
        stats = get_region_statistics(matrix, region, target_value)

        # Display results
        print("\n--- Region Analysis Results ---")
        print(f"Region: ({x_start},{y_start}) to ({x_end},{y_end})")
        print(f"Target: {'Red' if target_value == 1 else 'Blue'}")
        print(f"Total Cost: {total_cost:.4f}")
        print(f"Mean Cost: {mean_cost:.4f}")
        print("\nDetailed Statistics:")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")

        # Plot with region highlighted
        plot_contour_with_region(matrix, X, Y, region, target_value=target_value,
                                 title=f"Contour with Selected Region (Cost: {total_cost:.4f})")
        plt.show()

        # Optional: Show cost heatmap for the region
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cost_matrix, cmap='hot', interpolation='nearest')
        ax.set_title(f"Cost Heatmap for Region (Mean: {mean_cost:.4f})")

        # Add coordinates
        for i in range(cost_matrix.shape[1]):
            for j in range(cost_matrix.shape[0]):
                ax.text(i, j, f"{cost_matrix[j, i]:.2f}",
                        ha="center", va="center", color="black" if cost_matrix[j, i] < 0.5 else "white")

        fig.colorbar(im, ax=ax, label="Cost")
        plt.tight_layout()
        plt.show()

        return region, stats

    except ValueError:
        print("Invalid input. Please enter integer values for indices.")
        return None, None


# Example usage of the new functions
if __name__ == "__main__":
    # Get the 10x10 matrices for both datasets (reshape first, then normalize)
    # matrix1, X1, Y1 = reshape_to_10x10_then_normalize(data)
    matrix2, X2, Y2 = reshape_to_10x10_then_normalize(data2)

    # Example 1: Calculate cost for a specific region
    example_region = (2, 3, 4, 5)  # (x_start, y_start, x_end, y_end)
    target_value = 0  # 0 = blue target, 1 = red target

    total_cost, mean_cost, cost_matrix = calculate_region_cost(matrix2, example_region, target_value)
    print(f"Region cost: {total_cost:.4f}, Mean cost: {mean_cost:.4f}")

    # Example 2: Plot contour with highlighted region
    plot_contour_with_region(matrix2, X2, Y2, example_region, target_value=target_value,
                             title=f"Contour with Example Region (Cost: {total_cost:.4f})")
    #
    # Example 3: Interactive region analysis
    print("\nStarting interactive region analysis...")
    analyze_contour_region(matrix2, X2, Y2, "Interactive Region Analysis")