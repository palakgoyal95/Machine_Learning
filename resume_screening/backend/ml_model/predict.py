import PyPDF2
import pickle


def extract_text_from_pdf(pdf_file):

    text = ""

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:

        text += page.extract_text()

    return text



model = pickle.load(

    open(

        "ml_model/model.pkl",

        "rb"

    )

)


vectorizer = pickle.load(

    open(

        "ml_model/vectorizer.pkl",

        "rb"

    )

)
# Function to predict suitability
def predict_resume(text):

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)[0]


    classes = model.classes_


    result = []

    for role,score in zip(

        classes,

        probabilities

    ):

        result.append(

            {

                "role":role,

                "confidence":

                round(

                    score*100,

                    2

                )

            }

        )


    result = sorted(

        result,

        key=lambda x:x["confidence"],

        reverse=True

    )


    return {

        "predicted_role":

        prediction,


        "confidence":

        result[0]["confidence"],


        "top_matches":

        result[:3]

    }