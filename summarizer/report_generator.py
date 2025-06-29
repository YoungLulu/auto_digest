import json
import html
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import subprocess


class ReportGenerator:
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_reports(self, summaries: List[Dict[str, Any]], date_str: str = None) -> Dict[str, str]:
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        file_paths = {}
        
        # Generate JSON report
        json_path = self.output_dir / f"daily_{date_str}.json"
        self._generate_json_report(summaries, json_path)
        file_paths["json"] = str(json_path)
        
        # Generate Markdown report
        md_path = self.output_dir / f"daily_{date_str}.md"
        self._generate_markdown_report(summaries, md_path, date_str)
        file_paths["markdown"] = str(md_path)
        
        # Generate HTML report
        html_path = self.output_dir / f"daily_{date_str}.html"
        self._generate_html_report(summaries, html_path, date_str)
        file_paths["html"] = str(html_path)
        
        # Try to generate PDF (requires pandoc or weasyprint)
        try:
            pdf_path = self.output_dir / f"daily_{date_str}.pdf"
            self._generate_pdf_report(md_path, pdf_path)
            file_paths["pdf"] = str(pdf_path)
        except Exception as e:
            print(f"PDF generation failed: {e}")
        
        return file_paths
    
    def _generate_json_report(self, summaries: List[Dict[str, Any]], output_path: Path):
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "total_items": len(summaries),
            "sources": self._get_source_counts(summaries),
            "categories": self._get_category_counts(summaries),
            "summaries": summaries
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    def _generate_markdown_report(self, summaries: List[Dict[str, Any]], output_path: Path, date_str: str):
        md_content = self._build_markdown_content(summaries, date_str)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    def _build_markdown_content(self, summaries: List[Dict[str, Any]], date_str: str) -> str:
        # Group by source first, then by category
        sources = {"arxiv": [], "github": []}
        for summary in summaries:
            source = summary.get("source", "unknown")
            if source in sources:
                sources[source].append(summary)
        
        md_lines = [
            f"# 🧠 AI Coding Digest - {date_str}",
            "",
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"**Total Items**: {len(summaries)}",
            f"**Sources**: {self._format_source_counts(summaries)}",
            "",
            "---",
            ""
        ]
        
        # Add table of contents
        md_lines.extend([
            "## 📋 Table of Contents",
            ""
        ])
        
        for source_name, items in sources.items():
            if items:
                source_display = "📄 arXiv Papers" if source_name == "arxiv" else "💻 GitHub Repositories"
                md_lines.append(f"- [{source_display}](#{source_name}-section) ({len(items)} items)")
                
                # Add categories within each source
                categories = {}
                for item in items:
                    tags = item.get("category_tags", ["other"])
                    main_tag = tags[0] if tags else "other"
                    if main_tag not in categories:
                        categories[main_tag] = []
                    categories[main_tag].append(item)
                
                for category in sorted(categories.keys()):
                    category_name = self._format_category_name(category)
                    md_lines.append(f"  - [{category_name}](#{source_name}-{category.replace('_', '-')}) ({len(categories[category])} items)")
        
        md_lines.extend(["", "---", ""])
        
        # Add content by source
        for source_name, items in sources.items():
            if not items:
                continue
                
            source_display = "📄 arXiv Papers" if source_name == "arxiv" else "💻 GitHub Repositories"
            md_lines.extend([
                f"## {source_display}",
                "",
                f"*{len(items)} items from {source_name}*",
                "",
            ])
            
            # Group by category within each source
            categories = {}
            for item in items:
                tags = item.get("category_tags", ["other"])
                main_tag = tags[0] if tags else "other"
                if main_tag not in categories:
                    categories[main_tag] = []
                categories[main_tag].append(item)
            
            # Sort categories by relevance
            for category in sorted(categories.keys()):
                category_items = categories[category]
                category_name = self._format_category_name(category)
                
                md_lines.extend([
                    f"### {category_name}",
                    "",
                    f"*{len(category_items)} items*",
                    ""
                ])
                
                # Sort items by comprehensive score (highest first)
                for item in sorted(category_items, key=lambda x: x.get("final_score", x.get("relevance_score", 0)), reverse=True):
                    md_lines.extend(self._format_item_markdown(item))
                
                md_lines.extend([""])
            
            md_lines.extend(["---", ""])
        
        return "\n".join(md_lines)
    
    def _format_item_markdown(self, item: Dict[str, Any]) -> List[str]:
        lines = [
            f"### {item.get('title', 'No title')}",
            "",
            f"**🔗 Link**: [{item.get('url', 'N/A')}]({item.get('url', '#')})",
            ""
        ]
        
        # Add authors field
        authors = item.get('authors', [])
        if authors:
            if isinstance(authors, list):
                authors_str = ", ".join(authors[:5])  # Show up to 5 authors
                if len(authors) > 5:
                    authors_str += f" (+{len(authors)-5} more)"
            else:
                authors_str = str(authors)
            lines.extend([f"**👥 Authors**: {authors_str}", ""])
        
        # Add comprehensive scoring
        final_score = item.get('final_score')
        if final_score is not None:
            lines.append(f"**🏆 Overall Score**: {final_score}/10")
            
            # Add score breakdown if available
            comprehensive_scores = item.get('comprehensive_scores', {})
            if 'individual_scores' in comprehensive_scores:
                scores = comprehensive_scores['individual_scores']
                lines.append(f"  - Popularity: {scores.get('popularity', 'N/A')}/10, Technical Innovation: {scores.get('technical_innovation', 'N/A')}/10")
                lines.append(f"  - Application Value: {scores.get('application_value', 'N/A')}/10, Readability: {scores.get('readability', 'N/A')}/10")
                lines.append(f"  - Experimental Thoroughness: {scores.get('experimental_thoroughness', 'N/A')}/10, Author Influence: {scores.get('author_influence', 'N/A')}/10")
        else:
            lines.append(f"**📊 Relevance Score**: {item.get('relevance_score', 'N/A')}/10")
        
        lines.extend([
            f"**🎯 Target Audience**: {item.get('target_audience', 'N/A')}",
            "",
            f"**📝 Summary**: {item.get('summary', 'No summary available')}",
            "",
            f"**🔍 Background**: {item.get('background', 'Not specified')}",
            ""
        ])
        
        # Technical highlights
        highlights = item.get('technical_highlights', [])
        if highlights:
            lines.append("**⚡ Technical Highlights**:")
            for highlight in highlights:
                lines.append(f"- {highlight}")
            lines.append("")
        
        # Applications
        applications = item.get('potential_applications', [])
        if applications:
            lines.append("**🚀 Potential Applications**:")
            for app in applications:
                lines.append(f"- {app}")
            lines.append("")
        
        # Tags
        tags = item.get('category_tags', [])
        if tags:
            tag_str = " ".join([f"`{tag}`" for tag in tags])
            lines.append(f"**🏷️ Tags**: {tag_str}")
            lines.append("")
        
        lines.append("")
        return lines
    
    def _generate_html_report(self, summaries: List[Dict[str, Any]], output_path: Path, date_str: str):
        html_content = self._build_html_content(summaries, date_str)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _build_html_content(self, summaries: List[Dict[str, Any]], date_str: str) -> str:
        # Build proper HTML content directly
        
        # Group by source first, then by category
        sources = {"arxiv": [], "github": []}
        for summary in summaries:
            source = summary.get("source", "unknown")
            if source in sources:
                sources[source].append(summary)
        
        # Build HTML content
        content_html = f"""
        <h1>🧠 AI Coding Digest - {date_str}</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Total Items</strong>: {len(summaries)}</p>
        <p><strong>Sources</strong>: {self._format_source_counts(summaries)}</p>
        <hr>
        """
        
        # Add table of contents
        content_html += "<h2>📋 Table of Contents</h2><ul>"
        for source_name, items in sources.items():
            if items:
                source_display = "📄 arXiv Papers" if source_name == "arxiv" else "💻 GitHub Repositories"
                content_html += f'<li><a href="#{source_name}-section">{source_display}</a> ({len(items)} items)<ul>'
                
                # Add categories within each source
                categories = {}
                for item in items:
                    tags = item.get("category_tags", ["other"])
                    main_tag = tags[0] if tags else "other"
                    if main_tag not in categories:
                        categories[main_tag] = []
                    categories[main_tag].append(item)
                
                for category in sorted(categories.keys()):
                    category_name = self._format_category_name(category)
                    content_html += f'<li><a href="#{source_name}-{category}">{category_name}</a> ({len(categories[category])} items)</li>'
                
                content_html += "</ul></li>"
        content_html += "</ul><hr>"
        
        # Add content by source
        for source_name, items in sources.items():
            if not items:
                continue
                
            source_display = "📄 arXiv Papers" if source_name == "arxiv" else "💻 GitHub Repositories"
            content_html += f'<h2 id="{source_name}-section">{source_display}</h2>'
            content_html += f'<p><em>{len(items)} items from {source_name}</em></p>'
            
            # Group by category within each source
            categories = {}
            for item in items:
                tags = item.get("category_tags", ["other"])
                main_tag = tags[0] if tags else "other"
                if main_tag not in categories:
                    categories[main_tag] = []
                categories[main_tag].append(item)
            
            # Add content by category
            for category in sorted(categories.keys()):
                category_items = categories[category]
                category_name = self._format_category_name(category)
                
                content_html += f'<h3 id="{source_name}-{category}">{category_name}</h3>'
                content_html += f'<p><em>{len(category_items)} items</em></p>'
                
                # Sort items by comprehensive score (highest first)
                for item in sorted(category_items, key=lambda x: x.get("final_score", x.get("relevance_score", 0)), reverse=True):
                    content_html += self._format_item_html(item)
            
            content_html += "<hr>"
        
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Coding Digest - {date_str}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        h1 {{ border-bottom: 2px solid #007acc; }}
        h2 {{ border-bottom: 1px solid #ddd; }}
        .item {{ margin-bottom: 30px; padding: 20px; border: 1px solid #eee; border-radius: 8px; background: #fafafa; }}
        .tags {{ margin-top: 10px; }}
        .tag {{ background: #007acc; color: white; padding: 2px 6px; border-radius: 3px; font-size: 12px; margin-right: 5px; }}
        a {{ color: #007acc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 5px; }}
        hr {{ margin: 30px 0; border: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div id="content">
        {content_html}
    </div>
</body>
</html>"""
        
        return full_html
    
    def _format_item_html(self, item: Dict[str, Any]) -> str:
        """Format a single item as HTML."""
        item_html = f"""
        <div class="item">
            <h3>{html.escape(item.get('title', 'No title'))}</h3>
            <p><strong>🔗 Link</strong>: <a href="{item.get('url', '#')}" target="_blank">{item.get('url', 'N/A')}</a></p>
        """
        
        # Add authors field
        authors = item.get('authors', [])
        if authors:
            if isinstance(authors, list):
                authors_str = ", ".join(authors[:5])  # Show up to 5 authors
                if len(authors) > 5:
                    authors_str += f" (+{len(authors)-5} more)"
            else:
                authors_str = str(authors)
            item_html += f"<p><strong>👥 Authors</strong>: {html.escape(authors_str)}</p>"
        
        # Add comprehensive scoring
        final_score = item.get('final_score')
        if final_score is not None:
            item_html += f"<p><strong>🏆 Overall Score</strong>: {final_score}/10</p>"
            
            # Add score breakdown if available
            comprehensive_scores = item.get('comprehensive_scores', {})
            if 'individual_scores' in comprehensive_scores:
                scores = comprehensive_scores['individual_scores']
                item_html += f"<p><small>Popularity: {scores.get('popularity', 'N/A')}/10, Technical Innovation: {scores.get('technical_innovation', 'N/A')}/10, Application Value: {scores.get('application_value', 'N/A')}/10<br>"
                item_html += f"Readability: {scores.get('readability', 'N/A')}/10, Experimental Thoroughness: {scores.get('experimental_thoroughness', 'N/A')}/10, Author Influence: {scores.get('author_influence', 'N/A')}/10</small></p>"
        else:
            item_html += f"<p><strong>📊 Relevance Score</strong>: {item.get('relevance_score', 'N/A')}/10</p>"
        
        item_html += f"""
            <p><strong>🎯 Target Audience</strong>: {html.escape(self._format_target_audience(item.get('target_audience', 'N/A')))}</p>
            
            <p><strong>📝 Summary</strong>: {html.escape(item.get('summary', 'No summary available'))}</p>
            
            <p><strong>🔍 Background</strong>: {html.escape(item.get('background', 'Not specified'))}</p>
        """
        
        # Technical highlights
        highlights = item.get('technical_highlights', [])
        if highlights:
            item_html += "<p><strong>⚡ Technical Highlights</strong>:</p><ul>"
            for highlight in highlights:
                item_html += f"<li>{html.escape(str(highlight))}</li>"
            item_html += "</ul>"
        
        # Applications
        applications = item.get('potential_applications', [])
        if applications:
            item_html += "<p><strong>🚀 Potential Applications</strong>:</p><ul>"
            for app in applications:
                item_html += f"<li>{html.escape(str(app))}</li>"
            item_html += "</ul>"
        
        # Tags
        tags = item.get('category_tags', [])
        if tags:
            item_html += '<p><strong>🏷️ Tags</strong>: '
            for tag in tags:
                item_html += f'<span class="tag">{html.escape(str(tag))}</span>'
            item_html += '</p>'
        
        item_html += "</div>"
        return item_html
    
    def _generate_pdf_report(self, md_path: Path, pdf_path: Path):
        # Try pandoc first
        try:
            subprocess.run([
                'pandoc', str(md_path), '-o', str(pdf_path),
                '--pdf-engine=xelatex'
            ], check=True, capture_output=True)
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Try weasyprint as fallback
        try:
            from weasyprint import HTML, CSS
            html_path = md_path.with_suffix('.html')
            if html_path.exists():
                HTML(filename=str(html_path)).write_pdf(str(pdf_path))
                return
        except ImportError:
            pass
        
        raise Exception("PDF generation requires pandoc or weasyprint")
    
    def _get_source_counts(self, summaries: List[Dict[str, Any]]) -> Dict[str, int]:
        counts = {}
        for summary in summaries:
            source = summary.get("source", "unknown")
            counts[source] = counts.get(source, 0) + 1
        return counts
    
    def _get_category_counts(self, summaries: List[Dict[str, Any]]) -> Dict[str, int]:
        counts = {}
        for summary in summaries:
            tags = summary.get("category_tags", ["other"])
            for tag in tags:
                counts[tag] = counts.get(tag, 0) + 1
        return counts
    
    def _format_source_counts(self, summaries: List[Dict[str, Any]]) -> str:
        counts = self._get_source_counts(summaries)
        return ", ".join([f"{source}: {count}" for source, count in counts.items()])
    
    def _format_category_name(self, category: str) -> str:
        return category.replace('_', ' ').title()
    
    def _format_target_audience(self, target_audience) -> str:
        """Format target audience (handle both string and list)."""
        if isinstance(target_audience, list):
            return ", ".join(target_audience)
        elif isinstance(target_audience, str):
            return target_audience
        else:
            return "N/A"


if __name__ == "__main__":
    # Test the report generator
    generator = ReportGenerator()
    
    test_summaries = [
        {
            "title": "Test Paper on Code Generation",
            "url": "https://example.com",
            "background": "Testing report generation",
            "technical_highlights": ["Feature 1", "Feature 2"],
            "potential_applications": ["App 1", "App 2"],
            "target_audience": "Researchers",
            "category_tags": ["code_generation"],
            "relevance_score": 8,
            "summary": "This is a test summary",
            "source": "arxiv"
        }
    ]
    
    file_paths = generator.generate_reports(test_summaries)
    print("Generated reports:", file_paths)