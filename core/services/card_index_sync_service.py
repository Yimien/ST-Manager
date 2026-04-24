import logging

from core.services.index_job_worker import enqueue_index_job


logger = logging.getLogger(__name__)


def _normalize_ids(values):
    return [str(value).strip() for value in (values or []) if str(value).strip()]


def _safe_enqueue(job_type, **kwargs):
    try:
        enqueue_index_job(job_type, **kwargs)
        return True
    except Exception as exc:
        logger.error('Failed to enqueue %s for %s: %s', job_type, kwargs.get('entity_id', ''), exc)
        return False


def sync_card_index_jobs(
    *,
    card_id,
    source_path,
    cache_updated=False,
    has_embedded_wi=False,
    previous_has_embedded_wi=False,
    file_content_changed=False,
    rename_changed=False,
    force_set_cover=False,
    tags_changed=False,
    summary_changed=False,
    favorite_changed=False,
    resource_folder_changed=False,
    remove_entity_ids=None,
    remove_owner_ids=None,
):
    """Translate explicit card change facts into index reconcile jobs."""
    jobs_enqueued = []
    cleanup_entity_ids = _normalize_ids(remove_entity_ids)
    cleanup_owner_ids = _normalize_ids(remove_owner_ids)

    should_upsert_card = bool(
        summary_changed
        or favorite_changed
        or tags_changed
        or cleanup_entity_ids
        or ((file_content_changed or rename_changed or force_set_cover) and cache_updated)
    )
    if should_upsert_card:
        payload = {'remove_entity_ids': cleanup_entity_ids} if cleanup_entity_ids else None
        if payload:
            enqueued = _safe_enqueue('upsert_card', entity_id=card_id, source_path=source_path, payload=payload)
        else:
            enqueued = _safe_enqueue('upsert_card', entity_id=card_id, source_path=source_path)
        if enqueued:
            jobs_enqueued.append('upsert_card')

    should_upsert_embedded = bool(
        cache_updated and file_content_changed and (has_embedded_wi or previous_has_embedded_wi)
    )
    if should_upsert_embedded:
        if _safe_enqueue('upsert_world_embedded', entity_id=card_id, source_path=source_path):
            jobs_enqueued.append('upsert_world_embedded')

    should_upsert_owner = bool(
        resource_folder_changed
        or (cache_updated and file_content_changed)
        or cleanup_owner_ids
    )
    if should_upsert_owner:
        payload = {'remove_owner_ids': cleanup_owner_ids} if cleanup_owner_ids else None
        if payload:
            enqueued = _safe_enqueue('upsert_world_owner', entity_id=card_id, source_path=source_path, payload=payload)
        else:
            enqueued = _safe_enqueue('upsert_world_owner', entity_id=card_id, source_path=source_path)
        if enqueued:
            jobs_enqueued.append('upsert_world_owner')

    return {
        'upsert_card': 'upsert_card' in jobs_enqueued,
        'upsert_world_embedded': 'upsert_world_embedded' in jobs_enqueued,
        'upsert_world_owner': 'upsert_world_owner' in jobs_enqueued,
        'jobs_enqueued': jobs_enqueued,
    }
