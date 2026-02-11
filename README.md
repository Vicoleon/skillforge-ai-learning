# SkillForge - AI-Powered Adaptive Learning Platform

An intelligent learning platform that generates personalized courses on any topic using AI, with adaptive assessments, smart quizzes, spaced repetition, and a contextual AI tutor.

## Features

### 🎯 Diagnostic Assessment
- AI-generated assessment questions to evaluate user knowledge
- Identifies strengths and weaknesses across subtopics
- Creates personalized learning paths based on results

### 📚 Dynamic Course Generation
- AI generates complete course curricula on any topic
- Modules include lessons, exercises, flashcards, and quizzes
- Content adapts to user's skill level

### 🧠 Smart Quizzes
- Dynamic difficulty adjustment based on performance
- Detailed explanations for every answer
- "Review this topic" recommendations when struggling

### 🔄 Spaced Repetition System (SRS)
- SM-2 algorithm for optimal review scheduling
- Reviews scheduled at increasing intervals (1, 3, 7, 14, 30 days)
- Quality ratings affect next review timing

### 🤖 AI Tutor (Contextual Coach)
- Context-aware chat that knows your current module and progress
- Three explanation styles: Simple, Example-based, Advanced
- Aware of your weaknesses and recent errors

### 🎮 Gamification
- XP system for completing activities
- Streak tracking with visual indicators
- Level progression (Novice → Apprentice → Scholar → Master)
- Achievement badges

## Tech Stack

- **Framework**: [Reflex](https://reflex.dev) (Python)
- **AI**: OpenAI GPT-4o-mini
- **Styling**: Tailwind CSS

## Getting Started

1. Clone the repository
2. Install dependencies:
   bash
   pip install -r requirements.txt
   
3. Set up environment variables:
   bash
   export OPENAI_API_KEY=your_key_here
   
4. Run the app:
   bash
   reflex run
   

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key for AI content generation |

## License

MIT
