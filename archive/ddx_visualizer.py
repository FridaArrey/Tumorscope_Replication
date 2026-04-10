import matplotlib.pyplot as plt

def plot_diagnostic_space(current_inf, current_var):
    # Theoretical clusters based on clinical ground truth
    # Cancer: Low Dist, High Var
    # TB: High Dist, Low Var
    
    plt.figure(figsize=(10, 6))
    plt.axvspan(0, 15, color='red', alpha=0.1, label='Malignant Zone')
    plt.axhspan(0, 45, color='blue', alpha=0.1, label='Granulomatous Zone')
    
    # Plotting your current sample result
    plt.scatter(current_inf, current_var, color='black', s=200, marker='*', label='Current Patient Sample')
    
    plt.title('Lung Nodule Differential Diagnostic Space')
    plt.xlabel('Infiltration Score (Mean Min-Distance in px)')
    plt.ylabel('Zonation Variance (Std-Dev of Radius in px)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    plt.savefig('diagnostic_decision_space.png')
    print("SUCCESS: Diagnostic scatter plot saved as 'diagnostic_decision_space.png'.")

if __name__ == "__main__":
    # Using your actual results: 5.00 px and 76.89 px
    plot_diagnostic_space(5.00, 76.89)
