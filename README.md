# GTW-RAG-ChatBot


GTW-RAG-ChatBot is a Flask-based application that hosts a chatbot endpoint to respond to queries using a specified reference in a vector database.

# Table of Content

1. [System Config](#System-Config)
2. [Endpoint](#endpoint)
3. [Request Body](#request-body)
4. [Makefile](#makefile)
5. [資料夾說明](#資料夾說明)
6. [執行方式](#執行方式)
7. [Work In Progress](#work-in-progress)


## System Config
### 啟動服務前，可先設定正確的資料庫名稱以及其他參數 `system_config.yaml`
```
default_version: "v1"

required_chatbot_fields:
  retriever_threshold: .3
  retriever_topk: 5

required_db_fields:
  vector_db_path: "./vectorstores"
  prompt_db_path: "./prompt"
  prompt_name: "rag_v1.md"
```
- default_version: 版本
- required_chatbot_fields: Retriever threshold & retrieve numbers
- required_db_fields
   - vector db name on AWS s3
   - prompt db on AWS s3
   - prompt name 

## Endpoint

The API endpoint for the GTW-RAG-ChatBot is accessible at:

`{base_url}/chat/v1`

### Example Usages:
- **Base URL:** `http://dev.example.com`
- **Endpoint:** `http://dev.example.com/chat/v1`


Replace `{base_url}` with the actual base URL of your respective environment.

## Request Body

The API expects a JSON payload in the request body with the following structure:

```json
{
   "query": "Your question here"
}
```

## Makefile

### Deploy Info
- `HOME_DIR`: C:/Users/{ueser}
- `DOCKER_IMAGE_NAME`: GTW-RAG-Doument-System
- `DOCKER_IMAGE_VERSION`: 0.0.0
- `DOCKER_CONTAINER_NAME`: GTW-RAG-Doument-System-test
- `AWS_CONFIG_PATH`: $(HOME_DIR)/.aws
- `AWS_S3_profile`: default
- `AWS_Bedrock_profile`: bedrock

### Available Targets:
- `build`: Build the Docker image for the Flask app.
- `run`: Run the Flask app in a Docker container with .aws volume mount.
<!-- - `test`: Run unit tests from unit_test.py. -->
- `clean`: Stop and remove the Docker container, and remove the Docker image.
- `help`: Show available targets and their descriptions.

### Usage:
- `make build`: Build the Docker image.
- `make run`: Run the Flask app in a Docker container with AWS configuration.
<!-- - `make test`: Run unit tests. -->
- `make clean`: Stop the container and remove both the container and image.

## 資料夾說明

### Chatbot

### 評估
- eval: 儲存評估相關的程式碼
   - manager: 不同 package 提供的評估器，包裝的package為 [Ragas](https://docs.ragas.io/en/latest/index.html) 與 [trulens](https://github.com/truera/trulens)
   - service: 調用 manager 內容


## 執行方式

### Chatbot

### 評估
- 執行 `evaluator.py`
   ```
   >> python evaluator.py --file_path your_eval_csv_path --output_path your_output_csv_path --method choose_eval_method --gpt_reason
   ```
   - file_path: 需要評估的檔案，目前只支援csv
   - output_path: 輸出評估結果位置，目前只支援csv
   - method: 評估的方式，目前提供4種
      - `groundness`: 需提供 answer 與 context 欄位
      - `context_relevancy`: 需提供 question 與 context 欄位
      - `answer_relevancy`: 需提供 question 與 answer 欄位
      - `context_precision`: 需提供 answer 與 contexts 欄位
   - gpt_reason: 是否將 trulens Chatgpt cot 的結果輸出

- 評估的部分 `trulens`  groundness 因為原本套件的作法在parse分數有錯誤 有改到裡面的內容
   - 版本: `0.18.2`
   - 位置: `trulens_eval\feedback\groundedness.py` 裡 `groundedness_measure_with_cot_reasons` function:
      ```
      groundedness_scores = {}
        if isinstance(self.groundedness_provider,
                      (AzureOpenAI, OpenAI, LiteLLM, Bedrock)):
            plausible_junk_char_min = 4  # very likely "sentences" under 4 characters are punctuation, spaces, etc
            if len(statement) > plausible_junk_char_min:
                reason = self.groundedness_provider._groundedness_doc_in_out(
                    source, statement
                )
            i = 0
            for line in reason.split('\n'):
                if "Score" in line:
                    parse_score = gamania_re_0_10_rating(line) ## 需新增一個 gamania_re_0_10_rating function，在程式碼一開始也多 import 這個 function
                    if parse_score >= 0: ## 多判斷parse回來的分數是否大於0
                        groundedness_scores[f"statement_{i}"
                                        ] = parse_score / 10
                        i += 1
            return groundedness_scores, {"reason": reason}
        elif isinstance(self.groundedness_provider, Huggingface):
            raise Exception(
                "Chain of Thought reasoning is only applicable to OpenAI groundedness providers. Instantiate `Groundedness(groundedness_provider=OpenAI())` or use `groundedness_measure` feedback function."
            )
      ```
   - 位置: `trulens_eval\utils\generated.py` 裡新增 `gamania_re_0_10_rating` function:
      ```
      def gamania_re_0_10_rating(str_val):
         matches = gamania_pat_0_10.fullmatch(str_val)
         if not matches:
            return -10

         return int(matches.group(1))
      ```

## Work In Progress
- [ ] 薪增安裝說明
- [ ] unit test
- [ ] python 套件版本管理方式
- [ ] docker build