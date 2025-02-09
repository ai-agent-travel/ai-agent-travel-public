import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_structured_output_runnable
from langchain_google_vertexai import VertexAI, ChatVertexAI, create_structured_runnable
from langchain_core.messages import SystemMessage
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        try:
            self.llm = VertexAI(
                model_name="gemini-1.5-pro",
                project=os.getenv("PROJECT_ID"),
                location=os.getenv("LOCATION", "asia-northeast1")
            )
            logger.info("VertexAI initialized successfully")
        except Exception as e:
            logger.error(f"VertexAIの初期化エラー: {str(e)}")
            raise

        try:
            self.structured_llm = ChatOpenAI(
                model_name="gpt-4o",
                temperature=0,
                max_tokens=None,
                max_retries=6,
                stop=None,
            )
            logger.info("ChatOpenAI initialized successfully")
        except Exception as e:
            logger.error(f"ChatOpenAIの初期化エラー: {str(e)}")
            raise

        try:
            self.structured_llm_v2 = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=0,
                max_tokens=None,
                timeout=None,
                google_api_key=os.getenv("GEMINI_API_KEY"),
            )
            logger.info("ChatGoogleGenerativeAI initialized successfully")
        except Exception as e:
            logger.error(f"ChatGoogleGenerativeAIの初期化エラー: {str(e)}")
            raise

    def invoke(self, messages: list) -> str:
        try:
            response = self.llm.invoke(messages)
            return response
        except Exception as e:
            print(f"Error in LLMService.invoke: {str(e)}")
            raise
    
    def _clean_json_response(self, response: str) -> str:
        """マークダウンの装飾やその他の不要な文字を削除してJSONを抽出"""
        # マークダウンのJSON装飾を削除
        response = response.replace("```json", "").replace("```", "")
        # 前後の空白を削除
        response = response.strip()
        return response

    def invoke_structured(self, OutputStructure: any, prompt: str) -> str:
        try:
            chain = self.structured_llm.with_structured_output(OutputStructure)

            result = chain.invoke(prompt)
            
            # 結果が文字列の場合（生のレスポンス）、JSONをクリーニング
            if isinstance(result, str):
                result = self._clean_json_response(result)
            
            return result
        except Exception as e:
            print(f"Error in LLMService.invoke_structured: {str(e)}")
            raise

    def invoke_structured_v2(self, OutputStructure: any, prompt: any) -> object:
        try:
            # chain = self.structured_llm_v2.with_structured_output(OutputStructure)
            # input_payload = prompt  # Pass the list of messages directly

            # Construct the chain: LLM + structured output parsing. Note that 
            # `self.structured_llm_v2` is assumed to be *already* a Runnable.
            _chain = self.structured_llm_v2.with_structured_output(OutputStructure)
            result = _chain.invoke(prompt)

            return result
        except Exception as e:
            print(f"Error in LLMService.invoke_structured_v2: {str(e)}")
            raise

# 環境変数のチェック
try:
    required_vars = ["PROJECT_ID", "LOCATION", "GEMINI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

    llm_service = LLMService()
    logger.info("LLMService initialized successfully")
except Exception as e:
    logger.error(f"LLMServiceの初期化に失敗: {str(e)}")
    raise
