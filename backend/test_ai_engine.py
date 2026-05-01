import pytest
from unittest.mock import MagicMock, patch
import ai_engine

def test_generate_intro_pitch_mock():
    with patch('ai_engine.client') as mock_client:
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = "Hello from AI"
        mock_client.models.generate_content.return_value = mock_response
        
        result = ai_engine.generate_intro_pitch("10", "Tech", "No AI")
        assert result == "Hello from AI"
        mock_client.models.generate_content.assert_called_once()

def test_generate_intro_pitch_no_client():
    with patch('ai_engine.client', None):
        result = ai_engine.generate_intro_pitch("10", "Tech", "No AI")
        assert "Hello! I'm Aura" in result

def test_generate_sales_response_mock():
    with patch('ai_engine.client') as mock_client:
        mock_response = MagicMock()
        mock_response.text = "AI Sales Pitch"
        mock_client.models.generate_content.return_value = mock_response
        
        history = [{"sender": "user", "content": "Hi"}]
        result = ai_engine.generate_sales_response(history, "Tell me more")
        assert result == "AI Sales Pitch"

def test_analyze_lead_score_valid():
    with patch('ai_engine.client') as mock_client:
        mock_response = MagicMock()
        mock_response.text = "The score is 85.5"
        mock_client.models.generate_content.return_value = mock_response
        
        history = [{"sender": "user", "content": "I want to buy"}]
        score = ai_engine.analyze_lead_score(history)
        assert score == 85.5

def test_analyze_lead_score_invalid():
    with patch('ai_engine.client') as mock_client:
        mock_response = MagicMock()
        mock_response.text = "I don't know"
        mock_client.models.generate_content.return_value = mock_response
        
        score = ai_engine.analyze_lead_score([])
        assert score == 50.0

def test_analyze_lead_score_exception():
    with patch('ai_engine.client') as mock_client:
        mock_client.models.generate_content.side_effect = Exception("API Down")
        score = ai_engine.analyze_lead_score([])
        assert score == 50.0
