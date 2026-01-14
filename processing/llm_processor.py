import os
import json
import re
import anthropic
from datetime import datetime
from utils.db import get_raw_items_with_freshness, get_freshness_hours, supabase

# Replace with YOUR key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Models
HAIKU_MODEL = "claude-3-5-haiku-20241022"
SONNET_MODEL = "claude-sonnet-4-5-20250929"

CATEGORIES = [
    "cyber_attacks",
    "auth_identity",
    "saas_security",
    "adversary_cyber",
    "research_updates",
    "investment",
    "legal_regulations",
    "tech_developments",
    "geopolitics",
    "target_israel",
    "target_europe",
    "target_us",
    "target_south_korea",
    "target_japan",
]

# Priority order for deduplication (lower = higher priority)
CATEGORY_PRIORITY = {
    "cyber_attacks": 1,
    "auth_identity": 2,
    "saas_security": 3,
    "adversary_cyber": 4,
    "research_updates": 5,
    "investment": 6,
    "legal_regulations": 7,
    "tech_developments": 8,
    "geopolitics": 9,
    "target_israel": 10,
    "target_europe": 11,
    "target_us": 12,
    "target_south_korea": 13,
    "target_japan": 14,
}


def clean_summary(text):
    """Remove markdown formatting and meta-commentary."""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        lower_line = line.lower()
        if 'recommendation:' in lower_line:
            continue
        if 'skip this' in lower_line:
            continue
        if 'not relevant' in lower_line:
            continue
        cleaned_lines.append(line)
    
    text = ' '.join(cleaned_lines)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def get_filter_prompt(category, items_text):
    """Get category-specific filtering prompt."""
    
    if category == "geopolitics":
        return f"""Score these news items by GLOBAL IMPORTANCE.

This is for a "Geopolitics" section showing the most important world events.

For each item, score:
- importance_score (0-100): How significant is this event globally?
  - 90-100: Major international crisis, war development, superpower actions
  - 70-89: Significant diplomatic events, major elections, sanctions
  - 50-69: Notable political developments
  - Below 50: Local news, minor events, not globally significant

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "importance_score": XX}}, ...]"""

    elif category == "cyber_attacks":
        return f"""Score these news items for CYBERSECURITY RELEVANCE.

This is for a "Cyber Attacks" section for a cybersecurity startup CEO.

For each item, score:
- relevance_score (0-100): How relevant for cybersecurity industry?
  - 90-100: Major breach, nation-state attack, critical vulnerability
  - 70-89: Significant security incident, new threat actor
  - 50-69: Notable security news
  - Below 50: Not cybersecurity related
- involves_key_theft (true/false): Involves stolen credentials, keys, tokens, auth bypass
- key_theft_type: If true, specify: "credential", "api_key", "token", "certificate", "private_key", "mfa_bypass"
- damage_brief: Very brief damage description (e.g., "500K records leaked", "$10M ransom paid", "no confirmed damage yet")

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX, "involves_key_theft": false, "key_theft_type": null, "damage_brief": "..."}}, ...]"""

    elif category == "tech_developments":
        return f"""Score these news items by how BREAKTHROUGH and UNCONVENTIONAL they are.

This is for a "Tech Developments" section showing the most outstanding technological advancements across ALL domains.

For each item, score:
- importance_score (0-100): How breakthrough and non-canonical is this?
  - 90-100: Paradigm-shifting invention, challenges existing assumptions, truly novel approach
  - 70-89: Significant advancement, unusual solution, notable innovation
  - 50-69: Solid progress but conventional approach
  - Below 50: Incremental updates, routine product releases, not innovative

Prefer: unexpected discoveries, unconventional methods, cross-domain innovations

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "importance_score": XX}}, ...]"""

    elif category == "auth_identity":
        return f"""Score these news items for AUTHORIZATION/IDENTITY RELEVANCE.

This is for an "Authorization & Identity" section for a startup building auth/identity solutions.

For each item, score:
- relevance_score (0-100): How relevant to authorization/identity industry?
  - 90-100: Industry-wide news, standards updates, major vendor announcements affecting the whole domain
  - 70-89: Significant auth/identity developments with broad implications
  - 50-69: Tangentially related (general security with identity angle)
  - Below 40: Single product features, tutorials, how-to guides, company-specific blog posts about minor features

IMPORTANT: Filter OUT blog posts about individual product features or tutorials. Only include news that affects the authorization/identity domain widely.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "saas_security":
        return f"""Score these news items for SAAS SECURITY RELEVANCE.

