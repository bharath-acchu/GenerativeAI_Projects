## End to End Medical ChatBot Using GenAI

### Tech Stack Used:
* Python
* Langchain
* Google Gemini
* Chromadb
* HTML,CSS,Flask 


## Follow these steps to run 

### 1. Clone the repo

```bash
    git clone https://github.com/bharath-acchu/GenerativeAI_Projects.git
 ```

 ### 2. Change the directory to End_To_End_MedicalChatBot

 ```bash
    cd SourceCodeAnalayser
 ```

 ### 3. Create a conda env

```bash
    conda create -n <env_name> python=3.10 -y
```
### 4. Activate the env variable

```bash
    conda activate <env_name>
```
### 5. Install packages 
```bash
    pip install -r requirements.txt
```
### 6. Add your API KEYS in .env 

```bash
GOGGGLE_API_KEY = "***************************************"
```
### 7. Run the follwoing to store embeddings to pinecone
```bash
    python store_index.py
```
#### Note : Step 7 Will create a local chromadb

### 8. Finally run app.py
```bash
    python app.py
```

### 9. Open up in your localhost
```bash
    http://localhost:8080
```


