import re
from core.logger import get_logger

log = get_logger("registry_validation")

class RegistryValidator:
    """
    Service for validating alphanumeric identifiers based on 
    specific compliance rules.
    """

    @staticmethod
    def validate_identifier(credential: str) -> dict:
        """
        Runs a suite of compliance checks on a given string.

        Args:
            str(credential): The string provided for compliance check.

        Returns:
            dict: returns a dictionary with "is_valid" (bool) and "error_code" (str)
        """
        cleaned_credential = credential.strip().upper()

        if not cleaned_credential:
            return {"is_valid": False, "error_code": "ERR_EMPTY_INPUT"}
            
        # Rule 1. Length check (2-6 characters)
        if not (2 <= len(cleaned_credential) <= 6):
            return {"is_valid": False, "error_code": "ERR_INVALID_CHAR_LENGTH"}
       
        # Rule 2. Syntax check: No special characters or spaces
        if not cleaned_credential.isalnum():
            return {"is_valid": False, "error_code": "ERR_INVALID_CHAR"}
        
        # Rule 3. Lead character requirement: Must start with 2 letters
        if not cleaned_credential[0:2].isalpha():
            return {"is_valid": False, "error_code": "ERR_INVALID_LEADING_CHAR"}
        
        # Rule 4. Numeric Sequencing using Regex (Regular Expressions) 
        # This regex looks for: letters, followed by numbers (no numbers in middle, no leading zero)
        pattern = r"^[A-Z]{2,6}$|^[A-Z]{2,5}[1-9][0-9]{0,3}$"
        if not re.match(pattern, cleaned_credential):
            return {"is_valid": False, "error_code": "ERR_COMPLIANCE_PATTERN_MISMATCH"}

        log.info(f"Credential Identifier Validated: {cleaned_credential}")
        return {"is_valid": True, "error_code": None}
