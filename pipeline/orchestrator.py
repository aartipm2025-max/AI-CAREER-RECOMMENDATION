from core.data_loader import load_all_datasets
from agents.input_agent import InputAgent
from agents.degree_agent import DegreeAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent
from agents.ranking_engine import RankingEngine
from agents.career_intelligence_agent import CareerIntelligenceAgent
from agents.explanation_agent import ExplanationAgent
from agents.response_agent import ResponseAgent

class CareerAdvisorOrchestrator:
    def __init__(self):
        # Load datasets once
        self.datasets = load_all_datasets()
        
        # Initialize agents
        self.input_agent = InputAgent()
        self.degree_agent = DegreeAgent(self.datasets['degrees'])
        self.market_agent = MarketIntelligenceAgent(self.datasets['salary'], self.datasets['demand'])
        self.ranking_engine = RankingEngine()
        self.career_intel_agent = CareerIntelligenceAgent(self.datasets['skills'], self.datasets['paths'])
        self.explanation_agent = ExplanationAgent()
        self.response_agent = ResponseAgent()

    def run_pipeline(self, user_stream_input: str, top_n: int = 10):
        """
        Runs the full end-to-end multi-agent pipeline with Career Intelligence.
        """
        # 1. Input Validation
        normalised_stream = self.input_agent.validate_stream(user_stream_input)
        
        # 2. Degree Retrieval
        degrees = self.degree_agent.get_degrees_by_stream(normalised_stream)
        
        # 3. Market Intelligence Enrichment
        enriched = self.market_agent.enrich_degree_data(degrees)
        
        # 4. Ranking
        ranked = self.ranking_engine.rank_degrees(enriched)
        
        # 5. Career Intelligence Layer (EXTENSION)
        with_intel = self.career_intel_agent.enrich_with_intelligence(ranked)
        
        # 6. Explanation Generation
        explained = self.explanation_agent.generate_explanations(with_intel)
        
        # 7. Response Formatting
        final_table = self.response_agent.format_output(explained)
        
        # 8. Slicing for Top N
        return final_table.head(top_n)
