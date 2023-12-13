"""wrap RAGAS package"""
import ast
from datasets import Dataset
from ragas.metrics import ContextPrecision
from eval.manager.base import EvalBase

class RagasManager(EvalBase):
    """RAGAS service class"""
    # TODO: custom evaluate model
    def __init__(self, model_name = 'gpt-3.5-turbo-16k'):
        self.model_name = model_name
        self._context_precision_obj = ContextPrecision()

    def _evaluate_method(self, method_func: callable, eval_dataset: Dataset) -> dict:
        """General method evaluation"""
        res = method_func(eval_dataset)
        result = {'score': res['score']}
        return result

    def evaluate(self, data_obj: dict) -> dict:
        """Evaluate by ragas"""

        choice_list, eval_df = data_obj['choice_list'], data_obj['eval_df']
        res_dict = {}
        for choice in choice_list:
            if choice == 'context_precision':
                self._validate_params(eval_df, ['contexts', 'question'], 'context_precision')
                eval_df['contexts'] = eval_df['contexts'].apply(lambda x: ast.literal_eval(x))
                eval_dataset = Dataset.from_pandas(eval_df)
                res_dict['context_precision'] = self._evaluate_method(
                    self._context_precision, eval_dataset
                )

        return res_dict

    def _validate_params(self, data_df, required_params, method_name):
        """Validate required parameters"""
        missing_params = [param for param in required_params if param not in data_df.columns]
        if missing_params:
            raise ValueError(f'{method_name} should include {", ".join(missing_params)} attribute')

    def _context_precision(self, eval_dataset: Dataset) -> dict:

        try:
            res = self._context_precision_obj.score(eval_dataset)
            return {
                'score': res['context_precision']
            }
        except Exception as e:
            raise ValueError("call RAGAS context precision error: ") from e
