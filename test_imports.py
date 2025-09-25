try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    print("All packages imported successfully!")
except ImportError as e:
    print(f"Import error: {e}")