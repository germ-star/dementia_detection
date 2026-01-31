The main contribution of our project  is the extraction of disfluency markers as explicit tokens. This will alllow the model can attend to these discriminative features.
This way of augmennting the data will be called Pauses-based dusfluency markers (PAT-DM).
GCN + PAT-DM model for dementia detection using DementiaBank full dataset.
A total of 7 markers we added (FILLER, FRAGMENT, REPEAT, INCOMPLETE, TRAILING, RESTART, PAUSES)

## How we built the architecture

- **Model**: GCN with Naive Attention Pooling
- **Input**: 385 dimensions (SBERT 384 + disfluency count 1)
- **Layers**: 385 → 128 → 64 → 32 → 2
- **Key Features**:
  - PAT-DM augmentation (preserves disfluency markers)
  - Sentence-level graph construction
  - Semantic + sequential edges
  - Patient-level splitting (no data leakage)

## Files

```
dementia_d2/
├── utils.py              # PAT-DM augmentation, graph building, patient splits
├── data_loader.py        # for loading CSV and prepare graphs
├── model.py              # GCN with naive attention. (we tested GAT and result was almost the same but with more complexity, hence, we kept GCN)
├── main_cv.py            # 5-fold patient-level CV to avoid data leakage because some patients have more than one visit in the dataset
├── main_holdout.py       # 80/10/10 train/val/test split
├── compare_datasets.py   # compare first visit (D1) dataset vs fuull dataset (D2) performance
└── predictions/          # results prediction of the model
```

## Usage

### 1. 5-Fold Cross-Validation (Primary Evaluation)

```bash
python main_cv.py /path/to/D2_all_visits_raw.csv
```

This runs:
- this model will 25 evaluations in total
- patient-level stratified splitting
- saves checkpoints for each fold
- saves predictions CSV with columns: `patient_id, true_label, predicted_label, fold, seed`

### 2. 80/10/10 Holdout Split (Secondary Evaluation)

```bash
python main_holdout.py /path/to/D2_all_visits_raw.csv
```

This runs:
- 5 seeds with different train/val/test splits
- validation-based early stopping
- saves best checkpoint per seed
- reports test set performance

### 3. Compare D1 vs D2

```bash
python compare_datasets.py
```

This runs the same model on both datasets and compares:
- D1 (241 first visits) vs D2 (552 all visits)
- statistical significance test
- performance difference

## Requirements

```bash
pip install torch torch-geometric sentence-transformers scikit-learn pandas numpy scipy
```

## Model Hyperparameters

```python
# Architecture
input_dim = 385          # SBERT (384) + disfluency (1)
hidden_dim = 128         # GCN layer 1
output_dim = 64          # GCN layer 2
mlp_dim = 32             # MLP hidden
n_classes = 2            # Control, Dementia

# Training
learning_rate = 0.001
weight_decay = 0.01
dropout = 0.5
batch_size = 1           # Graph-level (one transcript at a time)
epochs = 100
patience = 15            # Early stopping for overfitting

# Graph construction
similarity_threshold = 0.5
max_sentences = 25
min_sentence_words = 2
```

## Notes
- we did mulitple seeds to check robustness of the model
