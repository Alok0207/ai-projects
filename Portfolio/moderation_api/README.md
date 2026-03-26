# Content Moderation using OpenAI API

This project demonstrates how to use the OpenAI Moderation API to analyze and classify user input for safety.

## Features

* Accepts user input from terminal
* Uses OpenAI moderation model to analyze content
* Displays whether the content is flagged
* Shows only the categories that are flagged
* Uses a default prompt if no input is provided

## Tech Stack

* Python
* OpenAI API
* python-dotenv

## Project Structure

```text
moderation_api/
├── moderation.py
├── requirements.txt
├── README.md
└── .env.example
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your API key:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run

```bash
python moderation.py
```

## Example Usage

```text
Enter text to check (press Enter to use default): 
```

## Purpose

This project demonstrates:

* API usage for moderation
* basic safety filtering logic
* handling user input dynamically
* clean terminal-based interaction
