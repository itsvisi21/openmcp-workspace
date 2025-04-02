from typing import Dict, Any, Optional
import openai
import anthropic
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.openai_client = openai.Client(api_key=settings.OPENAI_API_KEY)
        self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.default_provider = settings.DEFAULT_LLM_PROVIDER
        self.max_tokens = settings.MAX_TOKENS

    async def process_context(
        self,
        content: str,
        type: str,
        metadata: Dict[str, Any],
        provider: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process context using the specified LLM provider."""
        provider = provider or self.default_provider

        if provider == "openai":
            return await self._process_with_openai(content, type, metadata)
        elif provider == "anthropic":
            return await self._process_with_anthropic(content, type, metadata)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    async def _process_with_openai(
        self,
        content: str,
        type: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Process context using OpenAI's API."""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"Process the following {type} context and provide insights.",
                    },
                    {"role": "user", "content": content},
                ],
                max_tokens=self.max_tokens,
                temperature=0.7,
            )
            return {
                "provider": "openai",
                "model": "gpt-4",
                "response": response.choices[0].message.content,
                "metadata": {
                    **metadata,
                    "usage": response.usage.dict(),
                },
            }
        except Exception as e:
            raise Exception(f"OpenAI processing failed: {str(e)}")

    async def _process_with_anthropic(
        self,
        content: str,
        type: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Process context using Anthropic's API."""
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": f"Process the following {type} context and provide insights:\n\n{content}",
                    }
                ],
            )
            return {
                "provider": "anthropic",
                "model": "claude-3-opus-20240229",
                "response": response.content[0].text,
                "metadata": {
                    **metadata,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens,
                    },
                },
            }
        except Exception as e:
            raise Exception(f"Anthropic processing failed: {str(e)}") 