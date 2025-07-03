#!/usr/bin/env python3
"""
Colonel Katie Installation Verification Script
Comprehensive testing of all components and features
"""

import sys
import os
import importlib
from pathlib import Path

class ColonelKatieVerifier:
    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.passed_tests = 0
        self.total_tests = 0
        
    def print_header(self):
        print("=" * 70)
        print("🔍 COLONEL KATIE - INSTALLATION VERIFICATION 🔍")
        print("=" * 70)
        print("Testing all components and integrations...")
        print()
        
    def test_core_imports(self):
        """Test core application imports."""
        print("🧪 Testing Core Imports...")
        
        tests = [
            ("Main Window", "gui.desktop.main_window", "ColonelKDEApp"),
            ("Agent Builder", "gui.desktop.agent_builder_dialog", "AgentBuilderDialog"),
            ("Chat Window", "gui.desktop.chat_window", "ChatWindow"),
            ("Right Sidebar", "gui.desktop.right_sidebar", "RightSidebar"),
        ]
        
        for name, module_path, class_name in tests:
            self.total_tests += 1
            try:
                module = importlib.import_module(module_path)
                cls = getattr(module, class_name)
                print(f"   ✅ {name}: {class_name}")
                self.passed_tests += 1
            except Exception as e:
                print(f"   ❌ {name}: {e}")
                
    def test_services(self):
        """Test service layer components."""
        print("\n🔧 Testing Services...")
        
        services = [
            ("Prompt Library", "gui.desktop.services.prompt_library", "PromptLibrary"),
            ("Model Manager", "gui.desktop.services.model_manager", "ModelManager"),
            ("Chat Manager", "gui.desktop.services.chat_manager", "ChatManager"),
            ("Memory Service", "gui.desktop.services.memory_service", "MemoryService"),
            ("RAG Manager", "gui.desktop.services.rag_manager", "RAGManager"),
            ("TTS Service", "gui.desktop.services.tts_service", "TTSService"),
            ("STT Service", "gui.desktop.services.stt_service", "STTService"),
        ]
        
        for name, module_path, class_name in services:
            self.total_tests += 1
            try:
                module = importlib.import_module(module_path)
                cls = getattr(module, class_name)
                print(f"   ✅ {name}: {class_name}")
                self.passed_tests += 1
            except Exception as e:
                print(f"   ❌ {name}: {e}")
                
    def test_components(self):
        """Test UI components."""
        print("\n🎨 Testing UI Components...")
        
        components = [
            ("Enhanced Status Bar", "gui.desktop.components.enhanced_status_bar", "EnhancedStatusBar"),
            ("Animated Button", "gui.desktop.components.animated_button", "AnimatedButton"),
            ("Document Manager", "gui.desktop.components.document_manager", "DocumentManager"),
            ("Memory Manager", "gui.desktop.components.memory_manager_component", "MemoryManagerComponent"),
        ]
        
        for name, module_path, class_name in components:
            self.total_tests += 1
            try:
                module = importlib.import_module(module_path)
                cls = getattr(module, class_name)
                print(f"   ✅ {name}: {class_name}")
                self.passed_tests += 1
            except Exception as e:
                print(f"   ❌ {name}: {e}")
                
    def test_prompt_library(self):
        """Test prompt library functionality."""
        print("\n📚 Testing Prompt Library...")
        
        self.total_tests += 3
        try:
            from gui.desktop.services.prompt_library import PromptLibrary
            library = PromptLibrary()
            
            # Test prompt loading
            prompts = library.get_prompt_names()
            if len(prompts) >= 10:
                print(f"   ✅ Prompt Templates: {len(prompts)} loaded")
                self.passed_tests += 1
            else:
                print(f"   ❌ Prompt Templates: Only {len(prompts)} loaded (expected 10+)")
                
            # Test categories
            categories = library.get_all_categories()
            if len(categories) >= 8:
                print(f"   ✅ Categories: {len(categories)} found")
                self.passed_tests += 1
            else:
                print(f"   ❌ Categories: Only {len(categories)} found (expected 8+)")
                
            # Test search functionality
            search_results = library.search_prompts("code")
            if search_results:
                print(f"   ✅ Search: Found {len(search_results)} code-related prompts")
                self.passed_tests += 1
            else:
                print("   ❌ Search: No results for 'code' query")
                
        except Exception as e:
            print(f"   ❌ Prompt Library Error: {e}")
            
    def test_file_structure(self):
        """Test required files and directories."""
        print("\n📁 Testing File Structure...")
        
        required_files = [
            "main.py",
            "README.md",
            "requirements.txt",
            "install.py",
            "DEVELOPMENT_ROADMAP.md",
            "docs/USER_GUIDE.md",
            "gui/desktop/main_window.py",
            "gui/desktop/services/prompt_library.py",
        ]
        
        for file_path in required_files:
            self.total_tests += 1
            full_path = self.current_dir / file_path
            if full_path.exists():
                print(f"   ✅ {file_path}")
                self.passed_tests += 1
            else:
                print(f"   ❌ {file_path} - Missing")
                
    def test_dependencies(self):
        """Test critical dependencies."""
        print("\n📦 Testing Dependencies...")
        
        critical_deps = [
            ("PySide6", "PySide6"),
            ("OpenInterpreter", "interpreter"),
            ("Python-dotenv", "dotenv"),
            ("Markdown-it", "markdown_it"),
            ("Pygments", "pygments"),
            ("PSUtil", "psutil"),
        ]
        
        for name, module_name in critical_deps:
            self.total_tests += 1
            try:
                importlib.import_module(module_name)
                print(f"   ✅ {name}")
                self.passed_tests += 1
            except ImportError:
                print(f"   ❌ {name} - Not installed")
                
    def run_verification(self):
        """Run complete verification suite."""
        self.print_header()
        
        # Add current directory to path for imports
        sys.path.insert(0, str(self.current_dir))
        
        # Run all tests
        self.test_file_structure()
        self.test_dependencies()
        self.test_core_imports()
        self.test_services()
        self.test_components()
        self.test_prompt_library()
        
        # Print results
        self.print_results()
        
    def print_results(self):
        """Print verification results."""
        print("\n" + "="*70)
        print("📊 VERIFICATION RESULTS")
        print("="*70)
        
        success_rate = (self.passed_tests / self.total_tests) * 100
        
        print(f"Tests Passed: {self.passed_tests}/{self.total_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 95:
            print("\n🎉 EXCELLENT! Colonel Katie is ready for production!")
            print("🚀 All core systems verified and operational.")
        elif success_rate >= 85:
            print("\n✅ GOOD! Colonel Katie is functional with minor issues.")
            print("⚠️  Some optional features may need attention.")
        elif success_rate >= 70:
            print("\n⚠️  WARNING! Colonel Katie has significant issues.")
            print("🔧 Several components need fixes before production use.")
        else:
            print("\n❌ CRITICAL! Colonel Katie installation has major problems.")
            print("🚨 Extensive troubleshooting required.")
            
        print("\n📋 Recommendations:")
        if success_rate < 100:
            print("   • Check missing dependencies with: pip install -r requirements.txt")
            print("   • Verify file permissions and directory structure")
            print("   • Review error messages above for specific issues")
        
        print("   • Run the application: python main.py")
        print("   • Check documentation: docs/USER_GUIDE.md")
        print("   • Report issues: GitHub Issues")
        
        print("\n🦄⚡ Colonel Katie - AI Agent Development Platform ⚡🦄")
        print("="*70)

def main():
    """Main verification function."""
    verifier = ColonelKatieVerifier()
    verifier.run_verification()

if __name__ == "__main__":
    main()