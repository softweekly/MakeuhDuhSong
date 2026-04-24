#!/usr/bin/env python3
"""
Startup script for Parody Song Creator
Choose between CLI and Web interface
"""

import sys
import os

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import elevenlabs
        import openai
        from dotenv import load_dotenv
        import flask
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if environment variables are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    missing = []
    if not os.getenv("ELEVENLABS_API_KEY"):
        missing.append("ELEVENLABS_API_KEY")
    if not os.getenv("OPENAI_API_KEY"):
        missing.append("OPENAI_API_KEY")
    
    if missing:
        print(f"❌ Missing API keys: {', '.join(missing)}")
        print("💡 Add them to your .env file")
        return False
    
    print("✅ Environment variables are configured")
    return True

def show_menu():
    """Show startup menu"""
    print("\n🎭 Welcome to Parody Song Creator! 🎵")
    print("=" * 50)
    print("⚠️  IMPORTANT: Music generation complies with ElevenLabs policies")
    print("   (Cannot create tracks that sound like specific copyrighted songs)")
    print("✅ All lyric writing features work perfectly for parody creation!")
    print()
    print("How would you like to use the tool?")
    print()
    print("1. 💻 Command Line Interface (CLI)")
    print("   - Interactive text-based interface")
    print("   - Great for focused songwriting")
    print("   - Run: python parody_song_creator.py")
    print()
    print("2. 🌐 Web Interface")
    print("   - Browser-based visual interface")
    print("   - Better for collaboration and sharing")
    print("   - Run: python web_app.py")
    print()
    print("3. 🔧 Setup & Configuration")
    print("   - Check requirements and API keys")
    print("   - View project structure")
    print()
    print("4. 📖 Help & Documentation")
    print("   - View README and usage tips")
    print()
    print("5. 🚀 Future Features (AI Agent Roadmap)")
    print("   - See planned expansions")
    print()
    print("0. 👋 Exit")
    print()

def run_cli():
    """Run the CLI version"""
    try:
        from parody_song_creator import ParodyCreatorCLI
        cli = ParodyCreatorCLI()
        cli.run()
    except ImportError:
        print("❌ CLI module not found. Please check your installation.")
    except KeyboardInterrupt:
        print("\n👋 Goodbye from CLI!")

def run_web():
    """Run the web version"""
    print("\n🌐 Starting web interface...")
    print("📍 The web app will be available at: http://localhost:5000")
    print("🔗 Open this URL in your browser")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        import web_app
        web_app.app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError:
        print("❌ Web app module not found. Please check your installation.")
    except KeyboardInterrupt:
        print("\n👋 Web server stopped!")

def show_setup():
    """Show setup information"""
    print("\n🔧 Setup & Configuration")
    print("=" * 30)
    
    # Check requirements
    print("\n📦 Package Requirements:")
    if check_requirements():
        print("✅ All packages installed")
    else:
        print("❌ Some packages missing")
    
    print("\n🔑 API Key Configuration:")
    if check_environment():
        print("✅ API keys configured")
    else:
        print("❌ API keys missing")
    
    print("\n📁 Project Structure:")
    print("parody_song_creator.py  - Main CLI application")
    print("web_app.py             - Web interface")
    print("requirements.txt       - Python dependencies")
    print(".env                   - Environment variables")
    print("templates/             - Web interface templates")
    print("parody_projects/       - Saved projects (created on first use)")
    
    print("\n🎯 Quick Start:")
    print("1. pip install -r requirements.txt")
    print("2. Add API keys to .env file")
    print("3. Run this script again and choose CLI or Web")

def show_help():
    """Show help documentation"""
    try:
        with open('README.md', 'r') as f:
            content = f.read()
            # Show first part of README
            lines = content.split('\n')[:50]  # First 50 lines
            print('\n'.join(lines))
            print("\n... (see README.md for complete documentation)")
    except FileNotFoundError:
        print("❌ README.md not found. Please check your installation.")
    
    print("\n" + "="*50)
    print("📋 POLICY COMPLIANCE SUMMARY")
    print("="*50)
    try:
        with open('ELEVENLABS_POLICY_COMPLIANCE.md', 'r') as f:
            policy_content = f.read()
            # Show key points from policy guide
            lines = policy_content.split('\n')
            for line in lines[:30]:  # First 30 lines
                if line.startswith('##') or line.startswith('- ✅') or line.startswith('- ❌'):
                    print(line)
        print("\n... (see ELEVENLABS_POLICY_COMPLIANCE.md for complete policy guide)")
    except FileNotFoundError:
        print("❌ Policy compliance guide not found.")

def show_roadmap():
    """Show future development roadmap"""
    print("\n🚀 AI Agent System Roadmap")
    print("=" * 35)
    
    print("\n📈 Phase 1: Creative Tool Foundation (CURRENT)")
    print("✅ AI-powered lyric writing")
    print("✅ Song structure analysis")
    print("✅ Music generation integration")
    print("✅ Project management system")
    print("✅ Web interface")
    
    print("\n📈 Phase 2: Enhanced Automation")
    print("🔄 Trend analysis for topic suggestions")
    print("🔄 Automated content scheduling")
    print("🔄 Voice cloning capabilities")
    print("🔄 Multi-format export (video, sheet music)")
    print("🔄 Integration with social media platforms")
    
    print("\n📈 Phase 3: Full AI Agent System")
    print("🎯 Autonomous content creation")
    print("🎯 Real-time performance generation")
    print("🎯 Advanced collaboration tools")
    print("🎯 Machine learning from user feedback")
    print("🎯 Integration with steeltoepia.com")
    print("🎯 API for external systems")
    
    print("\n📈 Phase 4: Platform Integration")
    print("🌐 Docker containerization")
    print("🌐 Cloud deployment")
    print("🌐 Multi-user workspaces")
    print("🌐 Analytics and insights dashboard")
    print("🌐 Content marketplace integration")
    
    print("\n💡 Next Steps:")
    print("- Use current version to create parodies")
    print("- Provide feedback for improvements")
    print("- Suggest features for the AI agent system")
    print("- Consider integration requirements for steeltoepia.com")

def main():
    """Main startup function"""
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (0-5): ").strip()
            
            if choice == '1':
                if check_requirements() and check_environment():
                    run_cli()
                else:
                    print("\n❌ Please fix setup issues first (choose option 3)")
                    input("Press Enter to continue...")
                    
            elif choice == '2':
                if check_requirements() and check_environment():
                    run_web()
                else:
                    print("\n❌ Please fix setup issues first (choose option 3)")
                    input("Press Enter to continue...")
                    
            elif choice == '3':
                show_setup()
                input("\nPress Enter to continue...")
                
            elif choice == '4':
                show_help()
                input("\nPress Enter to continue...")
                
            elif choice == '5':
                show_roadmap()
                input("\nPress Enter to continue...")
                
            elif choice == '0':
                print("\n👋 Thanks for using Parody Song Creator!")
                print("🎵 Keep creating amazing parodies! 🎭")
                break
                
            else:
                print("❌ Invalid choice. Please enter 0-5.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()