import pandas as pd
from typing import List, Dict

class DegreeAgent:
    def __init__(self, degrees_df: pd.DataFrame):
        self.degrees_df = degrees_df

    def get_degrees_by_stream(self, normalised_stream: str) -> List[Dict]:
        """
        Retrieves all undergraduate degrees for the validated stream.
        """
        # Filter the dataframe
        filtered_df = self.degrees_df[self.degrees_df['stream'] == normalised_stream]
        
        # Convert to list of dictionaries for easier downstream processing
        return filtered_df.to_dict('records')
