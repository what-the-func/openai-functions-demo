# OpenAI Function Demo

A demonstration of how GPT-3.5/4 can be used as a reasoning engine to perform tasks using the powerful Function Calls feature

## Usage

The demo uses a dummy email marketing system that can create lists, add contacts to lists and send emails to specific lists.
Ask the system to perform a task or set of tasks.

**Example Request**

```
Create a new email list called Cold Leads then add the following emails to that list
bob@example.com, sally@acme.com
Finally send an email to that list with the subject 'Hello' and body 'Blah blah blah...'
```

**Example Response**

```
I created a new email list called "Cold Leads". Then, I added bob@example.com and sally@acme.com to this list.
Finally, I sent an email to the "Cold Leads" list with the subject 'Hello' and body 'Blah blah blah...'.
```

**Example Terminal Output**

```sh
Created list Cold Leads
Added bob@example.com to Cold Leads
Added sally@acme.com to Cold Leads
Sent email to Cold Leads with subject Hello and body Blah blah blah...
```

## Dependencies

The application depends on several Python libraries, including:

- openai
- langchain
- python-dotenv
- streamlit

Please see the `requirements.txt` file for the exact versions of these dependencies.

## Installation

To install the application, first clone this repository:

```bash
git clone https://github.com/what-the-func/openai-functions-demo
```

Then, navigate to the project directory and install the dependencies:

```bash
cd openai-functions-demo
pip install -r requirements.txt
```

Copy the `.env.example` file to `.env` and fill in the required environment variables:

```bash
cp .env.example .env
```

Finally, run the application:

```bash
streamlit run app.py
```

## License

This project is licensed under the terms of the MIT license.
