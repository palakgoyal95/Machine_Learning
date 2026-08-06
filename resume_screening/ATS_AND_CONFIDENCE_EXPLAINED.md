# ATS Score and Model Confidence: Project Explanation

This document explains the two percentages shown by the Resume Screening application:

- **ATS score**: an explainable rule-based score for resume readiness and, when supplied, match with a particular job description.
- **Match confidence**: a machine-learning model's estimated probability that the resume most resembles one of the role categories it was trained on.

They answer different questions. They must not be compared as though they mean the same thing.

| Displayed result | Question it answers | Method |
| --- | --- | --- |
| ATS score | “How well is this resume structured and how well does it cover this job description?” | Transparent rules and weighted matching |
| Match confidence | “Which trained role category does this resume's wording most resemble?” | TF-IDF + Logistic Regression classifier |

## 1. End-to-end flow

1. The user uploads a text-based PDF resume. The application extracts its readable text with `PyPDF2`.
2. A lightweight document check confirms that the text has enough resume-like signals. It needs at least 40 words and at least two signals such as common resume sections, contact information, recognised skills, or education/employment wording.
3. The same extracted text is sent independently to:
   - `predict_resume()` for role and confidence; and
   - `calculate_ats_score()` for the ATS score.
4. The app displays the predicted role, the confidence for that role, the ATS score, top three role matches, recognised skills, and—if a job description was supplied—matched and missing recognised skills.

Important: an image-only/scanned PDF may contain no extractable text. In that case the system does not produce a score; it asks for a text-based resume PDF.

## 2. ATS score

### What it is

This project’s ATS score is **not a commercial ATS score** and it is **not a hiring decision**. It is an explainable 0–100 indicator designed to help review resume readiness and relevance to a pasted job description.

The implementation is in `backend/ml_model/ats.py`.

### Inputs

The function accepts:

```python
calculate_ats_score(resume_text, job_description="")
```

- `resume_text` is the readable text extracted from the uploaded resume.
- `job_description` is optional. It is the role requirements pasted by the user.

The app first finds recognised technical and professional skills in both texts. Skills are found from an internal dictionary in `backend/ml_model/skills.py`. The dictionary includes aliases; for example, `python3` is recognised as **Python**, and `reactjs` is recognised as **React**.

### A. Resume-readiness component

The system calculates a base presentation/readiness score using four observable signals:

| Signal | Maximum points | Exact calculation | Meaning |
| --- | ---: | --- | --- |
| Readable length | 35 | `min(word_count / 180, 1) × 35` | Full points at 180 recognised words or more |
| Standard sections | 35 | `min(sections_found / 4, 1) × 35` | Full points when at least 4 markers are found |
| Recognised skills | 20 | `min(skills_found / 6, 1) × 20` | Full points when at least 6 library skills are found |
| Contact details | 10 | 10 if found, otherwise 0 | Detects an email, LinkedIn/GitHub link, or phone-like number |

The score is therefore:

```text
resume_readiness = length_points + section_points + skill_points + contact_points
```

Its theoretical range is 0–100.

#### Section markers currently checked

The system looks for these words anywhere in the resume text:

```text
experience, education, skills, projects, summary, certifications
```

It counts how many of these six markers appear. Four or more give the full 35 section points. A heading that uses very different wording may not receive a point, even if the resume is well written. That is a limitation of a transparent keyword approach.

#### What counts as a word

For the readability/length measure, a word is detected with this kind of pattern:

```text
[a-z][a-z0-9+#./-]{2,}
```

In simple terms, it counts word-like technical tokens with at least three characters. This is a basic text-readability signal—not a measure of work experience, quality, seniority, or ability.

### B. When no job description is entered

If the user leaves the job-description box empty:

```text
ATS score = resume_readiness
```

So the displayed number is based only on resume length, recognised sections, recognised skills, and contact details. It should be described as **general resume readiness**, not job-fit.

### C. When a job description is entered

If the user supplies a job description, the app computes two additional matching measures.

#### 1. Required-skill coverage (55% weight)

