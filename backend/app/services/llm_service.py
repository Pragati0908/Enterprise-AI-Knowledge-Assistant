import requests


class LLMService:
    """
    Handles communication with the local Ollama LLM.
    """

    BASE_URL = "http://localhost:11434/api/generate"

    MODEL = "llama3.2"

    TIMEOUT = 120

    @classmethod
    def generate(cls, prompt: str) -> str:
        """
        Send a prompt to Ollama and return the generated response.
        """

        payload = {
            "model": cls.MODEL,
            "prompt": prompt,
            "stream": False
        }

        try:

            response = requests.post(
                cls.BASE_URL,
                json=payload,
                timeout=cls.TIMEOUT
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                ""
            ).strip()

        except requests.exceptions.ConnectionError:

            raise RuntimeError(
                "Cannot connect to Ollama. "
                "Make sure Ollama is installed and running."
            )

        except requests.exceptions.Timeout:

            raise RuntimeError(
                "Ollama request timed out."
            )

        except requests.exceptions.HTTPError as e:

            raise RuntimeError(
                f"Ollama HTTP Error: {e}"
            )

        except requests.exceptions.RequestException as e:

            raise RuntimeError(
                f"LLM request failed: {e}"
            )

    # -------------------------------------------------------
    # Backward Compatibility
    # -------------------------------------------------------

    @classmethod
    def generate_response(cls, prompt: str) -> str:
        """
        Backward-compatible wrapper.
        Existing code can continue calling generate_response().
        """
        return cls.generate(prompt)

    # -------------------------------------------------------
    # Health Check
    # -------------------------------------------------------

    @classmethod
    def is_available(cls) -> bool:
        """
        Returns True if Ollama server is reachable.
        """

        try:

            requests.get(
                "http://localhost:11434",
                timeout=3
            )

            return True

        except Exception:

            return False