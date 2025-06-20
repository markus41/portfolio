from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class Segmenter:
    """Very simple rule based segment matcher."""

    def match(self, visitor: Dict[str, Any], rules: List[Dict[str, Any]]) -> List[str]:
        matched: List[str] = []
        for rule in rules:
            field, op, value = rule["field"], rule.get("op", "eq"), rule["value"]
            v = visitor.get(field)
            if op == "eq" and v == value:
                matched.append(rule["segment"])
            elif op == "gt" and isinstance(v, (int, float)) and v > value:
                matched.append(rule["segment"])
            elif op == "contains" and isinstance(v, str) and value in v:
                matched.append(rule["segment"])
        logger.info(f"Visitor {visitor.get('id')} matched segments {matched}")
        return matched
