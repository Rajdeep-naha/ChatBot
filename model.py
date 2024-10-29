def model(prompt,client,hf_api_key,history):

    history.append(prompt)

    if len(history) > 10:
        history.pop(0)

    prompt = prompt+"\nThese messages below are my previous messages:\n" + "\n".join(history) + "\nPlease use these as a backup when the current message is not sufficient or more information is needed.\n"

    messages = [
        {"role": "user", "content": prompt}
    ]

    stream = client.chat.completions.create(
        model="mistralai/Mistral-Nemo-Instruct-2407",
        messages=messages,
        max_tokens=500,
        stream=True
    )

    response = ""

    for chunk in stream:
        response += chunk.choices[0].delta.content

    return response
