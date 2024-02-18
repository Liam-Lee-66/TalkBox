import time

from talkboxportal import Portal

# Initialize the Portal object with French as input and output language,
# and display frequency of 1.5 seconds
tbportal = Portal(input_language='French', output_language='French',
                  disp_freq=1.5)
print(f"Initialized Portal with input_language='{tbportal.input_language}'"
      f"and output_language='{tbportal.output_language}'")

# Update the text for display
sample_text = "Bonjour, comment ça va?"
tbportal.update_text(sample_text)
print(f"Updated text for display: '{sample_text}'")

# Wait for the display frequency duration to simulate the display interval
print("Waiting for text to be displayed...")
time.sleep(tbportal.disp_freq)

# Change the input language
new_input_language = "Spanish"
tbportal.change_input_language(new_input_language)
print(f"Input language changed to: '{tbportal.input_language}'")

# Change the output language
new_output_language = "English"
tbportal.change_output_language(new_output_language)
print(f"Output language changed to: '{tbportal.output_language}'")

# Add more text
additional_text = "¿Cómo estás hoy?"
tbportal.update_text(additional_text)
print(f"Additional text updated for display: '{additional_text}'")

# Wait to simulate text display
time.sleep(tbportal.disp_freq)

# Stop the display thread
tbportal.stop_displaying()
print("Stopped displaying text. Background thread terminated.")