This is for a "SaaS Security" section covering security of SaaS applications and vendors.

For each item, score:
- relevance_score (0-100): How relevant to SaaS security?
  - 90-100: Major SaaS breach (Salesforce, Workday, ServiceNow, Slack, etc.), SaaS supply chain attack, critical SaaS vulnerability
  - 70-89: SaaS vendor security announcement, SOC2/ISO27001 certification, SaaS security product launch, OAuth/token security issues
  - 50-69: General cloud security with SaaS angle, enterprise software security
  - Below 40: Pure infrastructure (AWS/Azure/GCP), on-premise software, general IT news

IMPORTANT: Focus on SaaS APPLICATIONS (Salesforce, Workday, Microsoft 365, Google Workspace, Slack, ServiceNow, etc.) not cloud infrastructure providers.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "research_updates":
        return f"""Score these news items for RESEARCH RELEVANCE to authorization, authentication, and biometry.

This is for a "Research Updates" section focused STRICTLY on authentication, authorization, identity, and biometric research.

For each item, score:
- relevance_score (0-100): How relevant to auth/identity/biometry research?
  - 90-100: Directly about authentication, authorization, identity verification, biometrics, cryptographic identity
  - 70-89: Access control research, identity protocols, credential systems
  - 50-69: Related but not core (general crypto, tangential security)
  - Below 40: General cybersecurity research NOT about auth/identity/biometry

IMPORTANT: Only score high if the research is specifically about authentication, authorization, identity, or biometrics. General malware, network security, or other cyber research should score below 40.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "target_israel":
        return f"""Score these news items for ISRAEL CYBER/TECH MARKET RELEVANCE.

This is for an "Israel Market" section showing CYBER and TECH news relevant to Israel.

For each item, score:
- relevance_score (0-100): How relevant to Israeli CYBER/TECH market?
  - 90-100: Israeli cybersecurity companies, Israeli tech startups, Israeli government cyber policy
  - 70-89: Israeli tech investments, Israeli cyber incidents, defense tech
  - 50-69: Israeli tech ecosystem news
  - Below 50: General Israeli news NOT about cyber/tech (politics, entertainment, pharma, etc.)

IMPORTANT: Only include news about cybersecurity, technology, startups, or tech policy. Filter out general business, politics, entertainment, pharma, or non-tech news.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "target_europe":
        return f"""Score these news items for EUROPE CYBER/TECH MARKET RELEVANCE.

This is for a "Europe Market" section showing CYBER and TECH news relevant to Europe.

For each item, score:
- relevance_score (0-100): How relevant to European CYBER/TECH market?
  - 90-100: EU cyber regulations (GDPR, NIS2, Cyber Resilience Act), European cybersecurity companies
  - 70-89: European tech policy, major European cyber incidents, EU tech investments
  - 50-69: European tech ecosystem news
  - Below 50: General European news NOT about cyber/tech

IMPORTANT: Only include news about cybersecurity, technology, tech regulations, or tech policy. Filter out general politics, entertainment, or non-tech news.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "target_us":
        return f"""Score these news items for US CYBER/TECH MARKET RELEVANCE.

This is for a "US Market" section showing CYBER and TECH news relevant to United States.