The system extracts recognised skills from the job description and from the resume using the same skills dictionary.

```text
matched_skills = skills in both the job description and resume
missing_skills = job-description skills not found in the resume

skill_coverage = number of matched skills / number of required recognised skills
```

For example, if the job description contains six recognised skills and the resume contains four of those six:

```text
skill_coverage = 4 / 6 = 0.6667 = 66.67%
```

This is the largest part of the job-specific score because explicit skills are the most useful and auditable signal in this implementation.

#### 2. Keyword coverage (25% weight)

The app also extracts meaningful word-like terms from the job description and resume. It lowercases both texts, removes a predefined set of general words such as `required`, `experience`, `skills`, `work`, and `years`, then compares the remaining terms.

```text
keyword_coverage = matching meaningful job-description terms / meaningful job-description terms
```

This catches relevant terminology beyond the fixed skills dictionary. It is still exact word overlap; it does not understand synonyms unless they are explicitly in the skill alias dictionary.

#### 3. Weighted final score

When both skill coverage and keyword coverage are available, the final score is:

```text
ATS score =
  (0.20 × resume_readiness)
+ (0.55 × skill_coverage_percent)
+ (0.25 × keyword_coverage_percent)
```

Example:

```text
resume_readiness     = 80
skill coverage        = 66.67
keyword coverage      = 50

ATS = (0.20 × 80) + (0.55 × 66.67) + (0.25 × 50)
    = 16 + 36.67 + 12.5
    = 65.17

Displayed ATS score = 65%
```

The program rounds the final score to the nearest whole number for display.

#### Edge cases

- If no recognised skills are found in the job description, skill coverage cannot be calculated. The system omits its 55% component and **renormalises** the weights of the available components; it does not treat that as 0% skill coverage.
- If no meaningful keyword terms are found, keyword coverage is omitted and the remaining weights are renormalised.
- If no job description is supplied, only the readiness score is shown.

### What the ATS score does not use

The calculation does not use name, age, gender, ethnicity, religion, disability, marital status, photo, address/location, or other protected/personal characteristics. It also does not verify whether every claimed skill is true; it only checks whether matching terms appear in the text.

### Safe interview explanation for ATS

> “Our ATS score is an explainable 0–100 heuristic, not a hidden black-box hiring score. Without a job description, it measures basic resume readiness: readable content, standard sections, recognised skills, and contact details. With a job description, it uses 20% readiness, 55% recognised required-skill coverage, and 25% meaningful keyword overlap. We show matched and missing skills so the result is auditable.”

## 3. Match confidence

### What it is

Match confidence is the ML model's estimate of how likely the uploaded resume belongs to the **predicted role category**, based on patterns learned from labelled training resumes.

It is not:

- a measure of how good the candidate is;
- a probability of being hired;
- a suitability or eligibility decision; or
- the same as ATS score.

The implementation is in `backend/ml_model/predict.py`.

### Model artifacts used at runtime

The application loads two matching artifacts trained in Colab:

| File | Purpose |
| --- | --- |
| `backend/ml_model/model.pkl` | The trained `LogisticRegression` classifier |
| `backend/ml_model/vectorizer.pkl` | The trained `TfidfVectorizer` that turns text into numeric features |

Both files must come from the same training run. The vectorizer establishes the vocabulary and feature positions; the classifier was trained using precisely those positions. Replacing only one file would make predictions invalid or fail.

### Text preprocessing

Before prediction, the app performs minimal normalisation:

1. If the text is empty, it returns no prediction.
2. It collapses repeated whitespace into a single space.
3. It removes leading and trailing spaces.

This intentionally preserves most wording because the saved TF-IDF vectorizer is responsible for the training-compatible text feature representation.

### Step 1: TF-IDF vectorization

Computers cannot directly use raw words as inputs. `TfidfVectorizer` converts the resume text into a numeric vector.

TF-IDF means **Term Frequency–Inverse Document Frequency**:

- **Term frequency (TF)** increases when a term appears in the resume.
- **Inverse document frequency (IDF)** reduces the importance of very common terms and gives more weight to terms that are more distinctive in the training corpus.

