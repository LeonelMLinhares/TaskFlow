"""
Testes de integração para o módulo de clima do TaskFlow.

Utiliza mocks para simular as respostas da API Open-Meteo,
garantindo que o fluxo de dados funcione corretamente sem
depender de conexão real com a internet durante o CI.
"""

import json
from io import BytesIO
from unittest.mock import patch, MagicMock

import pytest

from src.clima import (
    buscar_coordenadas,
    buscar_previsao,
    previsao_para_cidade,
    WMO_CODES,
)


# ─────────────────────────────────────────────
# Fixtures de respostas simuladas (mocks)
# ─────────────────────────────────────────────

MOCK_GEOCODING_RESPONSE = {
    "results": [
        {
            "name": "São Paulo",
            "latitude": -23.5505,
            "longitude": -46.6333,
            "country": "Brasil",
        }
    ]
}

MOCK_FORECAST_RESPONSE = {
    "daily": {
        "time": ["2025-08-01", "2025-08-02", "2025-08-03"],
        "temperature_2m_max": [28.5, 30.1, 25.0],
        "temperature_2m_min": [18.0, 19.5, 16.0],
        "weathercode": [0, 61, 95],
    }
}

MOCK_GEOCODING_EMPTY = {"results": []}


def _make_mock_response(payload: dict):
    """Cria um mock de urllib.request.urlopen com resposta JSON."""
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(payload).encode("utf-8")
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


# ─────────────────────────────────────────────
# Testes: buscar_coordenadas
# ─────────────────────────────────────────────

class TestBuscarCoordenadas:
    def test_retorna_coordenadas_de_cidade_valida(self):
        """Integração: resposta da API deve ser parseada corretamente."""
        mock_resp = _make_mock_response(MOCK_GEOCODING_RESPONSE)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            resultado = buscar_coordenadas("São Paulo")

        assert resultado["nome"] == "São Paulo"
        assert resultado["latitude"] == -23.5505
        assert resultado["longitude"] == -46.6333
        assert resultado["pais"] == "Brasil"

    def test_cidade_nao_encontrada_levanta_value_error(self):
        """Entrada inválida: API retorna lista vazia → ValueError."""
        mock_resp = _make_mock_response(MOCK_GEOCODING_EMPTY)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            with pytest.raises(ValueError, match="não encontrada"):
                buscar_coordenadas("CidadeInexistenteXXX")

    def test_cidade_vazia_levanta_value_error(self):
        """Entrada inválida: nome de cidade vazio."""
        with pytest.raises(ValueError, match="vazio"):
            buscar_coordenadas("")

    def test_cidade_apenas_espacos_levanta_value_error(self):
        """Entrada inválida: nome com apenas espaços."""
        with pytest.raises(ValueError, match="vazio"):
            buscar_coordenadas("   ")

    def test_falha_de_rede_levanta_runtime_error(self):
        """Caso limite: falha de conexão deve lançar RuntimeError."""
        with patch("urllib.request.urlopen", side_effect=OSError("timeout")):
            with pytest.raises(RuntimeError, match="geocodificação"):
                buscar_coordenadas("São Paulo")


# ─────────────────────────────────────────────
# Testes: buscar_previsao
# ─────────────────────────────────────────────

class TestBuscarPrevisao:
    def test_retorna_lista_com_dias_corretos(self):
        """Integração: deve retornar N dias de previsão."""
        mock_resp = _make_mock_response(MOCK_FORECAST_RESPONSE)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            previsao = buscar_previsao(-23.5505, -46.6333, dias=3)

        assert len(previsao) == 3

    def test_estrutura_de_cada_dia(self):
        """Integração: cada dia deve conter os campos esperados."""
        mock_resp = _make_mock_response(MOCK_FORECAST_RESPONSE)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            previsao = buscar_previsao(-23.5505, -46.6333, dias=3)

        dia = previsao[0]
        assert "data" in dia
        assert "temp_max" in dia
        assert "temp_min" in dia
        assert "condicao" in dia
        assert "codigo_wmo" in dia

    def test_temperaturas_corretas(self):
        """Integração: valores de temperatura devem bater com o mock."""
        mock_resp = _make_mock_response(MOCK_FORECAST_RESPONSE)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            previsao = buscar_previsao(-23.5505, -46.6333, dias=3)

        assert previsao[0]["temp_max"] == 28.5
        assert previsao[0]["temp_min"] == 18.0

    def test_codigo_wmo_mapeado_corretamente(self):
        """Integração: código WMO 0 → céu limpo; 95 → tempestade."""
        mock_resp = _make_mock_response(MOCK_FORECAST_RESPONSE)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            previsao = buscar_previsao(-23.5505, -46.6333, dias=3)

        assert "Céu limpo" in previsao[0]["condicao"]
        assert "Chuva" in previsao[1]["condicao"]
        assert "Tempestade" in previsao[2]["condicao"]

    def test_dias_invalidos_levanta_value_error(self):
        """Caso limite: dias fora do intervalo 1–7."""
        with pytest.raises(ValueError, match="entre 1 e 7"):
            buscar_previsao(-23.5, -46.6, dias=0)

        with pytest.raises(ValueError, match="entre 1 e 7"):
            buscar_previsao(-23.5, -46.6, dias=8)

    def test_falha_de_rede_levanta_runtime_error(self):
        """Caso limite: falha de conexão deve lançar RuntimeError."""
        with patch("urllib.request.urlopen", side_effect=OSError("timeout")):
            with pytest.raises(RuntimeError, match="previsão"):
                buscar_previsao(-23.5505, -46.6333, dias=3)


# ─────────────────────────────────────────────
# Testes: previsao_para_cidade (fluxo completo)
# ─────────────────────────────────────────────

class TestPrevisaoParaCidade:
    def test_fluxo_completo_retorna_estrutura_correta(self):
        """
        Integração ponta-a-ponta: simula geocodificação + previsão
        e valida a estrutura final retornada.
        """
        respostas = [
            _make_mock_response(MOCK_GEOCODING_RESPONSE),
            _make_mock_response(MOCK_FORECAST_RESPONSE),
        ]

        with patch("urllib.request.urlopen", side_effect=respostas):
            resultado = previsao_para_cidade("São Paulo", dias=3)

        assert "São Paulo" in resultado["cidade"]
        assert "Brasil" in resultado["cidade"]
        assert len(resultado["previsao"]) == 3

    def test_cidade_invalida_propaga_erro(self):
        """Integração: cidade inválida deve propagar ValueError."""
        mock_resp = _make_mock_response(MOCK_GEOCODING_EMPTY)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            with pytest.raises(ValueError, match="não encontrada"):
                previsao_para_cidade("XYZ_Cidade_Falsa")
