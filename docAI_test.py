from google.cloud import documentai_v1beta2 as documentai
from google.oauth2 import service_account
from google.cloud import language
from google.cloud.language import types
from google.cloud import language_v1
from google.cloud.language_v1 import enums

cred_path = 'credentials.json'
credentials = service_account.Credentials.from_service_account_file(cred_path)
project_id = 'zourcing-280300'

def sample_analyze_entities(input_uri):
    """
    Analyzing Entities in text file stored in Cloud Storage
    """

    client = documentai.DocumentUnderstandingServiceClient(credentials=credentials)
    gcs_source = documentai.types.GcsSource(uri=input_uri)
    input_config = documentai.types.InputConfig(gcs_source=gcs_source, mime_type='application/pdf')
    parent = 'projects/{}/locations/us'.format(project_id)
    request = documentai.types.ProcessDocumentRequest(parent=parent, input_config=input_config)
    document = client.process_document(request=request)

    client = language_v1.LanguageServiceClient(credentials=credentials)


    type_ = enums.Document.Type.PLAIN_TEXT
    document = {"content": document.text, "type": type_}

    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))

        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{}: {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            # Get the mention type, e.g. PROPER for proper noun
            print(u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name))

    """
    response = client.analyze_sentiment(document, encoding_type=encoding_type)
    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(u"Document sentiment magnitude: {}".format(response.document_sentiment.magnitude))

    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))
    """

cvs = ['1107 (Jose Luis Rodriguez Hernandez)/Cvs 26 marzo/CVAndreaMonserratMartinezMurillo.pdf',
        '1512(Flor de María Amado Ruiz)/ABRAAM BONILLA.pdf', '1211 (Marisol Rojas)/4 Marzo/Angelica LM CV2020.pdf',
        '1431 (Roberto Puon)/CVs 19 marzo/CV Alducin Garcia Marco Antonio 2020.pdf', '1438 (Edith Pantaleon Gutierrez)/CV Juan Antonio.pdf',
        '1089 (Luz Vistraín)/Daniel_Pedraza.pdf', '1089 (Luz Vistraín)/Carlos Alberto Torres Martinez Embebidos.pdf', '1089 (Luz Vistraín)/Joel Baez.pdf',
        '1089 (Luz Vistraín)/Technical Lead  Oscar Valencia.pdf', '1511/CV VICTOR GARCIA.docx', '1438 (Edith Pantaleon Gutierrez)/CVVMSR.docx',
        '1348 (Karla Muciño)/Gerentes Admon y Finanzas/CVGeorginaOrtegaOsorio.docx', '1305 (Daniela Uribe)/Curriculum Jocelyn.docx',
        '1089 (Luz Vistraín)/Carlos Alberto Torres Martinez Embebidos.docx', '1089 (Luz Vistraín)/6 de Abril/SAP ABAP Arturo Castillo.pdf',
        '1511/CV Alberto Cardenas.pdf']

cv_path = 'gs://curriculums_bucket/CVS/'
CVs = [ cv_path + cv for cv in cvs]


sample_analyze_entities(CVs[1])
