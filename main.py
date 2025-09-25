# main.py - Main script to run all parts
import os

def main():
    print("=== CORD-19 DATA ANALYSIS PROJECT ===\n")
    print("This project will guide you through analyzing the CORD-19 dataset.")
    print("Please make sure you have downloaded metadata.csv from Kaggle and placed it in the data/ folder.\n")
    
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('visualizations', exist_ok=True)
    
    print("Choose which part to run:")
    print("1. Data Loading and Basic Exploration")
    print("2. Data Cleaning and Preparation") 
    print("3. Data Analysis and Visualization")
    print("4. Run Streamlit Application")
    print("5. Run All Parts Sequentially")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1':
        import part1_exploration
    elif choice == '2':
        import part2_cleaning
    elif choice == '3':
        import part3_analysis
    elif choice == '4':
        print("Starting Streamlit application...")
        print("Please run: streamlit run app.py")
        os.system("streamlit run app.py")
    elif choice == '5':
        print("Running all parts sequentially...\n")
        import part1_exploration
        import part2_cleaning
        import part3_analysis
        print("\n✅ All analysis parts completed!")
        print("🎯 Now you can run the Streamlit app with: streamlit run app.py")
    else:
        print("Invalid choice. Please run 1-5.")

if __name__ == "__main__":
    main()