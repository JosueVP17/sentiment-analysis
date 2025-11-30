def print_metrics(metrics):
    """Prints the training metrics in a readable format."""
    print("\n" + "="*70)
    print(" "*25 + "TRAINING RESULTS")
    print("="*70)
    
    # Accuracy
    print(f"\n📊 ACCURACY:")
    print(f"   Training:  {metrics['train_accuracy']:.2%}")
    print(f"   Testing:   {metrics['test_accuracy']:.2%}")
    
    # Samples
    print(f"\n📈 DATASET:")
    print(f"   Training samples: {metrics['train_samples']}")
    print(f"   Testing samples:  {metrics['test_samples']}")
    print(f"   Classes: {', '.join(metrics['classes'])}")
    
    # Classification Report
    print(f"\n📋 CLASSIFICATION REPORT:")
    print("-"*70)
    print(f"{'Class':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print("-"*70)
    
    for cls in metrics['classes']:
        if cls in metrics['classification_report']:
            m = metrics['classification_report'][cls]
            print(f"{cls:<15} {m['precision']:<12.2%} {m['recall']:<12.2%} {m['f1-score']:<12.2%} {m['support']:<10}")
    
    # Confusion Matrix
    print(f"\n🔢 CONFUSION MATRIX:")
    print("-"*70)
    import numpy as np
    cm = np.array(metrics['confusion_matrix'])
    
    # Header
    print(f"{'Actual \\ Pred':<15}", end="")
    for cls in metrics['classes']:
        print(f"{cls:<12}", end="")
    print()
    print("-"*70)
    
    # Rows
    for i, cls in enumerate(metrics['classes']):
        print(f"{cls:<15}", end="")
        for j in range(len(metrics['classes'])):
            print(f"{cm[i][j]:<12}", end="")
        print()
    
    print("="*70 + "\n")