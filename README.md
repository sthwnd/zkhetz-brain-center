# zkHetz Brain Center

Brain co-processor helps CEO to make the smartest data-driven decisions every day. Every morning it provides intelligence briefings customized for a particular market, problem, and product. Delivers analytics of the most relevant information from all over the internet to ensure both strategical decisions and next steps are aligned with the reality.

## Live Dashboard

🔗 [zkhetz-brain-center.vercel.app](https://zkhetz-brain-center.vercel.app)

## Features

- **130+ RSS Sources** - Aggregates news from government advisories, threat intel vendors, research institutions, and media
- **14 Categories** - Cyber attacks, SaaS security, geopolitics, adversary tracking, regional markets (Israel, Europe, US, South Korea, Japan), and more
- **AI-Powered Scoring** - Claude evaluates relevance and importance of each item
- **Smart Summarization** - Concise 2-sentence summaries that don't repeat headlines
- **Daily Automation** - GitHub Actions runs collection and processing every morning
- **Important Items** - Star and annotate items for follow-up

## Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  RSS Collector  │ ──▶ │   Supabase DB   │ ──▶ │  Next.js App    │
│  (Python)       │     │   (PostgreSQL)  │     │  (Vercel)       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                               
         ▼                                               
┌─────────────────┐                                      
│  LLM Processor  │                                      
│  (Claude API)   │                                      
└─────────────────┘                                      
```

## Setup

1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your keys
3. Install Python dependencies: `pip install -r requirements.txt`
4. Run collector: `python -m collectors.rss_collector`
5. Run processor: `python -m processing.llm_processor`
6. Start dashboard: `cd dashboard && npm install && npm run dev`

## Environment Variables
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## License

MIT
