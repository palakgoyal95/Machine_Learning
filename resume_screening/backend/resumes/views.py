from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from backend.ml_model.predict import extract_text_from_pdf, predict_resume 
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_resume(request):

    uploaded_file = request.FILES.get('resume')
    if  not uploaded_file:
        return Response({"error": "No file uploaded."}, status=400)

    try:
        text = extract_text_from_pdf(uploaded_file)

        if not text:
            return Response({"error": "No readable text was found in the uploaded PDF."}, status=400)

        prediction = predict_resume(text)
        return Response({"message": "Resume uploaded successfully.", "prediction": prediction}, status=200)
    except Exception as exc:
        return Response({"error": f"Unable to analyze resume: {exc}"}, status=500)

