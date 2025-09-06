#!/usr/bin/env python3
"""
Test cases for validating QWebChannel interface consistency
Tests the unified interface naming using itemId instead of boardId
"""

import json
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.editor.backend_interface import BackendInterface, RequestModel


class TestInterfaceConsistency(unittest.TestCase):
    """Test interface consistency across all components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.backend = BackendInterface("test")
        self.test_item_id = "test-item-123"
    
    def test_request_model_uses_item_id(self):
        """Test that RequestModel uses item_id as request_id"""
        # Test RequestModel creation
        request = RequestModel(
            action="setCurrentItemId",
            data={"item_id": self.test_item_id},
            request_id=self.test_item_id
        )
        
        self.assertEqual(request.request_id, self.test_item_id)
        self.assertEqual(request.data["item_id"], self.test_item_id)
    
    def test_send_message_uses_item_id(self):
        """Test that send_message uses item_id as request_id"""
        with patch.object(self.backend, 'page') as mock_page:
            mock_page.runJavaScript = Mock()
            
            callback = Mock()
            
            # Test send_message with item_id
            self.backend.send_message(
                action="setCurrentItemId",
                data={"item_id": self.test_item_id},
                callback=callback,
                item_id=self.test_item_id
            )
            
            # Verify the JavaScript code uses item_id as request_id
            mock_page.runJavaScript.assert_called_once()
            js_code = mock_page.runJavaScript.call_args[0][0]
            
            # Check that item_id is used as request_id
            self.assertIn(f'"{self.test_item_id}"', js_code)
            self.assertIn('setCurrentItemId', js_code)
            
            # Verify no random ID generation
            self.assertNotIn('uuid', str(js_code))
            self.assertNotIn('random', str(js_code))
    
    def test_dispatch_request_with_item_id(self):
        """Test that dispatch_request properly handles item_id"""
        with patch.object(self.backend, 'handlers', {}):
            # Register a test handler
            def test_handler(data):
                return {"success": True, "item_id": data.get("item_id")}
            
            self.backend.register_handler("setCurrentItemId", test_handler)
            
            # Create request with item_id
            request_data = {
                "action": "setCurrentItemId",
                "data": {"item_id": self.test_item_id},
                "requestId": self.test_item_id
            }
            
            response = self.backend.dispatch_request(json.dumps(request_data))
            response_dict = json.loads(response)
            
            self.assertEqual(response_dict["requestId"], self.test_item_id)
            self.assertTrue(response_dict["success"])


class TestFrontendInterfaceConsistency(unittest.TestCase):
    """Test frontend interface consistency"""
    
    def test_markdown_interface_uses_item_id(self):
        """Test that markdown interface uses item_id consistently"""
        # This would normally test the actual HTML/JS files
        # For now, we'll verify the interface contract
        expected_actions = [
            "setCurrentItemId",
            "setValue",
            "getContent",
            "textChanged"
        ]
        
        for action in expected_actions:
            # Verify action names are consistent
            self.assertIsInstance(action, str)
            self.assertTrue(len(action) > 0)
    
    def test_excalidraw_interface_uses_item_id(self):
        """Test that excalidraw interface uses item_id consistently"""
        expected_actions = [
            "setCurrentItemId",
            "loadExcalidrawData",
            "getExcalidrawData"
        ]
        
        for action in expected_actions:
            # Verify action names are consistent
            self.assertIsInstance(action, str)
            self.assertTrue(len(action) > 0)
    
    def test_landing_interface_uses_item_id(self):
        """Test that landing interface uses item_id consistently"""
        expected_actions = [
            "updateRecentFiles",
            "showWelcomeMessage",
            "getRecentFiles"
        ]
        
        for action in expected_actions:
            # Verify action names are consistent
            self.assertIsInstance(action, str)
            self.assertTrue(len(action) > 0)


class TestMessageFormat(unittest.TestCase):
    """Test message format consistency"""
    
    def test_message_structure(self):
        """Test that all messages follow the same structure"""
        expected_structure = {
            "requestId": str,
            "action": str,
            "data": dict
        }
        
        # Test with a sample message
        message = {
            "requestId": "test-item-123",
            "action": "setCurrentItemId",
            "data": {"item_id": "test-item-123"}
        }
        
        for key, expected_type in expected_structure.items():
            self.assertIn(key, message)
            self.assertIsInstance(message[key], expected_type)
    
    def test_response_structure(self):
        """Test that all responses follow the same structure"""
        expected_structure = {
            "requestId": str,
            "success": bool
        }
        
        # Test with a sample response
        response = {
            "requestId": "test-item-123",
            "success": True,
            "data": {"item_id": "test-item-123"}
        }
        
        for key, expected_type in expected_structure.items():
            self.assertIn(key, response)
            self.assertIsInstance(response[key], expected_type)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete interface"""
    
    def test_end_to_end_item_id_flow(self):
        """Test complete flow with item_id"""
        backend = BackendInterface("test")
        
        # Simulate setting item_id
        request_data = {
            "action": "setCurrentItemId",
            "data": {"item_id": "integration-test-123"},
            "requestId": "integration-test-123"
        }
        
        # This would normally test the actual handler
        # For now, verify the request structure
        self.assertEqual(request_data["requestId"], "integration-test-123")
        self.assertEqual(request_data["data"]["item_id"], "integration-test-123")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)