The vector contains a number for every learned vocabulary feature (words and, depending on training settings, word pairs). A resume that mentions words associated with Python/data engineering receives features different from one that emphasizes frontend/UI terms.

```text
resume text → saved TF-IDF vectorizer → numeric feature vector
```

### Step 2: Logistic Regression role classification

The trained multiclass `LogisticRegression` model reads the numeric vector and produces a score for each known category. The saved model has these 15 categories:

```text
AI/ML Specialists Resumes
Backend Developers Resumes
Blockchain Developers Resumes
Cloud Architects Resumes
Data Analysts Resumes
Database Administrators Resumes
DevOps Engineers Resumes
Frontend Developers Resumes
Full Stack Developers Resumes
Game Developers Resumes
Mobile Developers Resumes
Python Developers/Data Engineers Resumes
QA Engineers Resumes
Security Engineers Resumes
Technical Project Managers Resumes
```

The predicted role is the category with the highest model probability:

```text
predicted_role = category with maximum probability
```

### Step 3: Confidence percentage

`LogisticRegression` provides `predict_proba()`. This returns a probability for every role class. The probabilities sum to approximately 1 (100%).

```text
confidence = probability of predicted_role × 100
```

For example, if the output is:

| Role | Probability |
| --- | ---: |
| Python Developers/Data Engineers | 0.78 |
| Data Analysts | 0.14 |
| Backend Developers | 0.05 |
| All other roles combined | 0.03 |

the application displays:

```text
Best-fit role: Python Developers/Data Engineers
Match confidence: 78.0%
```

It also sorts all class probabilities and displays the top three role matches. This lets the user see whether the model strongly prefers one category or whether two categories are close.

### How to interpret high and low confidence

| Confidence | Practical interpretation |
| --- | --- |
| High | The resume wording looks relatively similar to training examples in one category compared with the other available categories. |
| Medium | More than one trained role may be plausible; review the top matches. |
| Low | The resume may be mixed, unusual, sparse, outside the dataset, or similarly related to several categories. Human review is especially useful. |

The dashboard uses these display labels:

- **80% or higher:** Strong pattern match
- **55% to below 80%:** Moderate pattern match
- **Below 55%:** Low pattern match

These labels are UI guidance, not scientifically calibrated hiring thresholds.

### Fallback behaviour

The current saved classifier has `predict_proba()`, so normal confidence calculation uses the probabilities above. For compatibility, the code has fallbacks:

1. If a model has no usable `predict_proba()` but has `decision_function()`, the app applies softmax to its scores to form relative probabilities.
2. If neither is available, it reports the predicted role with 100% as a technical fallback.

That second fallback should not be interpreted as real certainty; it merely means the loaded model did not expose scores the application could use.

### Safe interview explanation for confidence

> “The confidence is the probability produced by our trained Logistic Regression classifier for the top role category. We first transform resume text into TF-IDF features, then the classifier produces probabilities across the trained role labels. The highest probability becomes the predicted role and its percentage is shown as confidence. It measures similarity to our labelled training data—not candidate quality, job eligibility, or chance of hiring.”

## 4. ATS score versus confidence: the most important distinction

| Situation | Possible result | Why it can happen |
| --- | --- | --- |
| High confidence, low ATS | The model confidently recognises a role, but the resume has weak formatting/readiness or little overlap with the specific job description. | Confidence is role-category similarity; ATS includes presentation and job-specific coverage. |
| Low confidence, high ATS | The resume is well structured and uses many job-description terms, but it is broad or does not strongly match any one of the limited trained role categories. | ATS is a rule-based text match; confidence is a choice among fixed role classes. |
| Both high | The resume has strong readiness and job overlap, and its wording closely resembles a known category. | The signals happen to agree. |
| Both low | The text may be sparse, poorly extracted, poorly targeted, or outside the training data. | This should prompt human review, not automatic rejection. |

## 5. Limitations and responsible use

