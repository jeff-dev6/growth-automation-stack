import pytest
from modules.registry_validation import RegistryValidator

class TestRegistryValidator:
    """
    Suite of unit tests for the RegistryValidator service.
    Focuses on boundary value analysis and error code accuracy.

    """

    @pytest.mark.parametrize("credential, expected_valid, expected_error", [
        # --- SUCCESS CASES ---
        ("CS50", True, None),
        ("NRVOUS", True, None),
        ("  CS50  ", True, None),    # Testing sanitization
        ("ABC123", True, None),

        # --- FAILURE CASES: LENGTH ---
        ("A", False, "ERR_INVALID_CHAR_LENGTH"),         # Too short
        ("TOOLONG1", False, "ERR_INVALID_CHAR_LENGTH"),  # Too long

        # --- FAILURE CASES: SYNTAX ---
        ("PI3.14", False, "ERR_INVALID_CHAR"),           # Special character
        ("CS 50", False, "ERR_INVALID_CHAR"),            # Space (after strip)

        # --- FAILURE CASES: PREFIX ---
        ("C1234", False, "ERR_INVALID_LEADING_CHAR"),    # Only 1 letter
        ("123456", False, "ERR_INVALID_LEADING_CHAR"),   # No letters

        # --- FAILURE CASES: PATTERN/SEQUENCING ---
        ("CS05", False, "ERR_COMPLIANCE_PATTERN_MISMATCH"),   # Leading zero
        ("CS50A", False, "ERR_COMPLIANCE_PATTERN_MISMATCH"),  # Number in middle
        
        # --- FAILURE CASES: EMPTY ---
        ("", False, "ERR_EMPTY_INPUT"),
        ("   ", False, "ERR_EMPTY_INPUT"),
    ])

    def test_validate_identifier_compliance(self, credential, expected_valid, expected_error):
        """
        Validates that the identifier complies with regulatory standards 
        and returns the correct error codes upon failure.
        Args:
            credential (str): The alphanumeric string to validate.
            expected_valid (bool): Expected validity outcome.
            expected_error (str): Expected error message.
            
        """
        # Execute unit
        result = RegistryValidator.validate_identifier(credential)

        # Assertions
        assert result["is_valid"] == expected_valid
        assert result["error_code"] == expected_error