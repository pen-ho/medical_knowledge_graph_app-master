CURRENT_DIR=`pwd`
export BERT_BASE_DIR=
export DATA_DIR=../datasets
export OUTPUR_DIR=../outputs/mdner_output
TASK_NAME="mdner"
#
python ../run_ner_crf.py \
  --model_type=bert \
  --model_name_or_path='../prev_trained_model/bert-base' \
  --task_name="mdner" \
  --do_train \
  --do_eval \
  --do_lower_case \
  --data_dir=../datasets/MD \
  --train_max_seq_length=60 \
  --eval_max_seq_length=60 \
  --per_gpu_train_batch_size=24 \
  --per_gpu_eval_batch_size=24 \
  --learning_rate=3e-5 \
  --crf_learning_rate=1e-3 \
  --num_train_epochs=1.0 \
  --logging_steps=10000 \
  --save_steps=10000 \
  --output_dir=../outputs/mdner_output/mdner_output/ \
  --overwrite_output_dir \
  --seed=42 \
  --overwrite_cache
