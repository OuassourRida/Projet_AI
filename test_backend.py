#!/usr/bin/env python3
"""Standalone test tool for backend API - no frontend needed."""

import requests
import json
import sys
from pathlib import Path

# Ensure we can import the backend module
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'app'))

def test_health():
    """Test health endpoint."""
    print("\n📋 Test 1: Health Check")
    print("-" * 50)
    try:
        resp = requests.get('http://localhost:5000/health', timeout=3)
        print(f"✅ Status: {resp.status_code}")
        print(f"Response: {resp.json()}")
        return resp.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_recommendations(hotels, top_k=5):
    """Test recommendations endpoint."""
    print(f"\n📋 Test 2: Recommendations")
    print(f"Input: {hotels}, top_k={top_k}")
    print("-" * 50)
    try:
        payload = {'hotels': hotels, 'top_k': top_k}
        resp = requests.post(
            'http://localhost:5000/recommendations',
            json=payload,
            timeout=5
        )
        print(f"✅ Status: {resp.status_code}")
        data = resp.json()
        
        if 'recommendations' in data:
            recs = data['recommendations']
            print(f"📊 Found {len(recs)} recommendations:")
            for i, rec in enumerate(recs, 1):
                print(f"\n  {i}. {rec.get('name')} (ID: {rec.get('id')})")
                print(f"     Category: {rec.get('category')}")
                print(f"     Location: {rec.get('location')}")
                print(f"     Rating: ⭐ {rec.get('avg_rating', 'N/A')}")
        else:
            print(f"Response: {json.dumps(data, indent=2)}")
        
        return resp.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_direct_import():
    """Test backend function directly (no API call)."""
    print(f"\n📋 Test 3: Direct Backend Function")
    print("-" * 50)
    try:
        from models.knn_recommender import recommend
        
        hotels = ['La Mamounia', 'H002']
        print(f"Input: {hotels}, top_k=5")
        
        recs = recommend(hotels, top_k=5)
        print(f"✅ Direct call successful")
        print(f"📊 Found {len(recs)} recommendations:")
        
        for i, rec in enumerate(recs, 1):
            print(f"\n  {i}. {rec.get('name')} (ID: {rec.get('id')})")
            print(f"     Rating: ⭐ {rec.get('avg_rating', 'N/A')}")
        
        return len(recs) > 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("🏨 Backend API Tests")
    print("="*50)
    
    # Test 1: Direct function call (doesn't need server)
    print("\n" + "="*50)
    print("Testing Backend Function (No Server Needed)")
    print("="*50)
    success1 = test_direct_import()
    
    # Test 2 & 3: API calls (need server running)
    print("\n" + "="*50)
    print("Testing API Endpoints (Server Must Be Running)")
    print("="*50)
    
    try:
        success2 = test_health()
        success3 = test_recommendations(['La Mamounia'], top_k=5)
        success4 = test_recommendations(['H001', 'H002'], top_k=3)
    except requests.exceptions.ConnectionError:
        print("\n⚠️  Cannot connect to server at http://localhost:5000")
        print("Make sure backend is running: bash start_backend.sh")
        success2 = success3 = success4 = False
    
    # Summary
    print("\n" + "="*50)
    print("📊 Test Summary")
    print("="*50)
    tests = [
        ("Direct Backend Function", success1),
        ("Health Check API", success2),
        ("Recommendations API (Test 1)", success3),
        ("Recommendations API (Test 2)", success4),
    ]
    
    for name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(s for _, s in tests)
    print("\n" + ("="*50))
    if all_passed:
        print("✨ Tous les tests sont passés!")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return 0 if success1 else 1


if __name__ == '__main__':
    sys.exit(main())
