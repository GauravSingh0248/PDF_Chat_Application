from collections import defaultdict
import json
import re

from langchain_groq import ChatGroq
from pydantic import ValidationError

from app.core.exceptions import (
    DocumentContentNotFoundException,
    DocumentNotFoundException,
    DocumentNotReadyException,
    InsufficientPYQDocumentsException,
    PYQAnalysisFailedException,
)
from app.database.document_repository import get_document
from app.rag.pyq_prompt import PYQ_PROMPT
from app.rag.retriever import get_documents_chunks
from app.schemas.pyq import PYQAnalysis, PYQAnalysisRequest


def _paper_label(filename: str) -> str:
    """Use the filename (without extension) as the year/paper label."""

    name = filename.rsplit(".", 1)[0] if "." in filename else filename
    return name.strip() or filename


def _extract_json_payload(content: str) -> str:
    """Strip markdown fences if the model wraps JSON."""

    stripped = content.strip()

    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped, count=1)
        stripped = re.sub(r"\s*```$", "", stripped, count=1)

    return stripped.strip()


def _as_string_list(value) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        return [value] if value.strip() else []

    if isinstance(value, list):
        return [str(item) for item in value if item is not None and str(item).strip()]

    return [str(value)]


def _normalize_importance(value) -> str:
    if isinstance(value, str):
        normalized = value.strip().capitalize()
        if normalized in {"High", "Medium", "Low"}:
            return normalized

    return "Medium"


def _normalize_analysis_payload(data: dict) -> dict:
    """
    Coerce common LLM field aliases into the PYQAnalysis schema.
    gpt-oss often returns near-correct JSON with renamed keys.
    """

    topics = []
    for topic in data.get("topics") or []:
        if not isinstance(topic, dict):
            continue

        topic_name = topic.get("topic") or topic.get("name")
        if not topic_name:
            continue

        topics.append(
            {
                "topic": str(topic_name),
                "frequency": int(topic.get("frequency") or 1),
                "years_appeared": _as_string_list(
                    topic.get("years_appeared") or topic.get("years")
                ),
                "importance": _normalize_importance(topic.get("importance")),
                "reason": str(
                    topic.get("reason")
                    or topic.get("explanation")
                    or "Appears across the selected papers."
                ),
            }
        )

    repeated_questions = []
    for item in data.get("repeated_questions") or []:
        if not isinstance(item, dict):
            continue

        question = (
            item.get("question")
            or item.get("question_family")
            or item.get("canonical_question")
            or item.get("text")
        )
        if not question:
            continue

        repeated_questions.append(
            {
                "question": str(question),
                "frequency": int(item.get("frequency") or 1),
                "years_appeared": _as_string_list(
                    item.get("years_appeared") or item.get("years")
                ),
                "topic": str(item.get("topic") or "General"),
            }
        )

    similar_questions = []
    for group in data.get("similar_questions") or []:
        if not isinstance(group, dict):
            continue

        variants = group.get("similar_variants")
        if variants is None:
            variants = group.get("group") or group.get("variants") or []

        variant_list = _as_string_list(variants)
        representative = (
            group.get("representative_question")
            or group.get("question")
            or (variant_list[0] if variant_list else None)
        )
        if not representative:
            continue

        similar_questions.append(
            {
                "representative_question": str(representative),
                "similar_variants": variant_list,
                "frequency": int(group.get("frequency") or max(len(variant_list), 1)),
                "years_appeared": _as_string_list(
                    group.get("years_appeared") or group.get("years")
                ),
                "topic": str(group.get("topic") or "General"),
            }
        )

    important_topics = _as_string_list(data.get("important_topics"))
    if not important_topics:
        important_topics = [topic["topic"] for topic in topics[:5]]

    exam_focus_summary = (
        data.get("exam_focus_summary")
        or data.get("summary")
        or data.get("focus_summary")
        or ""
    )

    return {
        "subject": data.get("subject"),
        "papers_analyzed": _as_string_list(data.get("papers_analyzed")),
        "topics": topics,
        "repeated_questions": repeated_questions,
        "similar_questions": similar_questions,
        "important_topics": important_topics,
        "exam_focus_summary": str(exam_focus_summary).strip()
        or "Cross-year patterns were identified from the selected papers.",
    }


