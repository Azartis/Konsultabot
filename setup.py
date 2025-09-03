"""
Setup script for Konsultabot - EVSU DULAG AI Chatbot
Handles installation and initial configuration
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please upgrade to Python 3.8 or higher")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    # Core dependencies that should install without issues
    core_packages = [
        "python-dotenv",
        "bcrypt",
        "requests",
        "pandas",
        "numpy",
        "pillow",
        "langdetect",
        "regex"
    ]
    
    # AI/ML packages
    ai_packages = [
        "nltk",
        "google-generativeai",
        "sentence-transformers",
        "scikit-learn"
    ]
    
    # Voice packages (may require additional system dependencies)
    voice_packages = [
        "speechrecognition",
        "pyttsx3",
        "pyaudio"
    ]
    
    success_count = 0
    total_packages = len(core_packages) + len(ai_packages) + len(voice_packages)
    
    # Install core packages
    for package in core_packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✓ {package} installed successfully")
            success_count += 1
        else:
            print(f"✗ Failed to install {package}")
    
    # Install AI packages
    for package in ai_packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✓ {package} installed successfully")
            success_count += 1
        else:
            print(f"✗ Failed to install {package}")
    
    # Install voice packages (with error handling)
    for package in voice_packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✓ {package} installed successfully")
            success_count += 1
        else:
            print(f"⚠ Failed to install {package} (voice features may be limited)")
    
    print(f"\nInstallation complete: {success_count}/{total_packages} packages installed")
    return success_count >= len(core_packages) + len(ai_packages)

def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        print("Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✓ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"⚠ NLTK data download failed: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        env_example = Path(".env.example")
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print("✓ Created .env file from template")
            print("📝 Please edit .env file and add your Google AI Studio API key")
        else:
            # Create basic .env file
            env_content = """# Konsultabot Configuration
GOOGLE_API_KEY=your_google_ai_studio_api_key_here
DATABASE_PATH=konsultabot.db
ONLINE_MODE=true
DEFAULT_LANGUAGE=english
"""
            env_file.write_text(env_content)
            print("✓ Created basic .env file")
            print("📝 Please edit .env file and add your Google AI Studio API key")
    else:
        print("✓ .env file already exists")

def test_basic_functionality():
    """Test basic functionality without running the full GUI"""
    try:
        # Test database
        from database import DatabaseManager
        db = DatabaseManager()
        print("✓ Database module working")
        
        # Test language processor
        from language_processor import LanguageProcessor
        processor = LanguageProcessor()
        print("✓ Language processor working")
        
        # Test config
        import config
        print("✓ Configuration module working")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("KONSULTABOT SETUP - EVSU DULAG AI CHATBOT")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("⚠ Some dependencies failed to install")
        print("The application may still work with limited functionality")
    
    # Download NLTK data
    download_nltk_data()
    
    # Create environment file
    create_env_file()
    
    # Test basic functionality
    if test_basic_functionality():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit the .env file and add your Google AI Studio API key")
        print("2. Run the application: python main.py")
        print("3. Register with your EVSU email address")
        print("4. Start chatting with Konsultabot!")
        
        print("\nFor voice features, ensure you have:")
        print("- A working microphone")
        print("- Speakers or headphones")
        print("- Microphone permissions enabled")
        
    else:
        print("\n⚠ Setup completed with some issues")
        print("Check the error messages above and try running setup again")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
