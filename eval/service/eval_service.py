"""evaluator service"""
from utils.Config import (
    ragas_config, 
    trulens_config
)
from eval.manager.ragas_manager import RagasManager
from eval.manager.trulens_manager import TrulensManager

def eval_service(eval_data_csv, args):
    """eval dataset"""
    ragas_attr = list(set(ragas_config.methods).intersection(set(args.methods)))
    trulens_attr = list(set(trulens_config.methods).intersection(set(args.methods)))

    # # initial ragas obj
    if ragas_attr:
        ragas_service = RagasManager(model_name=args.model_name)
        ragas_scores = process_ragas_service(ragas_service, eval_data_csv, ragas_attr)
        for method in ragas_attr:
            if method in ragas_scores:
                eval_data_csv[method] = ragas_scores[method]['score']

    # initial trulens obj
    if trulens_attr:
        tru_service = TrulensManager(model_name=args.model_name, save_reason=args.gpt_reason)
        tru_scores, tru_reasons = process_trulens_service(
            tru_service, eval_data_csv, trulens_attr, args.gpt_reason
            )
        for method in trulens_attr:
            if method in tru_scores:
                eval_data_csv[method] = tru_scores[method]
            if method in tru_reasons:
                eval_data_csv[method + "_reason"] = tru_reasons[method]

    return eval_data_csv

def process_trulens_service(tru_service: TrulensManager, eval_data, methods: str, gpt_reason: bool):
    """handle trulens evaluate"""
    scores = {method: [] for method in methods}
    reasons = {method: [] for method in methods if gpt_reason}

    for _, row in eval_data.iterrows():
        data_dict = {
            'question': row['question'] if 'question' in row else '', 
            'context': row['context']  if 'context' in row else '', 
            'answer': row['answer'] if 'answer' in row else ''
            }
        tru_res = tru_service.evaluate({
            'choice_list': methods, 
            'data_dict': data_dict
        })

        for method in methods:
            if method in tru_res:
                scores[method].append(tru_res[method]['score'])
                if gpt_reason:
                    reasons[method].append(tru_res[method].get('reason', ''))

    return scores, reasons

def process_ragas_service(ragas_service: RagasManager, eval_data, methods: str):
    """handle ragas evaluate"""

    ragas_res = ragas_service.evaluate({
        'choice_list': methods, 
        'eval_df': eval_data
    })

    return ragas_res