For each item, score:
- relevance_score (0-100): How relevant to US CYBER/TECH market?
  - 90-100: US federal cyber policy, CISA directives, major US cybersecurity companies
  - 70-89: US tech regulations, significant US cyber incidents, US defense tech
  - 50-69: US tech ecosystem news
  - Below 50: General US news NOT about cyber/tech

IMPORTANT: Only include news about cybersecurity, technology, or tech policy. Filter out general politics, entertainment, or non-tech news.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "target_south_korea":
        return f"""Score these news items for SOUTH KOREA CYBER/TECH MARKET RELEVANCE.

This is for a "South Korea Market" section showing CYBER and TECH news relevant to South Korea.

For each item, score:
- relevance_score (0-100): How relevant to South Korean CYBER/TECH market?
  - 90-100: Korean cybersecurity companies, Korean tech giants (Samsung, LG tech divisions), Korean government cyber policy
  - 70-89: Korean tech investments, Korean cyber incidents, semiconductor/tech manufacturing
  - 50-69: Korean tech ecosystem news
  - Below 50: General Korean news NOT about cyber/tech (K-pop, politics, general business)

IMPORTANT: Only include news about cybersecurity, technology, semiconductors, or tech policy. Filter out general news, entertainment, or non-tech business.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "target_japan":
        return f"""Score these news items for JAPAN CYBER/TECH MARKET RELEVANCE.

This is for a "Japan Market" section showing CYBER and TECH news relevant to Japan.

For each item, score:
- relevance_score (0-100): How relevant to Japanese CYBER/TECH market?
  - 90-100: Japanese cybersecurity companies, Japanese tech giants, Japanese government cyber policy
  - 70-89: Japanese tech investments, Japanese cyber incidents, robotics/AI developments
  - 50-69: Japanese tech ecosystem news
  - Below 50: General Japanese news NOT about cyber/tech (politics, entertainment, general business)

IMPORTANT: Only include news about cybersecurity, technology, robotics, AI, or tech policy. Filter out general politics, entertainment, or non-tech news.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "investment":
        return f"""Score these news items for INVESTMENT DEAL relevance in Cybersecurity, DeepTech, or DefenseTech.

This is for an "Investment" section tracking ONLY actual funding rounds, M&A, and exits.

For each item, score:
- relevance_score (0-100): Is this an actual deal announcement?
  - 90-100: Specific funding round, acquisition, or IPO announcement with deal details
  - 70-89: Confirmed deal with some details missing
  - Below 40: Market reports, investor opinions, trend articles, listicles, predictions - NOT actual deals

IMPORTANT: Only include ACTUAL DEAL ANNOUNCEMENTS. Filter out articles about "top investors", "market trends", "predictions", or general reports. We want specific company + specific funding amount/acquisition.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

        return f"""Score these items for CYBER INDUSTRY THOUGHT LEADERSHIP relevance.

This is for a "Public Opinions" section showing notable statements and analysis from cybersecurity/cyber defense industry experts.

For each item, score:
- relevance_score (0-100): How notable is this opinion about cyber/security industry?
  - 90-100: Major cyber industry figure sharing significant insight about security trends, threats, or defense strategy
  - 70-89: Known security expert analyzing cyber defense topics or industry direction
  - 50-69: Relevant professional analysis on cybersecurity
  - Below 50: General news reporting (not opinion), or not about cyber/security industry

IMPORTANT: Only score high if this is OPINION/ANALYSIS from a recognized expert, specifically about cybersecurity, cyber defense, or security industry. News reporting without expert commentary should score low.

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "legal_regulations":
        return f"""Score these news items for LEGAL/REGULATORY RELEVANCE to cybersecurity, identity, and authorization.

This is for a "Legal & Regulations" section tracking laws and compliance affecting cyber/identity/auth industry.

For each item, score:
- relevance_score (0-100): How relevant as legal/regulatory news?
  - 90-100: New cyber/identity/auth laws, data protection regulations, compliance mandates
  - 70-89: Proposed legislation, regulatory guidance, enforcement actions in security/identity
  - 50-69: Legal news with cybersecurity/identity implications
  - Below 50: Not legal/regulatory or not related to cyber/identity/auth

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""

    elif category == "adversary_cyber":
        return f"""Score these news items for ADVERSARY CYBER ACTIVITY relevance.

