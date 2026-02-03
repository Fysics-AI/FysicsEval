"""
================================================================================
Data Format Specification

Before running the evaluation, please ensure your data is organized into the 
following format: a Python List of Dictionaries (List[Dict]).
Each element in the list represents the data for a single question.

Required Keys:
1. "prediction"   (str): The model's output (e.g., "A", "B", "C", "D")
2. "ground_truth" (str): The correct answer (e.g., "A", "B", "C", "D")

Optional Keys:
- "id": Question ID (useful for tracking specific errors in the logs)

【Example Data Structure】:
data = [
    {"id": 1, "prediction": "A", "ground_truth": "A"},  # Correct
    {"id": 2, "prediction": "C", "ground_truth": "B"},  # Incorrect
    {"id": 3, "prediction": "d", "ground_truth": "D"},  # Correct (Case insensitive)
]
================================================================================
"""

from typing import List, Dict, Union

def calculate_mcq_accuracy(results: List[Dict[str, Union[str, int]]]) -> Dict[str, float]:
    """
    Calculates accuracy for Multiple Choice Questions (MCQ).
    
    Args:
        results: A list of dictionaries containing 'prediction' and 'ground_truth'.
        
    Returns:
        A dictionary containing accuracy, correct count, and total count.
    """
    
    if not results:
        print("Warning: The data list is empty.")
        return {"accuracy": 0.0, "correct_count": 0, "total_count": 0}

    correct_count = 0
    total_count = len(results)
    
    # Error logs (Optional: used to print the first few errors for debugging)
    error_logs = []

    for idx, item in enumerate(results):
        # 1. Retrieve prediction and ground truth
        # Use .get() to prevent errors if keys are missing; default to empty string
        pred = str(item.get("prediction", "")).strip()
        truth = str(item.get("ground_truth", "")).strip()

        # 2. Data Cleaning (Normalization)
        # Convert to uppercase for comparison to ignore case differences
        pred_norm = pred.upper()
        truth_norm = truth.upper()

        # 3. Determine Correctness
        if pred_norm == truth_norm:
            correct_count += 1
        else:
            # Record error samples (Log only the first 5 to avoid cluttering the screen)
            if len(error_logs) < 5:
                error_logs.append({
                    "id": item.get("id", idx),
                    "pred": pred,
                    "truth": truth
                })

    # 4. Calculate Metrics
    accuracy = correct_count / total_count if total_count > 0 else 0.0

    # Print detailed results
    print("-" * 30)
    print(f"Evaluation Complete")
    print("-" * 30)
    print(f"Total Samples:   {total_count}")
    print(f"Correct Count:   {correct_count}")
    print(f"Accuracy:        {accuracy:.2%} ({accuracy:.4f})")
    print("-" * 30)
    
    if error_logs:
        print("Top 5 Error Examples:")
        for err in error_logs:
            print(f"  ID: {err['id']} | Pred: {err['pred']} != Truth: {err['truth']}")
        print("-" * 30)

    return {
        "accuracy": accuracy,
        "correct_count": correct_count,
        "total_count": total_count
    }

# ==========================================
# User Usage Example
# ==========================================

if __name__ == "__main__":
    # Simulate data organized by the user
    # Note: Ensure 'prediction' only contains the option letter (e.g., 'A'), 
    # not full sentences (e.g., 'The answer is A').
    user_data = [
        {"id": 101, "prediction": "A", "ground_truth": "A"}, # Correct
        {"id": 102, "prediction": "B", "ground_truth": "A"}, # Incorrect
        {"id": 103, "prediction": "C", "ground_truth": "C"}, # Correct
        {"id": 104, "prediction": "d", "ground_truth": "D"}, # Correct (Code handles case)
        {"id": 105, "prediction": "A", "ground_truth": "C"}, # Incorrect
    ]

    # Run evaluation
    metrics = calculate_mcq_accuracy(user_data)