1. **Dataset limitation:** the classifier only knows the categories represented in its training data. It cannot reliably identify a role outside those categories.
2. **Text extraction limitation:** PDF layout and scans can prevent correct text extraction.
3. **Keyword limitation:** ATS matching is mostly exact-term matching. A relevant synonym may be missed, and a keyword can be found without proving competence.
4. **Confidence calibration limitation:** a model probability is not automatically a real-world hiring probability. Proper calibration would require separate validation data and evaluation.
5. **No decision automation:** results should support human review, not approve/reject a person automatically.
6. **Training/data quality:** imbalance, labelling mistakes, and non-representative training samples can influence predictions.

## 6. Short project viva / interview answers

### “How do you calculate ATS score?”

> “It is a transparent weighted score. First, we calculate resume readiness from text length, standard sections, recognised skills, and contact details. If a job description is provided, we add recognised-skill coverage and meaningful keyword coverage. The weights are 20% readiness, 55% skill coverage, and 25% keyword coverage. The score is explainable because we also show which skills matched and which recognised job skills were absent.”

### “How do you calculate confidence?”

> “We use a saved TF-IDF vectorizer to convert extracted resume text into numeric features. A trained multiclass Logistic Regression model then gives probabilities for each role category. The role with the highest probability is the prediction, and that probability multiplied by 100 is the displayed confidence.”

### “Is a 90% confidence a 90% chance of getting hired?”

> “No. It only means the model found the resume much more similar to one trained role category than the other available categories. It is not a hiring probability or a judgement of the candidate.”

### “Why can the ATS score and confidence be different?”

> “They measure different things. ATS is an explainable readiness and job-description overlap score. Confidence is the ML classifier’s role-category probability. A resume can fit a category strongly but be poorly tailored to a particular vacancy, or be well tailored but not fit one trained category clearly.”

### “Is this fair?”

> “The scoring code deliberately avoids protected and personal characteristics. However, no model is automatically fair simply because those fields are not used. We treat the tool as decision support, use transparent outputs, recommend human review, and should evaluate the training data and outcomes for bias before real hiring use.”

## 7. Technical stack

| Layer | Technology | Role in this project |
| --- | --- | --- |
| Programming language | Python | Application, text processing, ML inference, and scoring logic |
| User interface | Streamlit | Multi-page web application for PDF upload, screening results, and insights |
| PDF text extraction | PyPDF2 | Reads text from uploaded text-based PDF resumes |
| Data handling | pandas | Loads and prepares CSV training data |
| Numerical computation | NumPy | Supports probability calculations and softmax fallback |
| Feature engineering | scikit-learn `TfidfVectorizer` | Converts resume text into numeric ML features |
| Classification algorithm | scikit-learn `LogisticRegression` | Predicts a role category and class probabilities |
| Train/test validation | scikit-learn `train_test_split`, metrics | Splits data and reports accuracy/classification report during training |
| Model persistence | pickle / joblib | Saves and loads the trained model and vectorizer artifacts |
| Optional backend dependencies | Django, Django REST Framework, django-cors-headers, WhiteNoise | Present in project requirements for backend/API use; the current screening UI runs through Streamlit |

## 8. Dataset, features, and target variable

### Default dataset used by the local training script

The local training script defaults to:

```text
datasets/resume_dataset_3000.csv
```

It contains 3,000 rows and these columns:

| Column | Meaning | Used by the local training script? |
| --- | --- | --- |
| `category` | Resume role label | Yes — this is the target variable (`y`) |
| `job_title` | Job-title information | No, not directly |
| `Text` | Main resume text | Yes |
| `experience_years` | Years of experience | No, not directly |
| `skills` | Skill text/field | Yes |
| `education` | Education information | No, not directly |

### Both datasets at a glance

| Dataset | Rows | Role categories | Columns |
| --- | ---: | ---: | --- |
| `datasets/resume_dataset_3000.csv` | 3,000 | 10 | `category`, `job_title`, `Text`, `experience_years`, `skills`, `education` |
| `datasets/resume_dataset_10000.csv` | 10,000 | 15 | `category`, `job_title`, `Text`, `experience_years`, `skills`, `education`, `university`, `company` |

