import { BrowserRouter, Routes, Route } from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import DocumentsPage from "./pages/DocumentsPage";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        <Route path="/documents" element={<DocumentsPage />} />

        <Route path="/chat/:documentId" element={<ChatPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