This is for an "Adversary Cyber" section tracking cyber activities from China, Russia, Iran, and North Korea.

For each item, score:
- relevance_score (0-100): How relevant to adversary cyber tracking?
  - 90-100: Direct attribution to China/Russia/Iran/North Korea cyber operations, APT activities
  - 70-89: Suspected nation-state activity, adversary capability developments
  - 50-69: News about these nations' tech/cyber policies
  - Below 50: Not related to adversary cyber activities
- adversary: Which nation - "china", "russia", "iran", "north_korea", or null

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX, "adversary": "china"}}, ...]"""

        return f"""Score these news items for OPPORTUNITIES relevance to cybersecurity startups.

This is for an "Opportunities & Events" section showing actionable opportunities for a cyber/identity startup.

For each item, score:
- relevance_score (0-100): How actionable is this opportunity?
  - 90-100: Open RFPs, grants, accelerator applications, pitch competitions in cyber/security
  - 70-89: Upcoming conferences, networking events, partnership opportunities
  - 50-69: Industry events with potential value
  - Below 50: Not actionable or not relevant to cyber startups

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""
    
    else:
        return f"""Score these news items by relevance (0-100).

Items:
{items_text}

Respond ONLY with valid JSON array:
[{{"index": 0, "relevance_score": XX}}, ...]"""


