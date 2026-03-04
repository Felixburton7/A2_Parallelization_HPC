import sys
import csv

def check_csv(file1, file2):
    try:
        def filter_comments(f):
            for line in f:
                if line.strip() and not line.startswith('#'):
                    yield line

        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            r1 = list(csv.DictReader(filter_comments(f1)))
            r2 = list(csv.DictReader(filter_comments(f2)))
            
            if len(r1) != len(r2):
                print(f"Length mismatch: {len(r1)} vs {len(r2)}")
                sys.exit(1)
                
            for i, (row1, row2) in enumerate(zip(r1, r2)):
                for col in ['E_kin', 'E_pot']:
                    v1, v2 = float(row1[col]), float(row2[col])
                    diff = abs(v1 - v2)
                    if diff > 1e-12 and diff / (abs(v1) + 1e-18) > 1e-12:
                        print(f"Mismatch at row {i}, col {col}: {v1} vs {v2}")
                        sys.exit(1)
                        
        print("MATCH")
        sys.exit(0)
    except Exception as e:
        print(f"Error checking tolerance: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: check_tolerance.py <file1.csv> <file2.csv>")
        sys.exit(1)
    check_csv(sys.argv[1], sys.argv[2])
