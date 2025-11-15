#!/bin/bash
# Script to create GitHub issues using GitHub CLI (gh)
# This script reads the github_issues.json file and creates issues

set -e

REPO="markus41/portfolio"
JSON_FILE="github_issues.json"

if [ ! -f "$JSON_FILE" ]; then
    echo "❌ Error: $JSON_FILE not found"
    echo "Please run: python scripts/generate_feature_issues.py first"
    exit 1
fi

if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo "❌ Error: Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

echo "🚀 Creating GitHub issues for repository: $REPO"
echo ""

# Function to create an issue
create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    
    echo "Creating issue: $title"
    
    # Create the issue and capture the URL
    issue_url=$(gh issue create \
        --repo "$REPO" \
        --title "$title" \
        --body "$body" \
        --label "$labels" 2>&1)
    
    if [ $? -eq 0 ]; then
        echo "✅ Created: $issue_url"
    else
        echo "❌ Failed to create: $title"
        echo "   Error: $issue_url"
    fi
    
    # Small delay to avoid rate limiting
    sleep 1
}

# Extract and create feature requests
echo "📋 Creating Feature Requests..."
echo ""

jq -r '.feature_requests[] | @json' "$JSON_FILE" | while read -r feature; do
    title=$(echo "$feature" | jq -r '.title')
    body=$(echo "$feature" | jq -r '.body')
    labels=$(echo "$feature" | jq -r '.labels | join(",")')
    
    create_issue "$title" "$body" "$labels"
    echo ""
done

echo ""
echo "📝 Creating Sub-Issues..."
echo ""

jq -r '.sub_issues[] | @json' "$JSON_FILE" | while read -r issue; do
    title=$(echo "$issue" | jq -r '.title')
    body=$(echo "$issue" | jq -r '.body')
    labels=$(echo "$issue" | jq -r '.labels | join(",")')
    
    create_issue "$title" "$body" "$labels"
    echo ""
done

echo ""
echo "✅ All issues created successfully!"
echo ""
echo "To view all issues, run:"
echo "  gh issue list --repo $REPO"
