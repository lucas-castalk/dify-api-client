# Add chunks to a document
# pip install dify-api-client==0.0.5
import argparse
import os

import dotenv

from dify_client import DifyClient, models


dotenv.load_dotenv()

DIFY_API_BASE = os.getenv("DIFY_API_BASE")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")


client = DifyClient(
    api_key=DIFY_API_KEY,
    api_base=DIFY_API_BASE,
    verify_ssl=False,
    follow_redirects=True,
)


def add_chunk_to_document():
    response = client.add_chunk_to_document(
        dataset_id="894f6555-f3a6-43a0-9891-579cd64beaa8",
        document_id="ef510e1a-41a7-4c15-99a2-34949412cba4",
        req=models.AddChunkToDocumentRequest(
            segments=[
                models.Segment(
                    content="Hello, world!",
                    answer="Hello, world!",
                    keywords=["hello", "world"],
                )
            ]
        ),
    )

    print(response)


def create_document_by_text():
    rules = models.Rule(
        pre_processing_rules=[
            {
                "id": "remove_extra_spaces",
                "enabled": True,
                "type": "remove_urls_emails",
                "params": True,
            }
        ],
        segmentation={
            "separator": "\n",
            "max_tokens": 10000,
        },
        parent_mode="full-doc",
        subchunk_segmentation={
            "separator": "sentence",
            "max_tokens": 10000,
            "chunk_overlap": 0,
        },
    )
    request = models.CreateDocumentByTextRequest(
        name="test_document",
        text="This is a test document content for the knowledge base.",
        indexing_technique=models.IndexModel.ECONOMY.value,
        doc_form=models.DocForm.TEXT_MODEL.value,
        process_rule=models.ProcessRule(
            mode=models.SegmentationMode.AUTOMATIC.value,
            rules=rules.model_dump(),
        ),
    )
    print(request.model_dump())
    response = client.create_document_by_text(
        dataset_id="894f6555-f3a6-43a0-9891-579cd64beaa8",
        req=request,
    )
    print(response)


def create_document_by_file():
    rules = models.Rule(
        pre_processing_rules=[
            {
                "id": "remove_extra_spaces",
                "enabled": True,
                "type": "remove_urls_emails",
                "params": True,
            }
        ],
        segmentation={
            "separator": "\n\n",
            "max_tokens": 1024,
        },
        parent_mode="full-doc",
        subchunk_segmentation={
            "separator": "sentence",
            "max_tokens": 1024,
            "chunk_overlap": 50,
        },
    )
    request = models.CreateDocumentByFileRequest(
        indexing_technique=models.IndexModel.HIGH_QUALITY.value,
        doc_form=models.DocForm.TEXT_MODEL.value,
        process_rule=models.ProcessRule(
            mode=models.SegmentationMode.CUSTOM.value,
            rules=rules.model_dump(),
        ),
    )
    print(request.model_dump())
    file_path = "data/expo_presentation_iori.jp.txt"
    response = client.create_document_by_file(
        dataset_id="97937f3c-f2c6-4c4b-b266-f1b22a509b4e",
        req=request,
        file=file_path,
    )
    print(response)


def get_documents():
    response = client.get_documents(
        dataset_id="894f6555-f3a6-43a0-9891-579cd64beaa8",
    )
    print(response)


def get_metadata_list():
    response = client.get_metadata_list(
        dataset_id="894f6555-f3a6-43a0-9891-579cd64beaa8",
    )
    print(response)


def update_document_metadata():
    response = client.update_document_metadata(
        dataset_id="894f6555-f3a6-43a0-9891-579cd64beaa8",
        req=models.UpdateDocumentMetadataRequest(
            operation_data=[
                models.DocumentMetadataOperationData(
                    document_id="ab737df7-619c-4859-96db-4e3254455b62",
                    metadata_list=[
                        models.DocumentMetadataUpdate(
                            id="8f6e86d4-0cbb-4ad8-8e79-e7c0ac188cce",
                            name="language_code",
                            value="en",
                        ),
                    ],
                ),
            ]
        ),
    )
    print(response)


def create_document_metadata():
    response = client.create_document_metadata(
        dataset_id="565c440e-eaf8-49bf-8d98-003d8eb9ddba",
        req=models.CreateDocumentMetadataRequest(
            name="language_code",
            type="string",
        ),
    )
    print(response)


def get_segments():
    response = client.get_segments(
        dataset_id="23e4855b-09bd-44e7-acdb-242e12e8d54d",
        document_id="0783c885-2b8f-499f-af01-0c112b987332",
        req=models.GetSegmentsRequest(
            keyword="d53c01c27c24440e98ad65b9af7516dd",
            status="completed",
            page=1,
            limit=20,
        ),
    )
    print(response)


def get_segments_simple():
    # Simple version without request object (uses defaults)
    response = client.get_segments(
        dataset_id="23e4855b-09bd-44e7-acdb-242e12e8d54d",
        document_id="0783c885-2b8f-499f-af01-0c112b987332",
    )
    print(response)


def update_segment():
    response = client.update_segment(
        dataset_id="23e4855b-09bd-44e7-acdb-242e12e8d54d",
        document_id="0783c885-2b8f-499f-af01-0c112b987332",
        segment_id="40ee72fd-91d6-4e02-bce0-e28481c97dd1",
        req=models.UpdateSegmentRequest(
            content="Updated content for this segment",
            keywords=["gackten"],
            enabled=True,
            regenerate_child_chunks=False,
        ),
    )
    print(response)


def main():
    parser = argparse.ArgumentParser(
        description="Dify API Client - Dataset Examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available modes:
  add-chunk              Add chunks to a document
  create-by-text         Create a document from text
  create-by-file         Create a document from file
  get-documents          Get all documents in a dataset
  get-metadata-list      Get metadata list for a dataset
  update-metadata        Update document metadata
  create-metadata        Create document metadata
  get-segments           Get segments/chunks from a document (with filters)
  get-segments-simple    Get segments/chunks from a document (simple)
  update-segment         Update a segment/chunk in a document
        """,
    )
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        choices=[
            "add-chunk",
            "create-by-text",
            "create-by-file",
            "get-documents",
            "get-metadata-list",
            "update-metadata",
            "create-metadata",
            "get-segments",
            "get-segments-simple",
            "update-segment",
        ],
        help="Mode to run (see list below)",
    )

    args = parser.parse_args()

    mode_to_function = {
        "add-chunk": add_chunk_to_document,
        "create-by-text": create_document_by_text,
        "create-by-file": create_document_by_file,
        "get-documents": get_documents,
        "get-metadata-list": get_metadata_list,
        "update-metadata": update_document_metadata,
        "create-metadata": create_document_metadata,
        "get-segments": get_segments,
        "get-segments-simple": get_segments_simple,
        "update-segment": update_segment,
    }

    func = mode_to_function[args.mode]
    func()


if __name__ == "__main__":
    main()
