# Project_2

## Get Start

1. create a new conda environment for this project & activate it

```
conda create -n project python=3.7 anaconda -y
conda activate project
```

2. install variables

```
cd project_2
pip install -r requirements.txt
```

3. Setup Alpaca Environment Variable

If you are interest to use it in production, please change base url to "https://api.alpaca.markets".

```
export APCA_API_KEY_ID="your-alpaca-api-key-here"
export APCA_API_SECRET_KEY="your-alpaca-api-secret-key-here"
export APCA_API_BASE_URL="https://paper-api.alpaca.markets"
```

4. Run the Streamlit Application

```
streamlit run streamlit_app.py
```
