from google.cloud import documentai_v1beta2 as documentai
from google.oauth2 import service_account
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

cred_path = 'credentials.json'
credentials = service_account.Credentials.from_service_account_file(cred_path)


def process_document(project_id = 'zourcing-280300', input_uri='gs://cloud-samples-data/documentai/invoice.pdf'):
    """Process a single document with the Document AI API, including
    text extraction and entity extraction."""

    client = documentai.DocumentUnderstandingServiceClient(credentials=credentials)

    gcs_source = documentai.types.GcsSource(uri=input_uri)

    # mime_type can be application/pdf, image/tiff,
    # and image/gif, or application/json
    input_config = documentai.types.InputConfig(gcs_source=gcs_source, mime_type='application/pdf')

    # Location can be 'us' or 'eu'
    parent = 'projects/{}/locations/us'.format(project_id)
    request = documentai.types.ProcessDocumentRequest(parent=parent, input_config=input_config)

    document = client.process_document(request=request)

    # All text extracted from the document
    print('Document Text: {}'.format(document.text))

    def _get_text(el):
        """Convert text offset indexes into text snippets.
        """
        response = ''
        # If a text segment spans several lines, it will
        # be stored in different text segments.
        for segment in el.text_anchor.text_segments:
            start_index = segment.start_index
            end_index = segment.end_index
            response += document.text[start_index:end_index]
        return response

    # for entity in document.entities:
    #     print('Entity type: {}'.format(entity.type))
    #     print('Text: {}'.format(_get_text(entity)))
    #     print('Mention text: {}\n'.format(entity.mention_text))

    return document


def get_email(text, substring='@', num_chars=20):

    idx = text.find(substring)
    if idx < num_chars:
        num_chars = idx
    list_candidates = [i for i in text[idx - num_chars:idx + num_chars].split('\n') if substring in i]
    cleaned_candidates = [email.replace(' ', '') for email in list_candidates]
    return cleaned_candidates


def sentiment_analysis(input_uri='gs://cloud-samples-data/documentai/invoice.pdf'):

    # Instantiates a client
    client = language.LanguageServiceClient(credentials=credentials)

    # The text to analyze
    text = process_document(input_uri=input_uri).text.encode("utf-8")
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document)

    return sentiment


def print_sentiment_result(sentiment):
    score = sentiment.document_sentiment.score
    magnitude = sentiment.document_sentiment.magnitude

    for index, sentence in enumerate(sentiment.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))

    print('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    return 0


#input_uri = 'gs://cv_files_qw/CV2.pdf'
input_uri = 'gs://curriculums_bucket/CVS/1114 (Sofia Curiel)/CV Michelle Montiel.pdf'

# Making sentiment analysis of CV (score --> positive / negative) and magnitude -->emotionality
sentiment_result = sentiment_analysis(input_uri=input_uri)

# Get emails from CV
document_result = process_document(input_uri=input_uri)
list_emails = get_email(document_result.text)

print_sentiment_result(sentiment_result)
print(list_emails)
