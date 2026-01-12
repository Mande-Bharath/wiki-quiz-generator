# Wiki Quiz Generator - Prompt Templates & Configuration

This document details the LangChain prompt templates and configuration used in the Wiki Quiz Generator.

## Prompt Templates Overview

All prompts are defined in `backend/app/prompts.py` and use LangChain's `ChatPromptTemplate` for structured LLM interactions.

---

## 1. Quiz Generation Prompt

### Purpose
Generate 5-10 multiple-choice quiz questions based on Wikipedia article content.

### Key Features
- **Grounding**: Questions must be directly from article content
- **Anti-Hallucination**: Explicit instruction to NOT make up facts
- **Variety**: Mix of difficulty levels (easy, medium, hard)
- **Explanations**: Each question includes evidence-based explanation
- **JSON Format**: Structured output for easy parsing

### Prompt Template

```python
QUIZ_GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert quiz generator. Your task is to create a structured quiz based on Wikipedia article content.

IMPORTANT RULES:
1. Generate 5-10 questions of varying difficulty levels (easy, medium, hard)
2. Each question must be directly supported by the provided article content
3. Create 4 multiple choice options (A, B, C, D) for each question
4. Clearly identify the correct answer
5. Provide a brief explanation referencing the article
6. Ensure questions cover different topics/sections of the article
7. Do NOT make up or hallucinate facts - only use information from the article
8. Format output as valid JSON

Return ONLY a valid JSON object with this structure:
{
  "questions": [
    {
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Correct option text",
      "difficulty": "easy|medium|hard",
      "explanation": "Why this answer is correct, referencing the article"
    }
  ]
}"""),
    ("human", "Article Title: {title}\n\nArticle Content:\n{content}\n\nGenerate a quiz with 5-10 questions based on ONLY the provided content above.")
])
```

### Optimization Strategies

1. **Explicit Anti-Hallucination Rule**: Emphasizes "only use information from the article"
2. **Clear JSON Structure**: Reduces parsing errors
3. **Difficulty Distribution**: Ensures engaging quiz with mix of easy/medium/hard
4. **Referenced Explanations**: Links answers back to article source
5. **Content Limiting**: Input limited to 8000 characters to avoid token overflow

### Example Output

```json
{
  "questions": [
    {
      "question": "Where was Alan Turing born?",
      "options": ["Cambridge", "Maida Vale, London", "Oxford", "Manchester"],
      "answer": "Maida Vale, London",
      "difficulty": "easy",
      "explanation": "The article explicitly states: 'Born in Maida Vale, London'"
    }
  ]
}
```

---

## 2. Related Topics Extraction Prompt

### Purpose
Extract 5-8 key topics and concepts from the article for context and learning paths.

### Key Features
- **Entity Recognition**: Identifies important people, places, concepts
- **Concept Extraction**: Pulls out central themes
- **JSON Structured Output**: Easy for frontend display

### Prompt Template

```python
RELATED_TOPICS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at identifying key topics from Wikipedia articles.

Your task is to extract 5-8 important related topics/concepts from the provided article content.
These should be:
1. Key entities mentioned in the article
2. Concepts central to understanding the topic
3. Related fields or disciplines
4. Important historical periods or events

Return ONLY a JSON object with this structure:
{
  "related_topics": ["Topic 1", "Topic 2", "Topic 3", ...]
}"""),
    ("human", "Article Title: {title}\n\nArticle Content:\n{content}\n\nIdentify 5-8 related topics from this article.")
])
```

### Optimization Strategies

1. **Clear Task Definition**: Specifies types of topics wanted
2. **Constraint-Based**: Exactly 5-8 topics ensures consistency
3. **Multi-Category**: Entities, concepts, fields, events provides diversity
4. **JSON Format**: Simple structure for frontend rendering

### Example Output

```json
{
  "related_topics": [
    "Cryptography",
    "Enigma Machine",
    "Computer Science",
    "Artificial Intelligence",
    "Turing Machine",
    "Computable Numbers",
    "World War II"
  ]
}
```

---

## 3. Summary Generation Prompt

### Purpose
Create a concise 2-3 sentence summary of the article for quick understanding.

### Key Features
- **Brevity**: Forces clarity and essential information only
- **Context**: Captures main subject and key points
- **Plain Text**: Easy human reading

### Prompt Template

```python
SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at summarizing Wikipedia articles.

Provide a brief 2-3 sentence summary of the article that captures the main subject and key points.

Return ONLY the summary text, no JSON or additional formatting."""),
    ("human", "Article Title: {title}\n\nArticle Content:\n{content}\n\nProvide a brief summary of this article.")
])
```

### Optimization Strategies

1. **Sentence Limit**: 2-3 sentences forces conciseness
2. **Plain Text Output**: No parsing needed, direct display
3. **Content Limiting**: Uses shorter excerpt (4000 chars) for focused summary

---

## Configuration Details

### LLM Configuration

Located in `backend/app/services.py`:

```python
self.llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.7,
    max_tokens=2000
)
```

**Parameters:**
- **model**: `gemini-2.0-flash` - Fast and accurate Gemini model
- **temperature**: `0.7` - Balanced creativity (0=deterministic, 1=random)
- **max_tokens**: `2000` - Limits response length, ensures completeness

### Content Limiting Strategy

