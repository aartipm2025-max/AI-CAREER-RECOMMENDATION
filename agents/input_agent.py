from core.config import VALID_STREAMS

class ValidationError(Exception):
    pass

class InputAgent:
    def __init__(self):
        self.valid_streams = [s.strip() for s in VALID_STREAMS]

    def validate_stream(self, user_input: str) -> str:
        """
        Normalises and validates user input for stream.
        Expected outputs: 'Science', 'Commerce', 'Arts'
        """
        if not user_input or not isinstance(user_input, str):
            raise ValidationError("Input must be a non-empty string.")

        # Normalise casing: capitalize first letter, lower rest
        normalised = user_input.strip().capitalize()

        if normalised not in self.valid_streams:
            raise ValidationError(f"Invalid stream: '{user_input}'. Please choose from {', '.join(self.valid_streams)}.")

        return normalised
