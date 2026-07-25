import gradio as gr
import requests


def get_ayah(ayat):
    try:
        # Check if input is empty
        if ayat is None:
            return "❌ Please enter an ayat number."

        # API URL
        url = f"https://api.alquran.cloud/v1/ayah/{int(ayat)}"

        # Send GET request
        response = requests.get(url)
        data = response.json()

        # Check if API returned success
        if data["code"] != 200:
            return "❌ Ayat not found. Please enter a valid ayat number."

        ayah = data["data"]

        # Extract information
        ayah_number = ayah["number"]
        text = ayah["text"]
        surah_name = ayah["surah"]["name"]
        surah_number = ayah["surah"]["number"]
        english_name = ayah["surah"]["englishName"]
        english_translation = ayah["surah"]["englishNameTranslation"]
        total_ayahs = ayah["surah"]["numberOfAyahs"]
        revelation_type = ayah["surah"]["revelationType"]
        manzil = ayah["manzil"]
        sajda = "Yes" if ayah["sajda"]==True else "No"

        # Return formatted Markdown
        return f"""
# 📖 Quran Ayat

### 🆔 Ayat Number
**{ayah_number}**

### 📜 Arabic Text
{text}

### 🕌 Surah Information
- **Surah Name:** {surah_name}
- **English Name:** {english_name}
- **Meaning:** {english_translation}
- **Surah Number:** {surah_number}
- **Total Ayahs:** {total_ayahs}
- **Revelation Type:** {revelation_type}
- **Manzil:** {manzil}
- **Sajda:** {sajda}


"""

    except Exception as e:
        return f"❌ Error: {e}"

      # Function to clear input and output
def reset():
    return None, ""


with gr.Blocks(title="Quran Ayat Finder") as demo:

    gr.Markdown("# 📖 Quran Ayat Finder")
    gr.Markdown("Enter the global **Quran ayah number** (1-6236)")

    ayat_input = gr.Number(
        label="Enter Ayat Number",
        precision=0,
        minimum=1
    )

    with gr.Row():

      search_button = gr.Button("🔍 Search")
      reset_button = gr.Button("🔄 Reset", variant="secondary")

    output = gr.Markdown()

    search_button.click(
        fn=get_ayah,
        inputs=ayat_input,
        outputs=output
    )

    ayat_input.submit(
    fn=get_ayah,
    inputs=ayat_input,
    outputs=output
)
    # Reset button
    reset_button.click(
        fn=reset,
        inputs=[],
        outputs=[ayat_input, output]
    )

demo.launch()
