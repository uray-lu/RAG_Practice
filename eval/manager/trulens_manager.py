"""wrap trulens function"""
from trulens_eval.feedback import Groundedness
from trulens_eval.feedback.provider.openai import OpenAI as fOpenAI
from eval.manager.base import EvalBase

class TrulensManager(EvalBase):
    """trulens class"""
    def __init__(self, model_name='gpt-3.5-turbo-16k', save_reason=True):
        self._openai_provider = fOpenAI(model_engine=model_name)
        self._grounded = Groundedness(groundedness_provider=self._openai_provider)
        self.save_reason = save_reason

    def _evaluate_method(self, method_func: callable, data_dict: dict) -> dict:
        """General method evaluation"""
        res = method_func(data_dict)
        result = {'score': res['score']}

        if self.save_reason:
            result['reason'] = res['reason']
        return result

    def evaluate(self, data_obj: dict) -> dict:
        """Evaluate by trulens"""
        choice_list, data_dict = data_obj['choice_list'], data_obj['data_dict']
        res_dict = {}
        for choice in choice_list:
            if choice == 'groundness':
                self._validate_params(data_dict, ['context', 'answer'], 'groundness')
                res_dict['groundness'] = self._evaluate_method(self._groundness, data_dict)

            if choice == 'context_relevancy':
                self._validate_params(data_dict, ['context', 'question'], 'context_relevancy')
                res_dict['context_relevancy'] = self._evaluate_method(
                    self._context_relevancy, data_dict
                )

            if choice == 'answer_relevancy':
                self._validate_params(data_dict, ['question', 'answer'], 'answer_relevancy')
                res_dict['answer_relevancy'] = self._evaluate_method(
                    self._answer_relevancy, data_dict
                )

        return res_dict

    def _validate_params(self, data_dict: dict, required_params: list, method_name: str):
        """Validate required parameters"""
        missing_params = [param for param in required_params if param not in data_dict]
        if missing_params:
            raise ValueError(f'{method_name} should include {", ".join(missing_params)} attribute')

    def _groundness(self, data_dict: dict) -> dict:

        res = self._grounded.groundedness_measure_with_cot_reasons(
            data_dict['context'], data_dict['answer']
        )

        return {
            'score': self._grounded.grounded_statements_aggregator(res[0]),
            'reason': res[1]['reason']
        }

    def _context_relevancy(self, data_dict: dict) -> dict:

        res = self._openai_provider.qs_relevance_with_cot_reasons(
            data_dict['question'], data_dict['context']
        )

        return {
            'score': res[0],
            'reason': res[1]['reason']
        }

    def _answer_relevancy(self, data_dict: dict) -> dict:

        res = self._openai_provider.relevance_with_cot_reasons(
            data_dict['question'], data_dict['answer']
        )

        return {
            'score': res[0],
            'reason': res[1]['reason']
        }
