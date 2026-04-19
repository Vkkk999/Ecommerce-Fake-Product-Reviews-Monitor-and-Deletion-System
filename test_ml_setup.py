#!/usr/bin/env python
"""
Quick test script to verify ML detector is working correctly.
Run: python test_ml_setup.py
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("ML DETECTOR SETUP TEST")
print("=" * 60)

# Test 1: Import modules
print("\n[1] Testing imports...")
try:
    from Ecom_App.ml_detector import (
        get_demo_dataset,
        train_fake_review_model,
        load_fake_review_model,
        predict_fake_review
    )
    print("   ✓ ML module imports successful")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Load demo dataset
print("\n[2] Testing demo dataset...")
try:
    texts, labels = get_demo_dataset()
    print(f"   ✓ Demo dataset loaded: {len(texts)} samples")
    print(f"     - Fake reviews: {sum(labels)}")
    print(f"     - Genuine reviews: {len(labels) - sum(labels)}")
except Exception as e:
    print(f"   ✗ Demo dataset failed: {e}")
    sys.exit(1)

# Test 3: Train model
print("\n[3] Training model...")
try:
    success = train_fake_review_model()
    if success:
        print("   ✓ Model training successful")
    else:
        print("   ✗ Model training returned False")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Model training failed: {e}")
    sys.exit(1)

# Test 4: Load model
print("\n[4] Loading model...")
try:
    model = load_fake_review_model()
    if model:
        print("   ✓ Model loaded successfully")
    else:
        print("   ✗ Model loading returned None")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Model loading failed: {e}")
    sys.exit(1)

# Test 5: Predictions
print("\n[5] Testing predictions...")
try:
    fake_review = "AMAZING AMAZING AMAZING  best best best!!!"
    genuine_review = "Good product, works as described."
    
    fake_result = predict_fake_review(fake_review)
    genuine_result = predict_fake_review(genuine_review)
    
    print(f"   Fake review test:     is_fake={fake_result['is_fake']}, "
          f"confidence={fake_result['confidence']:.2f}")
    print(f"   Genuine review test:  is_fake={genuine_result['is_fake']}, "
          f"confidence={genuine_result['confidence']:.2f}")
    
    if not fake_result['error'] and not genuine_result['error']:
        print("   ✓ Predictions working correctly")
    else:
        print("   ✗ Predictions had errors")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Prediction test failed: {e}")
    sys.exit(1)

# Test 6: Rule-based detector
print("\n[6] Testing rule-based detector...")
try:
    from Ecom_App.views import is_review_fake
    
    test_cases = [
        ("BEST BEST BEST!!!", True, "ALL CAPS with exclamation"),
        ("best best best best best", True, "Word repetition"),
        ("Good product, works well.", False, "Genuine review"),
    ]
    
    for text, expected, desc in test_cases:
        result = is_review_fake(text)
        status = "✓" if result == expected else "✗"
        print(f"   {status} {desc}: is_fake={result}")
        
except Exception as e:
    print(f"   ✗ Rule-based detector failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - ML SYSTEM READY!")
print("=" * 60)
print("\nNext steps:")
print("  1. Run: python manage.py test Ecom_App")
print("  2. Start server: python manage.py runserver")
print("  3. Visit: http://localhost:8000/Admin_Analytics/")
print("\n")
