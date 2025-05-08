import streamlit as st
import base64

from openai import OpenAI

# Judul aplikasi llm
st.title("Deteksi Ekstensi File")

# User input for API key
api_key = st.text_input("Enter your API Key:", type="password")
if api_key:
    client = OpenAI(api_key=api_key)

# Upload file
uploaded_file = st.file_uploader("Upload file", type="pdf")  # None artinya semua jenis file boleh diupload
if uploaded_file is not None:
    # Baca nama dan jenis file
    file_name = uploaded_file.name
    file_type = uploaded_file.type

    # Baca file sebagai bytes
    file_bytes = uploaded_file.read()

    # Encode ke base64
    encoded_base64 = base64.b64encode(file_bytes).decode('utf-8')
    
    # Tampilkan hasil
    st.write(f"Nama file: {file_name}")
    st.write(f"Tipe file: `{file_type}`")

    tab1, tab2 = st.tabs(["Summary", "Points"])
    with tab1:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "file",
                            "file": {
                                "filename": "draconomicon.pdf",
                                "file_data": f"data:application/pdf;base64,{encoded_base64}",
                            }
                        },
                        {
                            "type": "text",
                            "text": "Summarize the file into one paragraph.",
                        }
                    ],
                },
            ],
        )
        answer = completion.choices[0].message.content
        input_tokens = completion.usage.prompt_tokens
        output_tokens = completion.usage.completion_tokens
        price = 17_000 * ((input_tokens*0.15) + (output_tokens*0.6))/1_000_000
        with st.container():
            st.write(answer)
        with st.popover("Open Usage Details"):
            st.write(f"input_tokens : {input_tokens}")
            st.write(f"output_tokens : {output_tokens}")
            st.write(f"price (IDR): {price}")
    with tab2:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "file",
                            "file": {
                                "filename": "draconomicon.pdf",
                                "file_data": f"data:application/pdf;base64,{encoded_base64}",
                            }
                        },
                        {
                            "type": "text",
                            "text": "Summarize the file into several bullet points.",
                        }
                    ],
                },
            ],
        )
        answer = completion.choices[0].message.content
        input_tokens = completion.usage.prompt_tokens
        output_tokens = completion.usage.completion_tokens
        price = 17_000 * ((input_tokens*0.15) + (output_tokens*0.6))/1_000_000
        with st.container():
            st.write(answer)
        with st.popover("Open Usage Details"):
            st.write(f"input_tokens : {input_tokens}")
            st.write(f"output_tokens : {output_tokens}")
            st.write(f"price (IDR): {price}")