def get_summary_prompt(category, item):
    """Get category-specific summary prompt."""
    
    if category == "geopolitics":
        return f"""Write a 2 sentence analysis of this world event. Maximum 3 lines total.

Rules:
- Sentence 1: Additional context NOT already in the title
- Sentence 2: Potential consequences - what important things might happen because of this
- No markdown formatting

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Analysis (context + consequences, max 3 lines):"""

    elif category == "cyber_attacks":
        key_theft_note = ""
        if item.get("involves_key_theft"):
            key_theft_note = f"\nThis involves stolen {item.get('key_theft_type', 'credentials')}. Mention this."
        
        damage = item.get("damage_brief", "")
        damage_note = f"\nDamage/Impact: {damage}" if damage else ""
        
        return f"""Write a 1-2 sentence summary of this cybersecurity news. Maximum 3 lines total.

Rules:
- Do NOT repeat information already in the title
- Only add NEW information: impact, damage, who was affected
- No markdown formatting
{key_theft_note}

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}
{damage_note}

Summary (new info only, max 3 lines):"""

    elif category == "tech_developments":
        return f"""Write exactly 2 sentences about this technology news. Maximum 2 lines total.

Rules:
- Do NOT repeat information already in the title
- Sentence 1: What is this and why does it matter?
- Sentence 2: Key implication or what it enables
- No markdown formatting
- Keep it brief - exactly 2 sentences

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Summary (exactly 2 sentences):"""

    elif category == "auth_identity":
        return f"""Write analysis of this authorization/identity news in two parts. Maximum 3 lines total.

Rules:
- Do NOT repeat information already in the title
- No markdown formatting

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Context: How does this compare to existing solutions, approaches, and best practices in the auth/identity space?

Analysis: What's new, who's affected, market implications?"""

    elif category == "saas_security":
        return f"""Write exactly 2 sentences about this SaaS security news. Maximum 2 lines total.

Rules:
- Do NOT repeat information already in the title
- Sentence 1: What happened (which SaaS, what security issue/announcement)
- Sentence 2: Business impact or implications for SaaS users
- No markdown formatting

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Summary (exactly 2 sentences):"""

    elif category == "research_updates":
        return f"""Write analysis of this research in two parts. Maximum 3 lines total.

Rules:
- Do NOT repeat information already in the title
- No markdown formatting

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Context: How does this compare to existing solutions, best practices, and current approaches?

Finding: What's the key finding and its practical significance?"""

    elif category in ["target_israel", "target_europe", "target_us", "target_south_korea", "target_japan"]:
        market_name = {
            "target_israel": "Israel",
            "target_europe": "Europe", 
            "target_us": "US",
            "target_south_korea": "South Korea",
            "target_japan": "Japan"
        }.get(category, "this market")
        
        return f"""Write a 1-2 sentence analysis of this {market_name} cyber/tech market news. Maximum 3 lines total.

Rules:
- Do NOT repeat information already in the title
- Focus on: market impact, relevance to local tech/cyber ecosystem
- No markdown formatting

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Analysis (market impact, max 3 lines):"""

    elif category == "investment":
        return f"""Extract key deal information in 1 sentence. Maximum 1 line.

Format: [Round type] [Amount] at [Valuation] from [Key Investors]. Founded by [Founders] - [One line company description]

Only include information that is explicitly stated. Skip fields if not mentioned.

Title: {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Deal summary (1 sentence):"""

        return f"""Summarize this cyber industry expert opinion. Maximum 3 lines total.

Rules:
- Do NOT repeat information already in the title
- Include: who said it (name + brief title/role), their key claim or insight, why it matters for cyber industry
- No markdown formatting

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Summary (who + claim + significance, max 3 lines):"""

    elif category == "legal_regulations":
        return f"""Write a 1-2 sentence analysis of this legal/regulatory news. Maximum 2 lines total.

Rules:
- Do NOT repeat information already in the title
- Focus on: potential implications for cybersecurity/identity/authorization industry
- Keep it very brief - maximum 2 lines
- No markdown formatting

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Implications:"""

    elif category == "adversary_cyber":
        adversary = item.get("adversary", "unknown")
        return f"""Write exactly 2 sentences about this {adversary} cyber activity. Maximum 2 lines total.

Rules:
- Do NOT repeat information already in the title
- Sentence 1: What happened (tactics, targets)
- Sentence 2: Why it matters (implications)
- No markdown formatting
- Keep it brief - exactly 2 sentences

Title (do not repeat this): {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Summary (exactly 2 sentences):"""

        return f"""Extract key event/opportunity details. Maximum 4 lines total.

Include:
- Date and location/format (online/in-person)
- Organizer with brief profile
- Main agenda
- Target audience

Title: {item['title']}
Source: {item['source_name']}
Content: {item['content'][:1500]}

Details:"""
    
    else:
        return f"""Write a 1 sentence summary. Do not repeat the title.

Title: {item['title']}
Content: {item['content'][:1500]}

Summary:"""


