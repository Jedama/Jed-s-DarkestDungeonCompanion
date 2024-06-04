import anthropic

class TextBlock:
    def __init__(self, text, type):
        self.text = text
        self.type = type

def prompt_claude(user_prompt, system_prompt, assistant_prompt, max_tokens=350, temperature=0.75):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
    )

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_prompt}
        ]
    )
    return message.content

def clean_response_claude(response):
    # Check if the response is a list and has exactly one element
    if isinstance(response, list) and len(response) == 1:
        text_block = response[0]
        
        # Check if the object in the list has a 'text' attribute
        if hasattr(text_block, 'text'):
            return text_block.text
        else:
            return "No text available in the TextBlock"
    else:
        return "Invalid response format"