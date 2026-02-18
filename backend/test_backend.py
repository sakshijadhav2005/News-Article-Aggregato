"""
Simple test script to verify backend is working
Run: python test_backend.py
"""
import sys
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure backend is running: python -m uvicorn src.main:app --reload")
        return False

def test_fetch_articles():
    """Test article fetching"""
    print("\n🔍 Testing article fetch...")
    try:
        response = requests.post(f"{BASE_URL}/articles/fetch")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Article fetch passed: {data.get('message')}")
            return True
        else:
            print(f"❌ Article fetch failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Article fetch error: {e}")
        return False

def test_list_articles():
    """Test listing articles"""
    print("\n🔍 Testing article listing...")
    try:
        response = requests.get(f"{BASE_URL}/articles")
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            print(f"✅ Article listing passed: {total} articles found")
            return True
        else:
            print(f"❌ Article listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Article listing error: {e}")
        return False

def test_get_clusters():
    """Test getting clusters"""
    print("\n🔍 Testing clusters...")
    try:
        response = requests.get(f"{BASE_URL}/clusters")
        if response.status_code == 200:
            data = response.json()
            clusters = data.get('data', [])
            print(f"✅ Clusters passed: {len(clusters)} clusters found")
            for cluster in clusters:
                print(f"   - {cluster['label']}: {cluster['article_count']} articles")
            return True
        else:
            print(f"❌ Clusters failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Clusters error: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 News Aggregator Backend Test")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ Backend is not running!")
        print("   Start it with: python -m uvicorn src.main:app --reload")
        sys.exit(1)
    
    # Test fetch
    test_fetch_articles()
    
    # Test list
    test_list_articles()
    
    # Test clusters
    test_get_clusters()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Open http://localhost:8000/docs for API documentation")
    print("   2. Start frontend: cd frontend && npm run dev")
    print("   3. Open http://localhost:5173 in your browser")
    print("\n✨ Your News Aggregator is ready!")

if __name__ == "__main__":
    main()
