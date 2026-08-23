import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";

import LandingPage from "./pages/LandingPage";
import DocumentsPage from "./pages/DocumentsPage";
import ChatPage from "./pages/ChatPage";
import QuizPage from "./pages/QuizPage";
import NotesPage from "./pages/NotesPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        <Route path="/documents" element={<DocumentsPage />} />

        <Route path="/chat/:documentId" element={<ChatPage />} />

        <Route path="/quiz/:documentId" element={<QuizPage />} />

        <Route path="/notes/:documentId" element={<NotesPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
