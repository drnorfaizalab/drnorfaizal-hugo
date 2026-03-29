#!/bin/bash

# DR NOR FAIZAL HUGO — QUICK START SCRIPT
# Common commands for content creation, testing, and deployment

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Main menu
show_menu() {
    print_header "DR NOR FAIZAL HUGO — COMMAND MENU"
    echo ""
    echo "Content Creation:"
    echo "  1) Create new blog post"
    echo "  2) Create new specialty page"
    echo "  3) Create new patient guide"
    echo ""
    echo "Development:"
    echo "  4) Start local server (with drafts)"
    echo "  5) Build site for production"
    echo "  6) Clean build"
    echo ""
    echo "Git & Deployment:"
    echo "  7) Show git status"
    echo "  8) Commit and push changes"
    echo "  9) Show recent commits"
    echo ""
    echo "Utilities:"
    echo " 10) List all content"
    echo " 11) Check for broken links"
    echo " 12) Show site statistics"
    echo ""
    echo "  0) Exit"
    echo ""
}

# Create new blog post
create_blog_post() {
    echo ""
    read -p "Enter blog post slug (e.g., 'my-first-post'): " SLUG
    
    if [ -z "$SLUG" ]; then
        print_error "Slug cannot be empty"
        return 1
    fi
    
    # Create English version
    hugo new content "blog/$SLUG/_index.en.md"
    print_success "Created: content/blog/$SLUG/_index.en.md"
    
    # Create Bahasa Melayu version
    hugo new content "blog/$SLUG/_index.bm.md"
    print_success "Created: content/blog/$SLUG/_index.bm.md"
    
    print_info "Open the files in your editor and add content"
    print_info "Set draft: false when ready to publish"
}

# Create specialty page
create_specialty() {
    echo ""
    read -p "Enter specialty slug (e.g., 'pain-management'): " SLUG
    
    if [ -z "$SLUG" ]; then
        print_error "Slug cannot be empty"
        return 1
    fi
    
    hugo new content "expertise/$SLUG/_index.en.md"
    print_success "Created: content/expertise/$SLUG/_index.en.md"
    
    hugo new content "expertise/$SLUG/_index.bm.md"
    print_success "Created: content/expertise/$SLUG/_index.bm.md"
    
    print_info "Type set to 'specialty' - customize as needed"
}

# Create patient guide
create_guide() {
    echo ""
    read -p "Enter guide slug (e.g., 'meningioma-guide'): " SLUG
    
    if [ -z "$SLUG" ]; then
        print_error "Slug cannot be empty"
        return 1
    fi
    
    hugo new content "patients/guides/$SLUG/_index.en.md"
    print_success "Created: content/patients/guides/$SLUG/_index.en.md"
    
    hugo new content "patients/guides/$SLUG/_index.bm.md"
    print_success "Created: content/patients/guides/$SLUG/_index.bm.md"
    
    print_info "Add PDF download link in front matter"
}

# Start local server
start_server() {
    print_header "Starting Hugo Server"
    print_info "Building with drafts enabled..."
    echo ""
    hugo server --buildDrafts --disableFastRender
}

# Build production
build_production() {
    print_header "Building for Production"
    print_info "Cleaning previous build..."
    rm -rf public/
    echo ""
    
    print_info "Building minified site..."
    hugo --minify
    
    print_success "Build complete!"
    print_info "Output: $(du -sh public/ | cut -f1) in public/"
}

# Clean build
clean_build() {
    print_header "Clean Build"
    print_info "Removing caches..."
    rm -rf public/ resources/
    
    print_info "Building fresh..."
    hugo --minify
    
    print_success "Clean build complete!"
}

# Git operations
show_git_status() {
    print_header "Git Status"
    echo ""
    git status
    echo ""
    echo "Recent commits:"
    git log --oneline -10
}

commit_and_push() {
    print_header "Commit & Push Changes"
    
    echo ""
    git status
    echo ""
    
    read -p "Enter commit message: " MESSAGE
    
    if [ -z "$MESSAGE" ]; then
        print_error "Commit message cannot be empty"
        return 1
    fi
    
    echo ""
    read -p "Stage all changes? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        print_success "Changes staged"
        
        git commit -m "$MESSAGE"
        print_success "Changes committed"
        
        read -p "Push to GitHub? (y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push origin main
            print_success "Pushed to GitHub"
            print_info "Cloudflare Pages will auto-deploy in ~1-2 minutes"
        fi
    fi
}

# List content
list_content() {
    print_header "Content Inventory"
    echo ""
    
    echo "English posts:"
    find content -name "_index.en.md" | wc -l
    
    echo "Bahasa Melayu posts:"
    find content -name "_index.bm.md" | wc -l
    
    echo ""
    echo "By section:"
    find content -mindepth 2 -type d | sort | while read dir; do
        count=$(find "$dir" -name "_index.*.md" | wc -l)
        if [ $count -gt 0 ]; then
            echo "  $dir: $count files"
        fi
    done
}

# Show stats
show_stats() {
    print_header "Site Statistics"
    echo ""
    
    TOTAL_POSTS=$(find content -name "_index.*.md" | wc -l)
    TOTAL_SIZE=$(du -sh . | cut -f1)
    BUILD_SIZE=$(du -sh public/ 2>/dev/null | cut -f1 || echo "N/A (build site first)")
    
    echo "Content Files: $TOTAL_POSTS"
    echo "Project Size: $TOTAL_SIZE"
    echo "Build Size: $BUILD_SIZE"
    echo ""
    
    echo "Content breakdown:"
    echo "  Blog posts: $(find content/blog -name "_index.*.md" 2>/dev/null | wc -l)"
    echo "  Specialty pages: $(find content/expertise -name "_index.*.md" 2>/dev/null | wc -l)"
    echo "  Patient guides: $(find content/patients/guides -name "_index.*.md" 2>/dev/null | wc -l)"
}

# Main loop
while true; do
    show_menu
    read -p "Select option (0-12): " CHOICE
    
    case $CHOICE in
        1) create_blog_post ;;
        2) create_specialty ;;
        3) create_guide ;;
        4) start_server ;;
        5) build_production ;;
        6) clean_build ;;
        7) show_git_status ;;
        8) commit_and_push ;;
        9) git log --oneline -15 ;;
        10) list_content ;;
        11) print_info "Running link checker..."; hugo --printMemoryStats ;;
        12) show_stats ;;
        0) print_success "Goodbye!"; exit 0 ;;
        *) print_error "Invalid option" ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    clear
done
