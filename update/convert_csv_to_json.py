import os
import pandas as pd
import json

def csv_to_json():
    """Convert all district CSV files to a single JSON file for the frontend"""
    csv_folder = "slang_data"
    slang_data = {}
    
    # Get all CSV files
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        district_name = csv_file.replace('.csv', '').title()
        csv_path = os.path.join(csv_folder, csv_file)
        
        try:
            df = pd.read_csv(csv_path)
            slang_data[district_name] = {}
            
            for _, row in df.iterrows():
                slang = row.get('slang', '')
                if slang:
                    slang_data[district_name][slang] = {
                        'tamil': str(row.get('tamil', '')),
                        'english': str(row.get('english', '')),
                        'description': str(row.get('description', ''))
                    }
            
            print(f"✓ Loaded {len(slang_data[district_name])} slangs from {district_name}")
        except Exception as e:
            print(f"✗ Error loading {csv_file}: {e}")
    
    # Save as JSON
    output_file = "slang_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(slang_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Successfully created {output_file} with {len(slang_data)} districts!")
    print(f"Total slangs: {sum(len(v) for v in slang_data.values())}")

if __name__ == "__main__":
    csv_to_json()
