"""
class AgentEvaluator: A class that evaluates the agent's performance
based on the messages exchanged between the user and the assistant.
The class is made callable by implementing the special method
__call__. The class has four methods that validate the count of
dictionaries, assistant messages, user messages, and the time
difference between messages. The __call__ method calculates the
total score based on the results of the four validation methods and
returns the agent's score as a percentage.
"""
import json
from typing import List, Dict, Any


class AgentEvaluator:
    """ A class that evaluates the agent's performance."""
    def __init__(self):
        pass

    # A class is made a callable my implementing the special method __call__
    def __call__(self,
                 *,
                 full_output: str,
                 total_message_count: str,
                 total_user_message_count: str,
                 total_assistant_message_count: str,
                 time_difference: str,
                 **kwargs
                 ):

        full_output = json.loads(full_output)

        total_count = self.validate_dictionary_count(
            full_output,
            int(total_message_count)
        )

        assistant_count = self.validate_assistant_messages_count(
            full_output,
            int(total_assistant_message_count)
        )

        user_count = self.validate_user_messages_count(
            full_output,
            int(total_user_message_count)
        )

        time_diff = self.validate_time_difference(
            full_output,
            int(time_difference)
        )

        total_score = total_count + assistant_count + user_count + time_diff

        # Calculate percentage (4 is the maximum possible score)
        percentage = (total_score / 4) * 100

        return {"agent_score": int(percentage)}

    def validate_dictionary_count(self, messages: Any, expected_count: int) -> int:
        """
        Validates if the count of dictionaries matches the expected number
        Returns 1 if matches, 0 otherwise
        """

        return 1 if len(messages) == expected_count else 0

    def validate_assistant_messages_count(self, messages: List[Dict[str, Any]], expected_count: int) -> int:
        """
        Validates if the count of assistant messages matches the expected number
        Returns 1 if matches, 0 otherwise
        """
        assistant_count = sum(
            1 for msg in messages
            if msg.get('assistant_id') is not None and msg.get('role') == "assistant"
        )
        return 1 if assistant_count == expected_count else 0

    def validate_user_messages_count(self, messages: List[Dict[str, Any]], expected_count: int) -> int:
        """
        Validates if the count of user messages matches the expected number
        Returns 1 if matches, 0 otherwise
        """
        user_count = sum(
            1 for msg in messages
            if msg.get('assistant_id') is None and msg.get('role') == "user"
        )
        return 1 if user_count == expected_count else 0

    def validate_time_difference(self, messages: List[Dict[str, Any]], max_time_diff: int) -> int:
        """
        Validates if the time difference between messages is less than or equal to expected value
        Returns 1 if condition is met, 0 otherwise
        """
        if len(messages) < 2:
            return 1  # If there's only one or no messages, consider it valid

        timestamps = [int(msg['created_at']) for msg in messages]
        max_diff = max(timestamps) - min(timestamps)
        return 1 if max_diff <= max_time_diff else 0


if __name__ == "__main__":
    # Test the math response
    QUESTION = '[{"id": "xxx", "object": "thread.message", "created_at": ' \
           '"1739804579", "assistant_id": "xxxxx", "thread_id": "wwwww", ' \
           '"run_id": "rrrrr", "role": "assistant", "content_text": ' \
           '"The modular inverse of \\\\( 24 \\\\mod{121} \\\\) is \\\\( 116 ' \
           '\\\\)."}, {"id": "qqqq", "object": "thread.message", ' \
           '"created_at": "1739804575", "thread_id": "wwwww", "role": "user", ' \
           '"content_text": "Find \\\\( 24^{-1} \\\\pmod{11^2} \\\\)?"}]'

    agent_evaluator_test = AgentEvaluator()
    result = agent_evaluator_test(
        full_output=QUESTION,
        total_message_count=2,
        total_user_message_count=1,
        total_assistant_message_count=1,
        time_difference=10
    )
    print(result)
