#!/usr/bin/env python3
"""
Migrate deprecated Hugo Blox fields to new format:
- url_code, url_pdf, url_slides, url_video -> links array
- external_link -> links array with type: site
"""

import re
import sys
from pathlib import Path


def migrate_url_fields(content):
    """Convert url_* fields to new links format"""
    
    # First, check if there's already a links: field
    has_links_field = bool(re.search(r'^links:\s*(\[\]|$)', content, re.MULTILINE))
    
    # Find the url_* section
    url_pattern = r'url_code:\s*"([^"]*)"\s*\nurl_pdf:\s*"([^"]*)"\s*\nurl_slides:\s*"([^"]*)"\s*\nurl_video:\s*"([^"]*)"'
    
    def replace_urls(match):
        code, pdf, slides, video = match.groups()
        
        links = []
        if code:
            links.append(f"  - name: Code\n    url: '{code}'")
        if pdf:
            links.append(f"  - name: PDF\n    url: '{pdf}'")
        if slides:
            links.append(f"  - name: Slides\n    url: '{slides}'")
        if video:
            links.append(f"  - name: Video\n    url: '{video}'")
        
        if not links:
            return "links: []" if not has_links_field else ""
        
        return "links:\n" + "\n".join(links)
    
    content = re.sub(url_pattern, replace_urls, content)
    
    # If there was already a links: [] field, remove it
    if has_links_field and bool(re.search(url_pattern, content)):
        content = re.sub(r'^links:\s*\[\]\s*\n', '', content, flags=re.MULTILINE)
    
    return content


def migrate_external_link(content):
    """Convert external_link to new links format"""
    
    # Check if there's already a links: field
    has_links_field = bool(re.search(r'^links:\s*(\[\]|$)', content, re.MULTILINE))
    
    pattern = r'external_link:\s*"([^"]*)"'
    
    def replace_link(match):
        url = match.group(1)
        if not url:
            return "links: []" if not has_links_field else ""
        return f"links:\n  - name: External Site\n    url: '{url}'"
    
    content = re.sub(pattern, replace_link, content)
    
    # If there was already a links: [] field, remove it
    if has_links_field and 'external_link:' not in content:
        content = re.sub(r'^links:\s*\[\]\s*\n', '', content, flags=re.MULTILINE, count=1)
    
    return content


def process_file(filepath):
    """Process a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Check if file has deprecated fields
        has_url_fields = bool(re.search(r'url_(code|pdf|slides|video):', content))
        has_external_link = bool(re.search(r'external_link:', content))
        
        if not (has_url_fields or has_external_link):
            return False
        
        # Migrate
        if has_url_fields:
            content = migrate_url_fields(content)
        
        if has_external_link:
            content = migrate_external_link(content)
        
        # Write back only if changed
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False


def main():
    content_dir = Path(__file__).parent.parent / 'content'
    
    if not content_dir.exists():
        print(f"Content directory not found: {content_dir}")
        sys.exit(1)
    
    # Find all index.md files
    files = list(content_dir.rglob('*.md'))
    
    print(f"Found {len(files)} markdown files")
    
    updated = 0
    for filepath in files:
        if process_file(filepath):
            print(f"✓ Updated: {filepath.relative_to(content_dir)}")
            updated += 1
    
    print(f"\n✓ Migration complete: {updated} files updated")


if __name__ == '__main__':
    main()