def _build_multi_paper_context(
    document_ids: list[str],
    papers: list[dict],
) -> tuple[str, list[str]]:
    result = get_documents_chunks(document_ids)

    documents = result.get("documents") or []
    metadatas = result.get("metadatas") or []

    if not documents:
        raise DocumentContentNotFoundException(
            "No vector content found for the selected PYQ papers. "
            "Make sure each PDF finished processing."
        )

    chunks_by_document: dict[str, list[str]] = defaultdict(list)

    for index, content in enumerate(documents):
        metadata = metadatas[index] if index < len(metadatas) else {}
        doc_id = metadata.get("document_id")

        if not doc_id:
            continue

        chunks_by_document[doc_id].append(content)

    paper_by_id = {paper["document_id"]: paper for paper in papers}
    paper_sections: list[str] = []
    papers_analyzed: list[str] = []

    for document_id in document_ids:
        paper = paper_by_id[document_id]
        label = _paper_label(paper["filename"])
        papers_analyzed.append(paper["filename"])

        chunks = chunks_by_document.get(document_id, [])

        if not chunks:
            raise DocumentContentNotFoundException(
                f"No content found for paper: {paper['filename']}"
            )

        paper_body = "\n\n".join(chunks)

        paper_sections.append(
            f"""
            ========== PAPER START ==========
            Paper label: {label}
            Filename: {paper['filename']}
            Document ID: {document_id}
            ---------- CONTENT ----------
            {paper_body}
            ========== PAPER END ==========
            """.strip()
        )

    return "\n\n".join(paper_sections), papers_analyzed


def analyze_pyq(request: PYQAnalysisRequest) -> PYQAnalysis:
    # Preserve order, drop duplicates
    document_ids = list(dict.fromkeys(request.document_ids))

    if len(document_ids) < 2:
        raise InsufficientPYQDocumentsException()

    papers: list[dict] = []

    for document_id in document_ids:
        document = get_document(document_id)

        if document is None:
            raise DocumentNotFoundException()

        if document["status"] != "processed":
            raise DocumentNotReadyException()

        papers.append(document)

    context, papers_analyzed = _build_multi_paper_context(
        document_ids=document_ids,
        papers=papers,
    )

    subject_line = (
        f"Subject / exam focus: {request.subject}"
        if request.subject
        else "Subject / exam focus: (not provided — infer from papers if clear)"
    )

    # gpt-oss is a reasoning model: default max tokens often get spent on
    # reasoning_content, leaving response.content empty (finish_reason=length).
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        max_tokens=8192,
        reasoning_effort="low",
    )

    prompt = PYQ_PROMPT.invoke(
        {
            "subject_line": subject_line,
            "context": context,
        }
    )

    response = llm.invoke(prompt)
    content = (
        (response.content or "").strip()
        if isinstance(response.content, str)
        else ""
    )

    if not content:
        raise PYQAnalysisFailedException(
            "The analysis model returned an empty response. "
            "Please try again with fewer papers selected."
        )

    try:
        analysis_data = json.loads(_extract_json_payload(content))
        if not isinstance(analysis_data, dict):
            raise PYQAnalysisFailedException(
                "The analysis model returned invalid JSON. Please try again."
            )

        analysis = PYQAnalysis.model_validate(
            _normalize_analysis_payload(analysis_data)
        )
    except (json.JSONDecodeError, ValidationError, TypeError, ValueError) as error:
        raise PYQAnalysisFailedException(
            "The analysis model returned invalid JSON. Please try again."
        ) from error

    return analysis.model_copy(
        update={
            "papers_analyzed": papers_analyzed,
            "subject": request.subject or analysis.subject,
        }
    )
