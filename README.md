# Shiva Bot - HR Assistant Chatbot (Rasa)

A conversational HR assistant built with **Rasa 3.6** that helps employees check leave balances, salary, and bonus details through natural-language chat. A lightweight **Flask** backend serves employee data via a REST API, and Rasa custom actions query it during conversations.

## How It Works

```
User <-> Rasa NLU/Core  <->  Custom Actions (rasa_sdk)  <->  Flask API (backend/app.py)
```

- **Rasa pipeline:** WhitespaceTokenizer, Regex + CountVectors featurizers, DIETClassifier; RulePolicy + TEDPolicy
- **Forms and validation:** `ValidateLeaveForm` validates employee IDs and leave types (casual / sick / earned)
- **Flask backend:** mock employee database exposing leave balances, salary, and bonus per employee ID

## Project Structure

```
actions/actions.py    # Custom actions + form validation
backend/app.py        # Flask REST API (employee data)
data/nlu.yml          # Training examples
data/rules.yml        # Conversation rules
domain.yml            # Intents, slots, responses, forms
config.yml            # NLU pipeline + policies
```

## Setup and Run

Requires **Python 3.10**.

```bash
python3.10 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

rasa train
```

Then run each in its own terminal:

```bash
cd backend && python app.py     # 1. Start the Flask employee API
rasa run actions                # 2. Start the custom actions server
rasa shell                      # 3. Chat with the bot
```
