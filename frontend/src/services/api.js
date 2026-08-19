const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getDocuments() {
  const response = await fetch(`${API_BASE_URL}/api/documents`);

  if (!response.ok) {
    throw new Error("Failed to fetch documents.");
  }

  return response.json();
}

export async function uploadDocument(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();

    throw new Error(error?.error?.message || "Failed to upload document.");
  }

  return response.json();
}

export async function deleteDocument(documentId) {
  const response = await fetch(`${API_BASE_URL}/api/documents/${documentId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const error = await response.json();

    throw new Error(error?.error?.message || "Failed to delete document.");
  }
}

export async function chatWithDocument(documentId, question) {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      document_id: documentId,
      question: question,
    }),
  });

  if (!response.ok) {
    const error = await response.json();

    throw new Error(error?.error?.message || "Failed to get answer.");
  }

  return response.json();
}


export async function generateQuiz(documentId, numberOfQuestions) {
  const response = await fetch(`${API_BASE_URL}/api/quiz`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      document_id: documentId,
      number_of_questions: numberOfQuestions,
    }),
  });

  if (!response.ok) {
    const error = await response.json();

    throw new Error(error?.error?.message || "Failed to generate quiz.");
  }

  return response.json();
}

export async function submitQuiz(quizId, answers) {
  const response = await fetch(`${API_BASE_URL}/api/quiz/submit`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      quiz_id: quizId,
      answers: answers,
    }),
  });

  if (!response.ok) {
    const error = await response.json();

    throw new Error(error?.error?.message || "Failed to submit quiz.");
  }

  return response.json();
}