The repository contains both files. `train.py` currently defaults only to `resume_dataset_3000.csv`; it does not automatically train on the 10,000-row dataset. In Colab, either dataset can be selected, but the model and vectorizer exported from Colab determine what the live application uses.

The 10,000-row dataset has five extra role categories compared with the 3,000-row dataset: AI/ML Specialists, Blockchain Developers, Cloud Architects, Database Administrators, and Game Developers.

### Dataset columns

| Column | Meaning | Used directly by the current local training script? |
| --- | --- | --- |
| `category` | Resume role label | Yes — this is the target variable (`y`) |
| `job_title` | Job-title information | No |
| `Text` | Main resume text | Yes |
| `experience_years` | Years of experience | No |
| `skills` | Skill text/field | Yes |
| `education` | Education information | No |
| `university` | University name; only in the 10,000-row dataset | No |
| `company` | Company name; only in the 10,000-row dataset | No |

### Target variable

The supervised-learning target variable is:

```python
y = df['category'].values
```

This means the model learns to predict `category`, the labelled resume-role class. It is a **multiclass classification** problem because one resume belongs to one of multiple role categories.

### Input feature used for local training

The local `train.py` combines the two available text fields:

```python
input_text = Text + '\n' + skills
X = df['input_text'].values
```

Thus the raw ML input is text, not a hand-entered numeric score. The TF-IDF vectorizer then transforms it into numerical features.

### Classes: both datasets versus the active Colab model

This distinction is important when explaining the project:

- The **`resume_dataset_3000.csv`** dataset currently has 10 category labels.
- The **`resume_dataset_10000.csv`** dataset currently has 15 category labels.
- The **active Colab-trained `model.pkl`** currently has 15 output classes.

The active model's 15 classes exactly match the labels in `resume_dataset_10000.csv`. This strongly indicates the Colab model was trained using that 10,000-row dataset, or another dataset with exactly the same categories. The `.pkl` files do not store the original input filename, so the Colab notebook is the final source of truth for that fact.

The active model’s 15 classes are listed in the confidence section above. Therefore, the live app can predict those 15 classes because it uses the Colab model—not because the local CSV has all 15 labels.

Do not say that the current active model was trained with the local 3,000-row CSV unless you actually retrain it from that file. The correct statement is:

> “The application currently uses a trained model exported from Colab. The repository also contains a local CSV and `train.py` as a reproducible/local-training option, but they are separate from the active exported model unless I retrain and replace the artifacts.”

## 9. Algorithm and why it was selected

### Algorithm: multiclass Logistic Regression

The active saved model is a scikit-learn `LogisticRegression` classifier. It uses:

```text
solver: lbfgs
penalty: L2 regularisation
C: 1.0
max_iter: 2000
```

It performs multiclass classification: it calculates a probability for each possible role and selects the highest one.

### Feature representation: word-level TF-IDF

The active saved vectorizer uses:

```text
analyzer: word
lowercase: True
stop_words: english
ngram_range: (1, 2)
max_features: 20,000
```

This means it uses:

- individual words (**unigrams**), such as `python` and `docker`; and
- adjacent two-word phrases (**bigrams**), such as `machine learning` and `data analysis`.

It has a learned vocabulary of 20,000 features. English stop words are removed, so very general words such as “the” and “and” do not dominate the representation.

### Why this combination is appropriate

TF-IDF plus Logistic Regression is a strong baseline for short-to-medium text classification because it is:

- fast to train and predict;
- practical for a student/project deployment;
- able to handle high-dimensional sparse text features;
- interpretable relative to many complex models; and
- able to output class probabilities for the confidence display.

It is not an LLM and it does not semantically “understand” a resume the way a human does. It learns statistical patterns from the labelled training texts.

### Regularisation

L2 regularisation discourages the model from assigning excessively large weights to individual features. This helps reduce overfitting, especially because TF-IDF produces many possible word and phrase features.

