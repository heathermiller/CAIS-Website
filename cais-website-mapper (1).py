#!/usr/bin/env python3
"""
CAIS Website Inventory & SEO Sitemap Generator
Scans the CAIS website directory and creates SEO-compliant sitemaps and inventory.
Author: Josh Quicksall
Date: January 2025
"""

import os
import json
import mimetypes
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re
from urllib.parse import quote
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Optional: for HTML parsing (install with: pip install beautifulsoup4)
try:
    from bs4 import BeautifulSoup
    HTML_PARSING = True
except ImportError:
    HTML_PARSING = False
    print("Note: Install beautifulsoup4 for enhanced HTML parsing: pip install beautifulsoup4")

class WebsiteMapper:
    def __init__(self, root_dir, base_url="https://caisconf.org"):
        self.root_dir = Path(root_dir)
        self.base_url = base_url.rstrip('/')
        self.inventory = {
            'html_files': [],
            'css_files': [],
            'js_files': [],
            'images': [],
            'other': [],
            'total_size': 0,
            'file_count': 0
        }
        self.sitemap_pages = []  # For XML sitemap
        self.page_metadata = {}  # Store metadata for each page
        
    def scan_directory(self):
        """Recursively scan the directory and categorize files."""
        if not self.root_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.root_dir}")
        
        print(f"Scanning directory: {self.root_dir}")
        print("-" * 60)
        
        for root, dirs, files in os.walk(self.root_dir):
            # Skip hidden directories and common excludes
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.root_dir)
                file_info = self._get_file_info(file_path, rel_path)
                
                # Categorize by file type
                ext = file_path.suffix.lower()
                if ext in ['.html', '.htm']:
                    self.inventory['html_files'].append(file_info)
                    self._process_html_for_sitemap(file_path, rel_path)
                elif ext == '.css':
                    self.inventory['css_files'].append(file_info)
                elif ext == '.js':
                    self.inventory['js_files'].append(file_info)
                elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico']:
                    self.inventory['images'].append(file_info)
                else:
                    self.inventory['other'].append(file_info)
                
                self.inventory['file_count'] += 1
                self.inventory['total_size'] += file_info['size']
    
    def _get_file_info(self, file_path, rel_path):
        """Get detailed information about a file."""
        stat = file_path.stat()
        return {
            'name': file_path.name,
            'path': str(rel_path).replace('\\', '/'),
            'size': stat.st_size,
            'size_readable': self._format_size(stat.st_size),
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified_iso': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'type': mimetypes.guess_type(str(file_path))[0] or 'unknown'
        }
    
    def _format_size(self, size):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    def _process_html_for_sitemap(self, file_path, rel_path):
        """Process HTML file for SEO sitemap generation."""
        # Create URL path
        url_path = str(rel_path).replace('\\', '/')
        
        # Special handling for index files
        if file_path.name.lower() in ['index.html', 'index.htm']:
            if len(rel_path.parts) == 1:
                # Root index
                url_path = ''
            else:
                # Directory index - use directory path
                url_path = str(Path(url_path).parent).replace('\\', '/')
        
        # Skip special index variations (like index_OnlyCFP.html)
        if 'index_' in file_path.name.lower() and file_path.name.lower() != 'index.html':
            # These are alternate versions, not main pages
            return
        
        # Determine priority based on page location and name
        priority = self._calculate_priority(file_path, rel_path)
        
        # Get last modified time
        stat = file_path.stat()
        lastmod = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
        
        # Parse HTML for metadata if available
        metadata = {'title': None, 'description': None, 'changefreq': 'monthly'}
        if HTML_PARSING:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    
                # Extract title
                title_tag = soup.find('title')
                if title_tag:
                    metadata['title'] = title_tag.text.strip()
                
                # Extract meta description
                desc_tag = soup.find('meta', attrs={'name': 'description'})
                if desc_tag:
                    metadata['description'] = desc_tag.get('content', '').strip()
                
                # Look for any "coming soon" or "TBD" content to adjust changefreq
                content = soup.get_text().lower()
                if 'coming soon' in content or 'tbd' in content or 'to be announced' in content:
                    metadata['changefreq'] = 'weekly'
                    
            except Exception as e:
                print(f"Warning: Could not parse {rel_path}: {e}")
        
        # Store page metadata
        self.page_metadata[url_path] = metadata
        
        # Add to sitemap
        self.sitemap_pages.append({
            'loc': url_path,
            'lastmod': lastmod,
            'changefreq': metadata['changefreq'],
            'priority': priority,
            'title': metadata['title'],
            'description': metadata['description']
        })
    
    def _calculate_priority(self, file_path, rel_path):
        """Calculate SEO priority for a page."""
        name = file_path.name.lower()
        path_str = str(rel_path).lower()
        
        # Homepage gets highest priority
        if name in ['index.html', 'index.htm'] and len(rel_path.parts) == 1:
            return 1.0
        
        # Key pages get high priority
        if 'cfp' in path_str or 'call-for-papers' in path_str:
            return 0.9
        if 'program' in path_str or 'schedule' in path_str:
            return 0.8
        if 'register' in path_str or 'registration' in path_str:
            return 0.8
        
        # Policy pages get medium priority
        if 'code-of-conduct' in path_str or 'accessibility' in path_str or 'diversity' in path_str:
            return 0.6
        if 'policy' in path_str or 'policies' in path_str:
            return 0.5
        
        # Directory index pages
        if name in ['index.html', 'index.htm']:
            return 0.7
        
        # Default priority for other pages
        return 0.5
    
    def generate_xml_sitemap(self):
        """Generate SEO-compliant XML sitemap."""
        # Create root element with namespace
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        urlset.set('xsi:schemaLocation', 
                   'http://www.sitemaps.org/schemas/sitemap/0.9 '
                   'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
        
        # Add each page to sitemap
        for page in sorted(self.sitemap_pages, key=lambda x: -x['priority']):
            url = ET.SubElement(urlset, 'url')
            
            # Build full URL
            if page['loc']:
                loc = ET.SubElement(url, 'loc')
                loc.text = f"{self.base_url}/{page['loc']}"
            else:
                loc = ET.SubElement(url, 'loc')
                loc.text = self.base_url
            
            # Last modified date
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = page['lastmod']
            
            # Change frequency
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = page['changefreq']
            
            # Priority
            priority = ET.SubElement(url, 'priority')
            priority.text = str(page['priority'])
        
        # Convert to string with pretty printing
        xml_str = ET.tostring(urlset, encoding='unicode')
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent='  ', encoding='UTF-8').decode('utf-8')
    
    def generate_robots_txt(self):
        """Generate robots.txt file content."""
        robots = []
        robots.append("# Robots.txt for CAIS 2026 Conference Website")
        robots.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d')}")
        robots.append("")
        robots.append("# Allow all crawlers")
        robots.append("User-agent: *")
        robots.append("Allow: /")
        robots.append("")
        robots.append("# Sitemap location")
        robots.append(f"Sitemap: {self.base_url}/sitemap.xml")
        robots.append("")
        robots.append("# Crawl delay (be nice to the server)")
        robots.append("Crawl-delay: 1")
        robots.append("")
        robots.append("# Exclude temporary or duplicate pages")
        robots.append("Disallow: /index_OnlyCFP.html")
        robots.append("Disallow: /*.pdf$")
        robots.append("")
        
        return '\n'.join(robots)
    
    def generate_html_sitemap(self):
        """Generate an SEO-friendly HTML sitemap."""
        html = []
        html.append('<!DOCTYPE html>')
        html.append('<html lang="en">')
        html.append('<head>')
        html.append('  <meta charset="UTF-8">')
        html.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html.append('  <title>Sitemap - CAIS 2026 Conference</title>')
        html.append('  <meta name="description" content="Complete sitemap for the CAIS 2026 Conference website. Find all pages, resources, and important information.">')
        html.append('  <link rel="canonical" href="' + self.base_url + '/sitemap.html">')
        html.append('  <style>')
        html.append('    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 2rem; max-width: 1200px; margin: 0 auto; line-height: 1.6; }')
        html.append('    h1 { color: #1e4aa8; border-bottom: 3px solid #29ba96; padding-bottom: 0.5rem; }')
        html.append('    h2 { color: #183d8c; margin-top: 2rem; }')
        html.append('    .sitemap-section { margin: 2rem 0; }')
        html.append('    .priority-high { font-weight: bold; font-size: 1.1em; }')
        html.append('    .priority-medium { font-weight: 500; }')
        html.append('    .priority-low { color: #666; }')
        html.append('    ul { list-style-type: none; padding-left: 0; }')
        html.append('    li { margin: 0.5rem 0; }')
        html.append('    a { color: #1e4aa8; text-decoration: none; }')
        html.append('    a:hover { text-decoration: underline; }')
        html.append('    .meta { color: #666; font-size: 0.9em; margin-left: 1rem; }')
        html.append('    .description { color: #555; font-size: 0.95em; margin-left: 1rem; margin-top: 0.2rem; }')
        html.append('  </style>')
        html.append('</head>')
        html.append('<body>')
        html.append('  <h1>CAIS 2026 Conference - Sitemap</h1>')
        html.append(f'  <p>Last updated: {datetime.now().strftime("%B %d, %Y")}</p>')
        
        # Group pages by priority
        high_priority = [p for p in self.sitemap_pages if p['priority'] >= 0.8]
        medium_priority = [p for p in self.sitemap_pages if 0.5 <= p['priority'] < 0.8]
        low_priority = [p for p in self.sitemap_pages if p['priority'] < 0.5]
        
        # High priority pages
        if high_priority:
            html.append('  <div class="sitemap-section">')
            html.append('    <h2>Primary Pages</h2>')
            html.append('    <ul>')
            for page in sorted(high_priority, key=lambda x: -x['priority']):
                url = f"/{page['loc']}" if page['loc'] else "/"
                title = page['title'] or 'Homepage' if not page['loc'] else page['loc']
                html.append(f'      <li class="priority-high">')
                html.append(f'        <a href="{url}">{title}</a>')
                if page['description']:
                    html.append(f'        <div class="description">{page["description"][:150]}...</div>')
                html.append(f'      </li>')
            html.append('    </ul>')
            html.append('  </div>')
        
        # Medium priority pages
        if medium_priority:
            html.append('  <div class="sitemap-section">')
            html.append('    <h2>Conference Information</h2>')
            html.append('    <ul>')
            for page in sorted(medium_priority, key=lambda x: -x['priority']):
                url = f"/{page['loc']}" if page['loc'] else "/"
                title = page['title'] or page['loc']
                html.append(f'      <li class="priority-medium">')
                html.append(f'        <a href="{url}">{title}</a>')
                html.append(f'      </li>')
            html.append('    </ul>')
            html.append('  </div>')
        
        # Low priority pages (if any)
        if low_priority:
            html.append('  <div class="sitemap-section">')
            html.append('    <h2>Additional Pages</h2>')
            html.append('    <ul>')
            for page in sorted(low_priority, key=lambda x: page['loc']):
                url = f"/{page['loc']}" if page['loc'] else "/"
                title = page['title'] or page['loc']
                html.append(f'      <li class="priority-low">')
                html.append(f'        <a href="{url}">{title}</a>')
                html.append(f'      </li>')
            html.append('    </ul>')
            html.append('  </div>')
        
        html.append('</body>')
        html.append('</html>')
        
        return '\n'.join(html)
    
    def generate_urllist_txt(self):
        """Generate a simple URL list text file for search engines."""
        urls = []
        for page in sorted(self.sitemap_pages, key=lambda x: -x['priority']):
            if page['loc']:
                urls.append(f"{self.base_url}/{page['loc']}")
            else:
                urls.append(self.base_url)
        return '\n'.join(urls)
    
    def generate_summary(self):
        """Generate a summary of the website inventory."""
        summary = []
        summary.append("\n" + "=" * 60)
        summary.append("CAIS WEBSITE SEO AUDIT & INVENTORY")
        summary.append("=" * 60)
        summary.append(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append(f"Base URL: {self.base_url}")
        summary.append(f"Root Directory: {self.root_dir}")
        summary.append("-" * 60)
        summary.append("FILE STATISTICS:")
        summary.append(f"  Total Files: {self.inventory['file_count']}")
        summary.append(f"  Total Size: {self._format_size(self.inventory['total_size'])}")
        summary.append(f"  HTML Pages: {len(self.inventory['html_files'])}")
        summary.append(f"  CSS Files: {len(self.inventory['css_files'])}")
        summary.append(f"  JavaScript Files: {len(self.inventory['js_files'])}")
        summary.append(f"  Images: {len(self.inventory['images'])}")
        summary.append(f"  Other Files: {len(self.inventory['other'])}")
        summary.append("-" * 60)
        summary.append("SEO SITEMAP STATISTICS:")
        summary.append(f"  Indexed Pages: {len(self.sitemap_pages)}")
        summary.append(f"  High Priority Pages (0.8+): {len([p for p in self.sitemap_pages if p['priority'] >= 0.8])}")
        summary.append(f"  Medium Priority Pages (0.5-0.8): {len([p for p in self.sitemap_pages if 0.5 <= p['priority'] < 0.8])}")
        summary.append(f"  Low Priority Pages (<0.5): {len([p for p in self.sitemap_pages if p['priority'] < 0.5])}")
        summary.append("=" * 60)
        
        return '\n'.join(summary)
    
    def save_results(self, output_dir=None):
        """Save all SEO-optimized results to files."""
        if output_dir is None:
            output_dir = self.root_dir
        
        output_dir = Path(output_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Primary SEO files (no timestamp - these should be at root level)
        
        # Save XML sitemap
        xml_file = output_dir / 'sitemap.xml'
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_xml_sitemap())
        print(f"✅ XML Sitemap saved to: {xml_file}")
        
        # Save HTML sitemap
        html_sitemap = output_dir / 'sitemap.html'
        with open(html_sitemap, 'w', encoding='utf-8') as f:
            f.write(self.generate_html_sitemap())
        print(f"✅ HTML Sitemap saved to: {html_sitemap}")
        
        # Save robots.txt
        robots_file = output_dir / 'robots.txt'
        with open(robots_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_robots_txt())
        print(f"✅ Robots.txt saved to: {robots_file}")
        
        # Save URL list
        urllist_file = output_dir / 'urllist.txt'
        with open(urllist_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_urllist_txt())
        print(f"✅ URL List saved to: {urllist_file}")
        
        # Documentation files (with timestamp for version control)
        
        # Save JSON inventory
        json_file = output_dir / f'website_inventory_{timestamp}.json'
        inventory_with_seo = {
            **self.inventory,
            'sitemap_pages': self.sitemap_pages,
            'base_url': self.base_url,
            'scan_date': datetime.now().isoformat()
        }
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(inventory_with_seo, f, indent=2, default=str)
        print(f"✅ JSON inventory saved to: {json_file}")
        
        # Save audit report
        audit_file = output_dir / f'seo_audit_{timestamp}.txt'
        with open(audit_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_summary())
            f.write("\n\n")
            f.write("PAGES IN SITEMAP:\n")
            f.write("-" * 60 + "\n")
            for page in sorted(self.sitemap_pages, key=lambda x: -x['priority']):
                url = f"{self.base_url}/{page['loc']}" if page['loc'] else self.base_url
                f.write(f"Priority {page['priority']}: {url}\n")
                if page['title']:
                    f.write(f"  Title: {page['title']}\n")
                if page['description']:
                    f.write(f"  Description: {page['description'][:100]}...\n")
                f.write(f"  Last Modified: {page['lastmod']}\n")
                f.write(f"  Change Frequency: {page['changefreq']}\n\n")
        print(f"✅ SEO Audit saved to: {audit_file}")
        
        return xml_file, html_sitemap, robots_file, urllist_file, json_file, audit_file


def main():
    # Configuration
    WEBSITE_DIR = r"C:\Users\jquicksa\Desktop\Job Search\Portfolio\CAIS-Website"
    BASE_URL = "https://caisconf.org"  # Change this to your actual domain
    
    print("🚀 CAIS Website SEO Sitemap Generator")
    print("=" * 60)
    
    # Ask user for base URL
    print(f"Default base URL: {BASE_URL}")
    custom_url = input("Enter custom base URL (press Enter to use default): ").strip()
    if custom_url:
        BASE_URL = custom_url
    
    try:
        # Create mapper instance
        mapper = WebsiteMapper(WEBSITE_DIR, BASE_URL)
        
        # Scan the directory
        mapper.scan_directory()
        
        # Print summary to console
        print(mapper.generate_summary())
        
        # Save all results
        print("\nGenerating SEO files...")
        xml_file, html_sitemap, robots_file, urllist_file, json_file, audit_file = mapper.save_results()
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! SEO sitemap and files generated.")
        print("\n📋 SEO-CRITICAL FILES (upload these to your web server):")
        print(f"  1. sitemap.xml - Submit to Google Search Console")
        print(f"  2. sitemap.html - Human-readable sitemap page")
        print(f"  3. robots.txt - Tells search engines how to crawl")
        print(f"  4. urllist.txt - Simple URL list for some tools")
        
        print("\n📊 DOCUMENTATION FILES:")
        print(f"  5. {json_file.name} - Complete inventory")
        print(f"  6. {audit_file.name} - SEO audit report")
        
        print("\n🎯 NEXT STEPS:")
        print("  1. Upload sitemap.xml to your website root")
        print("  2. Submit sitemap.xml to Google Search Console")
        print("  3. Submit sitemap.xml to Bing Webmaster Tools")
        print("  4. Upload robots.txt to your website root")
        print("  5. Link to sitemap.html from your footer")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please check that the directory path is correct.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
