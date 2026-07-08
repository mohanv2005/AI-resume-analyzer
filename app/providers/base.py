class BaseProvider:
   """
    Abstract base class for all AI providers.
    Every provider must implement the generate() method.

    This ensures all providers have the same interface —
    the rest of the app calls provider.generate(prompt)
    and never needs to know which SDK is underneath.
    """
   
   def generate(self, prompt: str) -> str:  
      """
        Send a prompt to the AI model and return the text response.

        Args:
            prompt: The full prompt string to send

        Returns:
            The model's response as a plain string

        Raises:
            NotImplementedError: if subclass doesn't implement this
        """
      raise NotImplementedError(f"{self.__class__.__name__} must implement generate()")
   
   def get_provider_name(self) -> str:
      return self.__class__.__name__
   