class Museum:
    def __init__(self, value: list[int], weight: list[int], c_max: int) -> None:
        # Store the list of values of items 
        self.value = value
        # Store the list of weights of items 
        self.weight = weight
        # Store the maximum capacity of the knapsack (museum storage)
        self.c_max = c_max
        # Number of items (excluding the unused 0th index)
        self.n = len(value) - 1
        # Placeholder for the DP table 
        self.S = []

    def __optimal_subset_value(self) -> list[list[int]]:
        """
        Build DP matrix S where:
        S[i][c] = max value achievable with first i items and capacity c.
        """
        # Initialize the DP table S with (n+1) rows and (c_max+1) columns filled with zeros
        S = [[0 for _ in range(self.c_max + 1)] for _ in range(self.n + 1)]

        # Loop through each item (1 to n)
        for i in range(1, self.n + 1):
            # Loop through each possible capacity (1 to c_max)
            for c in range(1, self.c_max + 1):
                # If the item is too heavy to fit in current capacity c
                if self.weight[i] > c:
                    # We cannot take this item, so value is same as previous row
                    S[i][c] = S[i - 1][c]
                else:
                    # Otherwise, we have two choices:
                    # Choice 1: exclude the item i
                    option1 = S[i - 1][c]
                    # Choice 2: include the item i (value of item + best we can do with remaining capacity)
                    option2 = self.value[i] + S[i - 1][c - self.weight[i]]
                    # Pick the better of the two options
                    if option1 >= option2:
                        S[i][c] = option1
                    else:
                        S[i][c] = option2

        # Save the DP table to the object
        self.S = S
        # Return the completed DP table
        return S

    def __build_subset(self) -> list[int]:
        """
        Backtrack through S to find which items are in the optimal subset.
        Returns the list of item indices included.
        """
        # Start with an empty list for chosen items
        subset = []
        # Begin from the bottom-right corner of the DP table
        i, c = self.n, self.c_max

        # Work backwards until we reach the top row or leftmost column
        while i > 0 and c > 0:
            # If value is same as the row above, item i was not included
            if self.S[i][c] == self.S[i - 1][c]:
                i -= 1  # move up one row
            else:
                # Otherwise, item i was included in the subset
                subset.append(i)
                # Reduce remaining capacity by the weight of the item
                c -= self.weight[i]
                # Move up one row to continue backtracking
                i -= 1

        # Reverse list so items appear in increasing order
        subset.reverse()
        # Return the list of items included in optimal subset
        return subset

    def solve(self) -> None:
        """
        Solve the knapsack problem and print the required summary.
        """
        # Step 1: Fill in the DP table
        self.__optimal_subset_value()
        # Step 2: Backtrack to get the actual items chosen
        optimal_subset = self.__build_subset()

        # Calculate statistics
        # Total number of subsets possible is 2^n
        total_subsets = 2 ** self.n
        # Total number of cells in the DP table
        matrix_size = (self.n + 1) * (self.c_max + 1)
        # Total weight of chosen items
        total_weight = sum(self.weight[i] for i in optimal_subset)
        # Total value of chosen items
        total_value = sum(self.value[i] for i in optimal_subset)

        # Print solution details
        print("===== Museum Knapsack Solution =====")
        print(f"Theoretical number of subsets: {total_subsets}")
        print(f"Size of DP matrix S: {matrix_size} cells ({self.n+1} x {self.c_max+1})")
        print(f"Number of items in optimal subset: {len(optimal_subset)}")
        print(f"Items chosen: {optimal_subset}")
        print(f"Total weight: {total_weight} (capacity = {self.c_max})")
        print(f"Total value: {total_value}")
        print("===================================")


# Example usage
if __name__ == "__main__":
    # Define values for each item (index 0 unused)
    value = [None, 10, 5, 16, 11]
    # Define weights for each item (index 0 unused)
    weight = [None, 3, 2, 4, 4]
    # Define maximum capacity of the knapsack
    c_max = 10
    # Create a Museum object with these parameters
    small_museum = Museum(value, weight, c_max)
    # Solve the knapsack problem for this museum
    small_museum.solve()
