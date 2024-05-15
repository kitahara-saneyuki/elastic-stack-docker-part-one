import re

from celery_app import celery_app
from embeddings import embeddings
from elasticsearch import Elasticsearch, helpers


ES_HOST = "https://es01:9200/"
ES_PASS = "y5AADXZR0l63CvTz1AsWznNiAM1Ukq7KSd3MEra"

client = Elasticsearch(
    # For local development
    hosts=[ES_HOST],
    basic_auth=('elastic', ES_PASS), 
    verify_certs=False
)


@celery_app.task(
    bind=True,
    name="ingest_data",
    autoretry_for=(),
    default_retry_delay=30,
    acks_late=True,
    task_reject_on_worker_lost=True,
)
def ingest_data(self, **kwargs):
    kwargs["docs"] = list(map(lambda doc: 
        doc | {
            "passages":list(map(lambda sentence: {
                "text": sentence,
                "vector": {
                    "predicted_value": embeddings.embed_query(sentence),
                    "is_truncated": False,
                    "model_id": "baai__bge-large-zh-v1.5"
                },
            }, [sentence for sentence in re.split('(?<=[。！？…])', doc["text"]) if len(sentence) > 0]))
        },
        kwargs["docs"]
    ))
    response = helpers.bulk(
        client,
        kwargs["docs"],
        refresh=True,
        request_timeout=60 * 10,
    )


@celery_app.task(
    bind=True,
    name="ingest_data_es",
    autoretry_for=(),
    default_retry_delay=30,
    acks_late=True,
    task_reject_on_worker_lost=True,
)
def ingest_data_es(self, **kwargs):
    response = helpers.bulk(
        client,
        kwargs["docs"],
        refresh=True,
        request_timeout=60 * 10,
    )