## 10. Training and evaluation workflow

### Current intended workflow

Training can be done in Google Colab. Once training is complete, export both matching artifacts:

```text
model.pkl
vectorizer.pkl
```

Place both in:

```text
backend/ml_model/
```

At runtime, `predict.py` loads them and only performs inference. It does not retrain the model when the Streamlit app starts.

### Local script workflow (reference only)

`backend/ml_model/train.py` is optional. It:

1. reads the selected CSV;
2. creates `input_text` from `Text` plus `skills`;
3. removes empty text and rows without `category`;
4. optionally samples rows with a fixed `random_state=42`;
5. splits data into 80% training and 20% testing sets;
6. uses `stratify=y` so each class is represented proportionally in both sets;
7. fits the vectorizer on the training data only;
8. trains Logistic Regression;
9. evaluates accuracy and per-class precision/recall/F1 in a classification report; and
10. saves new artifacts only when started with `--save`.

This script saves `model.joblib` and `vectorizer.joblib`. The inference code searches for `.joblib` first, then `.pkl`. Therefore, if you create `.joblib` files locally, the app will prefer them over the Colab `.pkl` files.

### Evaluation metrics

During training, the script reports:

| Metric | Meaning |
| --- | --- |
| Accuracy | Fraction of test resumes assigned the correct category |
| Precision | Of resumes predicted as a role, how many actually belonged to that role? |
| Recall | Of resumes that actually belong to a role, how many did the model find? |
| F1-score | Balance of precision and recall |
| Support | Number of test examples for that class |

For a class-imbalanced dataset, accuracy alone is not enough. The per-class classification report matters because a model can achieve good overall accuracy while performing poorly on a minority class.

### Version compatibility note

The active exported artifacts were serialized with scikit-learn `1.6.1`; the local environment currently uses `1.9.0`. They currently load, but scikit-learn warns that cross-version artifact loading may be unsafe or produce different behaviour. For reproducibility, record the Colab package versions and ideally use the same versions in deployment, or retrain and validate with the deployment version.

## 11. System architecture

```text
User uploads PDF + optional job description
              |
              v
Streamlit screening page
              |
              v
PyPDF2 extracts readable resume text
              |
       +------+------------------+
       |                         |
       v                         v
Document/resume check      ML prediction path
                             saved vectorizer -> TF-IDF features
                             saved model -> role probabilities
       |                         |
       +-----------+-------------+
                   |
                   v
         ATS scoring path (rules + skills + keyword overlap)
                   |
                   v
     UI shows role, confidence, ATS score, top 3 matches, skills
```

The optional job description affects the ATS calculation only. It does **not** change the current ML role prediction or confidence calculation.

## 12. Important implementation details to mention

1. **Separate measures:** ATS and confidence are deliberately independent so the app can give both a transparent job-description comparison and an ML role classification.
2. **Model-vectorizer pairing:** `model.pkl` and `vectorizer.pkl` must be from the same Colab training run.
3. **Inference-only deployment:** the Streamlit application loads saved artifacts; it does not train on user-uploaded resumes.
4. **No automatic rejection:** the system is designed to assist review, and results should not be treated as an automated employment decision.
5. **Privacy consideration:** uploaded resume text is processed for the current screening result. In a production version, define clear retention, access-control, consent, and deletion policies before storing candidate data.
6. **Explainability:** ATS returns matched/missing recognised skills and score details. The top three probabilities make ambiguous role predictions easier to review.
7. **Role lead:** the Insights page also calculates the gap between the first and second confidence values. A small gap indicates that the model sees multiple roles as similarly plausible.

## 13. Relevant source files

- `backend/ml_model/ats.py` — ATS formula, terms, weights, and score breakdown.
- `backend/ml_model/skills.py` — recognised skill dictionary and aliases.
- `backend/ml_model/predict.py` — model/vectorizer loading, text preprocessing, role prediction, and confidence calculation.
- `app_pages/screening_page.py` — upload flow and display of results.
- `app_pages/dashboard_page.py` — role lead and confidence labels.
