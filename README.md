# weather proxy

## Start server

1. Maintain env
```bash
export WEATHER_API=weathermap-apikey
```

2. Run in docker:
```bash
docker compose up --build
```

## Usage

```bash
curl --location --request GET '0.0.0.0:8080/weather?country_code=ru&city=Moscow&date=2021-11-01 10:00'
```
Date time format must be only in such format which represented in example above
