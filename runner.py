#!/usr/bin/env python3
"""
AI Coding Digest - Main Runner Script

This script orchestrates the entire daily digest generation process:
1. Fetch data from arXiv and GitHub
2. Clean and deduplicate data
3. Generate summaries using LLM
4. Create reports in multiple formats
5. Send email digest

Usage:
    python runner.py [--config config.json] [--date YYYY-MM-DD] [--dry-run]
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from collector.arxiv_fetcher import ArxivFetcher
from collector.github_fetcher import GitHubFetcher
from collector.cleaner import DataCleaner
from summarizer.gpt_summarizer import GPTSummarizer
from summarizer.report_generator import ReportGenerator
from senders.email_sender import EmailSender


class AICodeDigestRunner:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.setup_logging()
        
        # Initialize components with config
        self.arxiv_fetcher = ArxivFetcher(config=self.config)
        self.github_fetcher = GitHubFetcher(
            config=self.config,
            token=os.getenv('GITHUB_TOKEN')
        )
        self.data_cleaner = DataCleaner()
        self.summarizer = GPTSummarizer(config=self.config)
        self.report_generator = ReportGenerator(
            output_dir=self.config["output"]["output_dir"],
            config=self.config
        )
        self.email_sender = EmailSender()
        
        self.logger = logging.getLogger(__name__)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if not self.config_path.exists():
            self.logger.error(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def setup_logging(self):
        """Setup logging configuration."""
        log_config = self.config.get("logging", {})
        log_level = getattr(logging, log_config.get("level", "INFO"))
        
        # Create logs directory if specified
        log_file = log_config.get("file")
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(log_file) if log_file else logging.NullHandler()
            ]
        )
    
    def run_daily_digest(self, target_date: str = None, dry_run: bool = False) -> bool:
        """
        Run the complete daily digest process.
        
        Args:
            target_date: Target date in YYYY-MM-DD format (defaults to today)
            dry_run: If True, don't send emails
            
        Returns:
            bool: True if successful, False otherwise
        """
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")
        
        self.logger.info(f"Starting AI Code Digest generation for {target_date}")
        
        try:
            # Step 1: Fetch data
            self.logger.info("Step 1: Fetching data from sources...")
            raw_data = self.fetch_all_data()
            self.logger.info(f"Fetched {len(raw_data)} raw items")
            
            if not raw_data:
                self.logger.warning("No data fetched. Stopping process.")
                return False
            
            # Step 2: Clean and deduplicate
            self.logger.info("Step 2: Cleaning and deduplicating data...")
            cleaned_data = self.data_cleaner.clean_and_deduplicate(raw_data)
            self.logger.info(f"Cleaned data: {len(cleaned_data)} items")
            
            # Step 3: Generate summaries
            self.logger.info("Step 3: Generating LLM summaries...")
            summaries = self.summarizer.summarize_items(cleaned_data)
            self.logger.info(f"Generated {len(summaries)} summaries")
            
            # Step 4: Generate reports
            self.logger.info("Step 4: Generating reports...")
            report_files = self.report_generator.generate_reports(summaries, target_date)
            self.logger.info(f"Generated reports: {list(report_files.keys())}")
            
            # Step 5: Send email (if not dry run)
            if not dry_run and self.config["email"]["enabled"]:
                self.logger.info("Step 5: Sending email digest...")
                success = self.send_email_digest(report_files, target_date, summaries)
                if success:
                    self.logger.info("Email digest sent successfully")
                else:
                    self.logger.error("Failed to send email digest")
                    return False
            elif dry_run:
                self.logger.info("Step 5: Skipping email (dry run mode)")
            else:
                self.logger.info("Step 5: Email disabled in configuration")
            
            self.logger.info("AI Code Digest generation completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during digest generation: {e}", exc_info=True)
            return False
    
    def fetch_all_data(self) -> List[Dict[str, Any]]:
        """Fetch data from all enabled sources."""
        all_data = []
        
        # Fetch from arXiv
        if self.config["data_collection"]["arxiv"]["enabled"]:
            try:
                arxiv_config = self.config["data_collection"]["arxiv"]
                papers = self.arxiv_fetcher.fetch_papers(
                    max_results=arxiv_config["max_results"],
                    days_back=arxiv_config["days_back"]
                )
                all_data.extend(papers)
                self.logger.info(f"Fetched {len(papers)} papers from arXiv")
            except Exception as e:
                self.logger.error(f"Error fetching from arXiv: {e}")
        
        # Fetch from GitHub
        if self.config["data_collection"]["github"]["enabled"]:
            try:
                github_config = self.config["data_collection"]["github"]
                repos = self.github_fetcher.fetch_repositories(
                    max_per_query=github_config["max_per_query"],
                    days_back=github_config["days_back"]
                )
                all_data.extend(repos)
                self.logger.info(f"Fetched {len(repos)} repositories from GitHub")
            except Exception as e:
                self.logger.error(f"Error fetching from GitHub: {e}")
        
        return all_data
    
    def send_email_digest(self, 
                         report_files: Dict[str, str], 
                         date_str: str, 
                         summaries: List[Dict[str, Any]]) -> bool:
        """Send email digest with reports."""
        email_config = self.config["email"]
        
        # Prepare summary statistics
        summary_stats = {
            "total_items": len(summaries),
            "sources": self.report_generator._get_source_counts(summaries),
            "categories": self.report_generator._get_category_counts(summaries)
        }
        
        # Filter attachments if needed
        attachments = report_files.copy()
        if not email_config.get("send_attachments", True):
            # Only keep HTML for email body
            attachments = {k: v for k, v in attachments.items() if k == "html"}
        
        # Get recipient from environment variable
        recipient = os.getenv(email_config["recipient_env"])
        if not recipient:
            self.logger.error(f"Email recipient not found in environment variable: {email_config['recipient_env']}")
            return False
        
        return self.email_sender.send_daily_digest(
            to_email=recipient,
            report_files=attachments,
            date_str=date_str,
            summary_stats=summary_stats
        )


def main():
    parser = argparse.ArgumentParser(description="AI Coding Digest Generator")
    parser.add_argument("--config", default="config.json", help="Configuration file path")
    parser.add_argument("--date", help="Target date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Don't send emails")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Override logging level if verbose
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        runner = AICodeDigestRunner(args.config)
        success = runner.run_daily_digest(args.date, args.dry_run)
        
        if success:
            print("✅ AI Code Digest generation completed successfully")
            sys.exit(0)
        else:
            print("❌ AI Code Digest generation failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()