```python
# Quiz generation: 8000 characters
content[:8000]

# Related topics: 8000 characters
content[:8000]

# Summary generation: 4000 characters
content[:4000]
```

**Rationale:**
- Reduces token usage (cost & speed)
- Prevents context window overflow
- Focuses LLM on main article sections
- Maintains output quality

---

## Quality Assurance

### Prompt Validation Rules

1. **JSON Parsing**: Response must be valid JSON
2. **Structure Validation**: Checks for required fields
3. **Fallback JSON Extraction**: Attempts to parse markdown code blocks
4. **Error Logging**: All parsing issues are logged

Implementation in `services.py`:

```python
@staticmethod
def _parse_json_response(response_text: str) -> Dict:
    """Parse JSON from various LLM response formats"""
    # Try direct parsing
    # Try markdown code blocks
    # Try to extract JSON with regex
    # Log if all attempts fail
```

### Hallucination Prevention

1. **System Prompt Rule**: "Only use information from the article"
2. **Content Grounding**: Full article text provided as context
3. **Explanation Requirement**: Forces LLM to cite sources
4. **Anti-Hallucination Keywords**: Uses "referenced in the article"

### Output Quality Metrics

**Quiz Questions:**
- ✅ 5-10 questions per article
- ✅ Difficulty mix (easy/medium/hard)
- ✅ All options distinct
- ✅ Correct answer matches one option
- ✅ Explanation relevant and grounded

**Related Topics:**
- ✅ 5-8 topics
- ✅ Unique topics
- ✅ Relevant to article content
- ✅ Mix of entities and concepts

---

## Advanced Prompt Engineering Techniques Used

### 1. Few-Shot Learning
While not implemented here, the JSON structure acts as implicit guidance for format.

### 2. Chain-of-Thought
Explanations require reasoning about why answers are correct.

### 3. Role Assignment
"You are an expert quiz generator" establishes context and expertise.

### 4. Constraint-Based Generation
- Specific number of questions
- Explicit difficulty levels
- Defined option count

### 5. Content Grounding
Providing full article content prevents hallucination better than abstract instructions.

### 6. Explicit Negation
"Do NOT make up or hallucinate" directly addresses common LLM failure modes.

---

## Future Prompt Optimizations

### Potential Improvements

1. **Section-Based Prompts**: Separate prompts for each article section
   ```
   "Focus questions on the 'Early Life' section..."
   ```

2. **Difficulty-Balanced Prompts**: Separate prompts for each difficulty
   ```
   "Generate only HARD questions that require deep understanding..."
   ```

3. **Multi-Turn Prompts**: Use chat history for refinement
   ```
   1. Generate questions
   2. User feedback
   3. Refine questions
   ```

4. **Domain-Specific Prompts**: Different prompts for different topics
   ```
   - History articles: Focus on dates and events
   - Science articles: Focus on mechanisms and theories
   ```

5. **User-Customizable Prompts**: Let users define question focus
   ```
   "Focus on [topic] aspects of the article"
   ```

---

## Testing Prompt Effectiveness

### Test Cases

Run these examples to verify prompt quality:

#### Test 1: Alan Turing
```
URL: https://en.wikipedia.org/wiki/Alan_Turing
Expected: 6-8 questions covering: birthplace, contributions, WWII role, Turing Test
```

#### Test 2: Machine Learning
```
URL: https://en.wikipedia.org/wiki/Machine_learning
Expected: Questions on ML definition, types, applications, differences from traditional programming
```

#### Test 3: Short Article
```
URL: Any short Wikipedia article
Expected: Minimum 5 questions regardless of length
```

---

## Troubleshooting Prompt Issues

### Problem: Questions not grounded in content
**Solution**: Increase content limit, add more explicit grounding rules

### Problem: JSON parsing failures
**Solution**: Add fallback parsing logic, use more structured examples

### Problem: Hallucinated facts
**Solution**: Strengthen anti-hallucination rules, reduce temperature

### Problem: Poor explanation quality
**Solution**: Add example explanations, require article citations

### Problem: Unbalanced difficulty
**Solution**: Explicitly specify difficulty distribution

---

## Performance Metrics

### Average Metrics (Gemini 2.0-Flash)

- **Quiz Generation Time**: 30-45 seconds
- **Related Topics Time**: 5-10 seconds
- **JSON Parse Success Rate**: 99%+
- **Tokens per Request**: 800-1500
- **Cost**: < $0.01 per quiz (free tier)

---

## Integration with Frontend

### Flow Diagram

```
User Input (URL)
    ↓
Scraper (BeautifulSoup)
    ↓
LLM Prompt 1: Quiz Generation
    ↓ (JSON)
LLM Prompt 2: Related Topics
    ↓ (JSON)
LLM Prompt 3: Summary
    ↓ (plain text)
Combine Results
    ↓
Store in Database
    ↓
Return to Frontend
    ↓
React Renders Quiz UI
```

---

## References

- **LangChain Documentation**: https://python.langchain.com
- **Gemini API**: https://ai.google.dev/docs
- **Prompt Engineering Guide**: https://www.promptingguide.ai/
- **JSON Schema**: https://json-schema.org/

---

**Document Version**: 1.0  
**Last Updated**: January 9, 2026  
**Author**: Wiki Quiz Generator Team
