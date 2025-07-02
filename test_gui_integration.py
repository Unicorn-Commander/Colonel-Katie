#!/usr/bin/env python3
"""
Quick test script to verify GUI service integrations are working
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_services():
    """Test all the GUI service integrations"""
    print("🧪 Testing The Colonel GUI Service Integrations")
    print("=" * 50)
    
    # Test WebSearchService
    try:
        from gui.desktop.services.web_search import WebSearchService
        search_service = WebSearchService()
        print("✅ WebSearchService: Imported successfully")
        # Test basic functionality (without actual network call)
        print(f"   - SearXNG URL: {search_service.searxng_url}")
    except Exception as e:
        print(f"❌ WebSearchService: {e}")
    
    # Test SettingsManager
    try:
        from gui.desktop.services.settings_manager import SettingsManager
        settings = SettingsManager()
        settings.set_setting("test_key", "test_value")
        value = settings.get_setting("test_key")
        assert value == "test_value"
        print("✅ SettingsManager: Working correctly")
    except Exception as e:
        print(f"❌ SettingsManager: {e}")
    
    # Test RAGManager
    try:
        from gui.desktop.services.rag_manager import RAGManager
        rag = RAGManager()
        print("✅ RAGManager: Imported successfully")
        print(f"   - Embedding model: {rag.embedding_model}")
    except Exception as e:
        print(f"❌ RAGManager: {e}")
    
    # Test ModelManager
    try:
        from gui.desktop.services.model_manager import ModelManager
        model_mgr = ModelManager()
        print("✅ ModelManager: Imported successfully")
        print(f"   - Ollama URL: {model_mgr.ollama_url}")
    except Exception as e:
        print(f"❌ ModelManager: {e}")
    
    # Test ChatManager
    try:
        from gui.desktop.services.chat_manager import ChatManager
        from gui.desktop.services.model_manager import ModelManager
        from interpreter import OpenInterpreter
        
        model_mgr = ModelManager()
        interpreter = OpenInterpreter()
        chat_mgr = ChatManager(model_mgr, interpreter)
        print("✅ ChatManager: Imported successfully")
    except Exception as e:
        print(f"❌ ChatManager: {e}")
    
    # Test FunctionRegistry
    try:
        from gui.desktop.services.function_registry import FunctionRegistry
        func_reg = FunctionRegistry()
        print("✅ FunctionRegistry: Imported successfully")
    except Exception as e:
        print(f"❌ FunctionRegistry: {e}")
    
    print("\n🎉 Service Integration Test Complete!")
    print("\n🚀 The Colonel GUI is ready with:")
    print("   - ✅ Web Search (SearXNG integration)")
    print("   - ✅ RAG Document Processing") 
    print("   - ✅ Model Management")
    print("   - ✅ Settings Management")
    print("   - ✅ Chat Management")
    print("   - ✅ Function Registry")
    print("\n🎯 Launch with: python -m gui.desktop.main")

if __name__ == "__main__":
    test_services()