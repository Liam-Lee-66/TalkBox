# test_talkboxportal.py
import time

import pytest
from talkboxportal import Portal

@pytest.fixture
def portal():
    """Fixture to create a Portal instance with default settings."""
    return Portal()

def test_update_text(portal):
    """Test adding new text to the display queue."""
    sample_text = "Sample text for testing."
    portal.update_text(sample_text)
    # Assuming _text_queue is accessible for testing.
    # If not, adjust the approach to verify the update.
    assert sample_text == portal._text_queue.dequeue(), \
        "The text should be the first in the queue."

def test_change_input_language(portal):
    """Test changing the input language."""
    new_language = "French"
    portal.change_input_language(new_language)
    assert portal.input_language == new_language, \
        "The input language should be updated to French."

def test_change_output_language(portal):
    """Test changing the output language."""
    new_language = "German"
    portal.change_output_language(new_language)
    assert portal.output_language == new_language, \
        "The output language should be updated to German."

def test_disp_freq_change(portal):
    """Test changing the display frequency."""
    new_freq = 1.5
    portal.disp_freq = new_freq
    assert portal.disp_freq == new_freq, \
        "The display frequency should be updated."

def test_stop_displaying_effect(portal):
    """Test the effect of stopping the display."""
    portal.stop_displaying()
    # Assuming there's a way to check if the thread is alive.
    # If not, adjust based on implementation.
    assert not portal._display_thread.is_alive(), \
        "The display thread should be stopped after calling stop_displaying."

def test_initial_state(portal):
    """Test the initial state of the Portal."""
    assert portal.input_language == 'English', "Default input language should be English."
    assert portal.output_language == 'English', "Default output language should be English."
    assert portal.disp_freq == 2.0, "Default display frequency should be 2.0 seconds."

# def test_text_display_interval(portal, mocker):
#     """Test the text display interval."""
#     mocker.patch('time.sleep', return_value=None)  # Mock sleep
#     portal.update_text("First piece of text.")
#     portal.update_text("Second piece of text.")
#     assert portal._text_queue.size() == 2, "Two texts should be in the queue."
#
# def test_text_display_output(portal, mocker):
#     """Test the output of the displayed text."""
#     displayed_texts = []
#     mocker.patch('builtins.print', side_effect=lambda x: displayed_texts.append(x))
#     portal.update_text("Display this text.")
#     time.sleep(portal.disp_freq)
#     assert displayed_texts[-1] == "Displaying: Display this text.", "The text should be displayed."
#
# def test_text_display_output(portal, mocker):
#     """Test the output of the displayed text."""
#     displayed_texts = []
#     mocker.patch('builtins.print', side_effect=lambda x: displayed_texts.append(x))
#     portal.update_text("Display this text.")
#     time.sleep(portal.disp_freq)
#     assert displayed_texts[-1] == "Displaying: Display this text.", "The text should be displayed."
#
# def test_repeated_shutdown(portal):
#     """Test that calling stop_displaying multiple times doesn't raise an error."""
#     portal.stop_displaying()  # First call to stop
#     try:
#         portal.stop_displaying()  # Second call to stop
#     except RuntimeError:
#         pytest.fail("Calling stop_displaying() second time should not raise an error.")
#
# def test_restart_display(portal):
#     """Test restarting the display after stopping."""
#     portal.stop_displaying()
#     assert not portal._display_thread.is_alive(), "Display thread should be stopped."
#     portal.start_displaying()  # Method to restart the display, assuming it's implemented.
#     assert portal._display_thread.is_alive(), "Display thread should be running after restart."
#