def generate_sentiment_analysis(all_items):
    """Generate overall sentiment analysis from all collected items."""
    print("Generating sentiment analysis...")
    
    west_headlines = []
    adversary_headlines = []
    
    for item in all_items[:50]:
        headline = item.get("title", "")
        source = item.get("source_name", "")
        category = item.get("category", "")
        
        if category == "adversary_cyber" or "china" in source.lower() or "russia" in source.lower():
            adversary_headlines.append(headline)
        else:
            west_headlines.append(headline)
    
    west_text = "\n".join(west_headlines[:20])
    adversary_text = "\n".join(adversary_headlines[:15]) if adversary_headlines else "No adversary-specific news collected today."
    
    prompt = f"""Based on these news headlines, generate a sentiment snapshot.

WESTERN SOURCES HEADLINES:
{west_text}

ADVERSARY-RELATED HEADLINES:
{adversary_text}

Generate exactly this format:

WEST_SENTIMENT: [One word: Optimistic / Cautiously Optimistic / Neutral / Concerned / Alarmed]
WEST_EXPLANATION: [2 sentences explaining the overall mood and key themes]

ADVERSARY_SENTIMENT: [One word: Quiet / Active / Aggressive / Escalating]
ADVERSARY_EXPLANATION: [2 sentences about key activities from China, Russia, Iran, North Korea]

Keep each explanation to 2 sentences maximum."""

    try:
        response = client.messages.create(
            model=SONNET_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        
        sentiment_data = {
            "west_sentiment": "Neutral",
            "west_explanation": "",
            "adversary_sentiment": "Active",
            "adversary_explanation": ""
        }
        
        lines = result.split("\n")
        for line in lines:
            if line.startswith("WEST_SENTIMENT:"):
                sentiment_data["west_sentiment"] = line.replace("WEST_SENTIMENT:", "").strip()
            elif line.startswith("WEST_EXPLANATION:"):
                sentiment_data["west_explanation"] = line.replace("WEST_EXPLANATION:", "").strip()
            elif line.startswith("ADVERSARY_SENTIMENT:"):
                sentiment_data["adversary_sentiment"] = line.replace("ADVERSARY_SENTIMENT:", "").strip()
            elif line.startswith("ADVERSARY_EXPLANATION:"):
                sentiment_data["adversary_explanation"] = line.replace("ADVERSARY_EXPLANATION:", "").strip()
        
        return sentiment_data
    
    except Exception as e:
        print(f"  Error generating sentiment: {e}")
        return {
            "west_sentiment": "Neutral",
            "west_explanation": "Unable to generate sentiment analysis.",
            "adversary_sentiment": "Active",
            "adversary_explanation": "Unable to generate sentiment analysis."
        }


def detect_and_translate_if_needed(text, item):
    """Detect if text is non-English and translate if needed."""
    if not text:
        return text
    
    # Simple detection: check for non-ASCII characters that suggest non-English
    non_ascii_ratio = sum(1 for c in text if ord(c) > 127) / max(len(text), 1)
    
    # If more than 30% non-ASCII, likely non-English
    if non_ascii_ratio > 0.3:
        try:
            print(f"    Translating non-English content...")
            translate_prompt = f"""Translate this text to English. Return ONLY the English translation, nothing else.

Text: {text}

English translation:"""
            
            response = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=200,
                messages=[{"role": "user", "content": translate_prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"    Translation error: {e}")
            return text
    return text


def filter_items_by_category(items):
    """Score items using category-specific criteria."""
    print(f"Filtering {len(items)} items by category...")
    
    scored_items = []
    
    # Only process items in valid categories
    valid_categories = set(CATEGORIES)
    
    by_category = {}
    skipped = 0
    for item in items:
        cat = item["category"]
        if cat not in valid_categories:
            skipped += 1
            continue
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item)
    
    if skipped > 0:
        print(f"  Skipped {skipped} items with invalid categories")
    
    for category, cat_items in by_category.items():
        num_batches = (len(cat_items) + 9) // 10  # ceiling division
        print(f"  Processing {category}: {len(cat_items)} items ({num_batches} batches)")
        
        for i in range(0, len(cat_items), 10):
            batch = cat_items[i:i+10]
            batch_num = (i // 10) + 1
            print(f"    Batch {batch_num}/{num_batches}...", end=" ", flush=True)
            
            items_text = ""
            for j, item in enumerate(batch):
                items_text += f"\n[{j}] {item['source_name']}\n"
                items_text += f"Title: {item['title']}\n"
                items_text += f"Content: {item['content'][:300]}...\n"
            
            prompt = get_filter_prompt(category, items_text)
            
            try:
                response = client.messages.create(
                    model=HAIKU_MODEL,
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                response_text = response.content[0].text.strip()
                
                # Find the FIRST complete JSON array only
                start_idx = response_text.find('[')
                if start_idx != -1:
                    # Find matching closing bracket by counting brackets
                    bracket_count = 0
                    end_idx = -1
                    for i, char in enumerate(response_text[start_idx:], start_idx):
                        if char == '[':
                            bracket_count += 1
                        elif char == ']':
                            bracket_count -= 1
                            if bracket_count == 0:
                                end_idx = i + 1
                                break
                    
                    if end_idx > start_idx:
                        json_text = response_text[start_idx:end_idx]
                        scores = json.loads(json_text)
                        print(f"OK ({len(scores)} scored)")
                    else:
                        print(f"WARN (unclosed JSON)")
                        scores = []
                else:
                    print(f"WARN (no JSON)")
                    scores = []
                
                for score_data in scores:
                    idx = score_data.get("index", -1)
                    if 0 <= idx < len(batch):
                        item = batch[idx].copy()
                        item["score"] = score_data.get("importance_score") or score_data.get("relevance_score") or 50
                        item["involves_key_theft"] = score_data.get("involves_key_theft", False)
                        item["key_theft_type"] = score_data.get("key_theft_type")
                        item["damage_brief"] = score_data.get("damage_brief")
                        item["adversary"] = score_data.get("adversary")
                        scored_items.append(item)
            
            except Exception as e:
                print(f"ERROR ({e})")
                for item in batch:
                    item["score"] = 50
                    item["involves_key_theft"] = False
                    item["key_theft_type"] = None
                    item["damage_brief"] = None
                    item["adversary"] = None
                    scored_items.append(item)
    
    print(f"  Scored {len(scored_items)} items total")
    return scored_items


def deduplicate_items(scored_items):
    """Remove duplicate items, keeping the one in highest-priority category."""
    print("Deduplicating items...")
    
    by_title = {}
    for item in scored_items:
        normalized = item["title"].lower().strip()
        normalized = re.sub(r'[^\w\s]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        if normalized not in by_title:
            by_title[normalized] = []
        by_title[normalized].append(item)
    
    unique_items = []
    duplicates_removed = 0
    
    for title, items in by_title.items():
        if len(items) == 1:
            unique_items.append(items[0])
        else:
            items.sort(key=lambda x: CATEGORY_PRIORITY.get(x["category"], 99))
            unique_items.append(items[0])
            duplicates_removed += len(items) - 1
    
    print(f"  Removed {duplicates_removed} duplicates")
    return unique_items


def select_top_items(scored_items, per_category=5):
    """
    Select top items per category, prioritizing fresh items.
    - First fill slots with fresh items (score >= 70)
    - If not enough fresh items, backfill with older items (score >= 70)
    - Always try to fill all 5 slots per category
    """
    print(f"Selecting top {per_category} items per category...")
    
    # Separate fresh and old items that pass score threshold
    fresh_items = [item for item in scored_items if item["score"] >= 70 and item.get("is_fresh", False)]
    old_items = [item for item in scored_items if item["score"] >= 70 and not item.get("is_fresh", False)]
    
    print(f"  {len(fresh_items)} fresh items, {len(old_items)} older items above threshold")
    
    # Group by category
    fresh_by_cat = {}
    old_by_cat = {}
    
    for item in fresh_items:
        cat = item["category"]
        if cat not in fresh_by_cat:
            fresh_by_cat[cat] = []
        fresh_by_cat[cat].append(item)
    
    for item in old_items:
        cat = item["category"]
        if cat not in old_by_cat:
            old_by_cat[cat] = []
        old_by_cat[cat].append(item)
    
    selected = []
    for cat in CATEGORIES:
        # Get fresh items for this category, sorted by score
        cat_fresh = fresh_by_cat.get(cat, [])
        cat_fresh.sort(key=lambda x: x["score"], reverse=True)
        
        # Get old items for this category, sorted by score
        cat_old = old_by_cat.get(cat, [])
        cat_old.sort(key=lambda x: x["score"], reverse=True)
        
        # Take fresh first, then backfill with old
        top_items = []
        top_items.extend(cat_fresh[:per_category])
        
        remaining_slots = per_category - len(top_items)
        if remaining_slots > 0:
            top_items.extend(cat_old[:remaining_slots])
        
        # Assign ranks
        for rank, item in enumerate(top_items, 1):
            item["rank"] = rank
        
        selected.extend(top_items)
        
        fresh_count = len([i for i in top_items if i.get("is_fresh", False)])
        old_count = len(top_items) - fresh_count
        print(f"  {cat}: {len(top_items)} items ({fresh_count} fresh, {old_count} old)")
    
    return selected


def summarize_items(items):
    """Summarize selected items with Sonnet using category-specific prompts."""
    print(f"Summarizing {len(items)} items with Sonnet...")
    
    for i, item in enumerate(items):
        print(f"  [{i+1}/{len(items)}] {item['title'][:50]}...")
        
        # Check if title/content needs translation first
        content_to_summarize = item['content']
        
        # Detect and translate content if non-English
        content_to_summarize = detect_and_translate_if_needed(content_to_summarize, item)
        
        # Temporarily update item content for summary prompt
        original_content = item['content']
        item['content'] = content_to_summarize
        
        prompt = get_summary_prompt(item["category"], item)
        
        # Restore original content
        item['content'] = original_content
        
        try:
            response = client.messages.create(
                model=SONNET_MODEL,
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.content[0].text.strip()
            summary = clean_summary(summary)
            
            # Translate summary if it came out non-English
            summary = detect_and_translate_if_needed(summary, item)
            
            item["summary"] = summary
        
        except Exception as e:
            print(f"    Error: {e}")
            item["summary"] = detect_and_translate_if_needed(item["title"], item)
    
    return items


def save_daily_items(items, sentiment_data):
    """Save processed items and sentiment to database."""
    print(f"Saving {len(items)} items to database...")
    
    today = datetime.now().date().isoformat()
    
    supabase.table("daily_items").delete().eq("date", today).execute()
    
    for item in items:
        supabase.table("daily_items").insert({
            "date": today,
            "category": item["category"],
            "rank": item["rank"],
            "headline": item["title"],
            "summary": item["summary"],
            "source_name": item["source_name"],
            "source_url": item["url"],
            "source_type": item["source_type"],
            "is_fresh": item.get("is_fresh", False),
            "involves_key_theft": item.get("involves_key_theft", False),
            "key_theft_type": item.get("key_theft_type"),
            "published_at": item.get("published_at")
        }).execute()
    
    supabase.table("daily_sentiment").delete().eq("date", today).execute()
    supabase.table("daily_sentiment").insert({
        "date": today,
        "west_sentiment": sentiment_data["west_sentiment"],
        "west_explanation": sentiment_data["west_explanation"],
        "adversary_sentiment": sentiment_data["adversary_sentiment"],
        "adversary_explanation": sentiment_data["adversary_explanation"]
    }).execute()
    
    print(f"  Saved to database")


def run_pipeline():
    """Run the full processing pipeline."""
    print("=" * 50)
    print("zkHetz Brain Center - Processing Pipeline")
    print("=" * 50)
    
    fresh_hours = get_freshness_hours()
    day_name = datetime.now().strftime("%A")
    print(f"Day: {day_name} | Fresh window: {fresh_hours}h")
    
    items = get_raw_items_with_freshness()
    fresh_count = len([i for i in items if i.get("is_fresh", False)])
    print(f"\nLoaded {len(items)} raw items ({fresh_count} fresh, {len(items) - fresh_count} old)")
    
    if not items:
        print("No items to process. Run RSS collector first.")
        return
    
    sentiment_data = generate_sentiment_analysis(items)
    
    scored_items = filter_items_by_category(items)
    
    unique_items = deduplicate_items(scored_items)
    
    selected_items = select_top_items(unique_items)
    
    if not selected_items:
        print("No items passed filtering.")
        return
    
    summarized_items = summarize_items(selected_items)
    
    save_daily_items(summarized_items, sentiment_data)
    
    print("\n" + "=" * 50)
    print("Pipeline complete!")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()