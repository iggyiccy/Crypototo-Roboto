# import neptune.new as neptune

# run = neptune.init(project='iggyiccy/Project2MarketSignal',
#                    api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJhOGYxMzYwZC1hYWZmLTQ2OTEtYTMzZC1lMzczYzc4OTIyZWEifQ==') # your credentials

# params = {"learning_rate": 0.001,
#           "optimizer": "Adam"}
# run["parameters"] = params

# for epoch in range(10):
#    run["train/loss"].log(0.9 ** epoch)

# run["eval/f1_score"] = 0.66

# run.stop()
