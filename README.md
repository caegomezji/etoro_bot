# ETORO TRADER BOT

> **__IN DEVELOPMENT__**

I do this project just for fun. Please be careful!!!
If you want to contribute you can make a PR.


# Instalation

### Without docker 

1. Install the dependencies.
```bash
pip install \
    selenium==4.16.0 \
    undetected-chromedriver==3.5.4 \
    fastapi \
    uvicorn 
```

2. Set the environment variables with your etoro credentials.

```bash
export ETORO_USER=blablabla
export ETORO_PWD=blablabla
```
3. Start the service 
```bash
uvicorn etoro_bot.main:app
```

### With docker 

1. Create the `.env` file with the `.env.example` as example 

2. Run the script `./create_docker_selenium.sh`

# Using the service
Make a http post like this

```python
requests.post(
    "http://localhost:8000/trade",
    json={
        "trade_action": "buy",
        "symbol": "BTC",
        "virtual_portfolio" : True,
        "value":50
    },
    headers={"accept"  : "application/json",
            "Content-Type":"application/json"}
)

```
# Considerations
- One issue with docker by the moment is, you can not see the chrome gui interface. **PR ARE OPEN ;)**
- however without docker you can set the environment variable `SELENIUM_GUI=true`
- The telegram service is optional...  is just for advising  if there were some problems. keep it as false or not setted


