"""
TaskFlow - Módulo de integração com API pública de clima.

Utiliza a Open-Meteo API (https://open-meteo.com/) — gratuita, sem chave.
A previsão do tempo ajuda o estudante a planejar dias de estudo intensivo
em casa versus atividades externas.
"""

import json
import urllib.parse
import urllib.request

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES = {
    0: "☀️  Céu limpo",
    1: "🌤️  Principalmente limpo",
    2: "⛅ Parcialmente nublado",
    3: "☁️  Nublado",
    45: "🌫️  Névoa",
    48: "🌫️  Névoa com geada",
    51: "🌦️  Chuvisco leve",
    53: "🌦️  Chuvisco moderado",
    55: "🌧️  Chuvisco intenso",
    61: "🌧️  Chuva leve",
    63: "🌧️  Chuva moderada",
    65: "🌧️  Chuva intensa",
    80: "🌦️  Pancadas de chuva leves",
    81: "🌦️  Pancadas de chuva moderadas",
    82: "⛈️  Pancadas de chuva intensas",
    95: "⛈️  Tempestade",
    99: "⛈️  Tempestade com granizo",
}


def _http_get(url: str) -> dict:
    """Realiza uma requisição HTTP GET e retorna o JSON parseado."""
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def buscar_coordenadas(cidade: str) -> dict:
    """
    Busca latitude e longitude de uma cidade via API de geocodificação.

    Args:
        cidade: Nome da cidade.

    Returns:
        Dicionário com 'nome', 'latitude', 'longitude' e 'pais'.

    Raises:
        ValueError: Se a cidade não for encontrada.
        RuntimeError: Se houver falha na comunicação com a API.
    """
    if not cidade or not cidade.strip():
        raise ValueError("O nome da cidade não pode ser vazio.")

    params = urllib.parse.urlencode({
        "name": cidade.strip(),
        "count": 1,
        "language": "pt",
        "format": "json",
    })
    url = f"{GEOCODING_URL}?{params}"

    try:
        data = _http_get(url)
    except Exception as exc:
        raise RuntimeError(f"Erro ao conectar com a API de geocodificação: {exc}") from exc

    resultados = data.get("results")
    if not resultados:
        raise ValueError(f"Cidade '{cidade}' não encontrada.")

    r = resultados[0]
    return {
        "nome": r.get("name", cidade),
        "latitude": r["latitude"],
        "longitude": r["longitude"],
        "pais": r.get("country", ""),
    }


def buscar_previsao(latitude: float, longitude: float, dias: int = 3) -> list[dict]:
    """
    Busca a previsão do tempo para os próximos dias.

    Args:
        latitude: Latitude da localização.
        longitude: Longitude da localização.
        dias: Número de dias de previsão (1–7).

    Returns:
        Lista de dicionários com data, temperatura máxima/mínima e condição.

    Raises:
        ValueError: Se os parâmetros forem inválidos.
        RuntimeError: Se houver falha na comunicação com a API.
    """
    if not (1 <= dias <= 7):
        raise ValueError("O número de dias deve ser entre 1 e 7.")

    params = urllib.parse.urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "auto",
        "forecast_days": dias,
    })
    url = f"{FORECAST_URL}?{params}"

    try:
        data = _http_get(url)
    except Exception as exc:
        raise RuntimeError(f"Erro ao conectar com a API de previsão: {exc}") from exc

    daily = data.get("daily", {})
    datas = daily.get("time", [])
    temp_max = daily.get("temperature_2m_max", [])
    temp_min = daily.get("temperature_2m_min", [])
    codes = daily.get("weathercode", [])

    previsao = []
    for i, data_dia in enumerate(datas):
        code = codes[i] if i < len(codes) else 0
        previsao.append({
            "data": data_dia,
            "temp_max": temp_max[i] if i < len(temp_max) else None,
            "temp_min": temp_min[i] if i < len(temp_min) else None,
            "condicao": WMO_CODES.get(code, "Condição desconhecida"),
            "codigo_wmo": code,
        })

    return previsao


def previsao_para_cidade(cidade: str, dias: int = 3) -> dict:
    """
    Função de alto nível: retorna coordenadas + previsão para uma cidade.

    Args:
        cidade: Nome da cidade.
        dias: Número de dias de previsão.

    Returns:
        Dicionário com 'cidade' e 'previsao'.
    """
    coords = buscar_coordenadas(cidade)
    previsao = buscar_previsao(coords["latitude"], coords["longitude"], dias)
    return {
        "cidade": f"{coords['nome']}, {coords['pais']}",
        "previsao": previsao,
    }
